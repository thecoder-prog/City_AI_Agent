from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI

from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from tools import get_weather, get_news


# ============================================================
# TOOLS
# ============================================================

tools = [
    get_weather,
    get_news
]

tool_map = {
    tool.name: tool
    for tool in tools
}


# ============================================================
# PRIMARY MODEL - GEMINI
# ============================================================

gemini = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


# ============================================================
# FALLBACK MODEL 1 - GEMINI 3.1
# ============================================================

gemini_fallback = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash",
    temperature=0
)


# ============================================================
# FALLBACK MODEL 2 -  MISTRAL
# ============================================================

mistral_model = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0
)

# ============================================================
# FALLBACK MODEL 3 - OPENAI
# ============================================================


openai_model = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)


# ============================================================
# BIND TOOLS TO EACH MODEL
# ============================================================

gemini_with_tools = gemini.bind_tools(
    tools
)

gemini_fallback_with_tools = gemini_fallback.bind_tools(
    tools
)

mistral_with_tools = mistral_model.bind_tools(
    tools
)

openai_with_tools = openai_model.bind_tools(
    tools
)

# ============================================================
# PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are City AI Agent.

You help users with real-time information about
cities in India.

Available tools:

1. get_weather(city)
2. get_news(city)

Rules:

- Use get_weather for current weather.
- Use get_news for latest news.
- If both weather and news are requested,
  use both tools.
- Automatically execute required tools.
- Never invent real-time information.
- Give clear and concise answers.
"""
        ),

        MessagesPlaceholder(
            variable_name="messages"
        )
    ]
)


# ============================================================
# CREATE RUNNABLE FOR EACH MODEL
# ============================================================

gemini_chain = prompt | gemini_with_tools

gemini_fallback_chain = (
    prompt | gemini_fallback_with_tools
)

mistral_chain = prompt | mistral_with_tools

openai_chain = prompt | openai_with_tools

# ============================================================
# MULTI-MODEL FALLBACK RUNNABLE
# ============================================================

chain = gemini_chain.with_fallbacks(
    [
        gemini_fallback_chain,
        mistral_chain,
        openai_chain
        
    ]
)


# ============================================================
# CLEAN MODEL RESPONSE
# ============================================================

def clean_content(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, str):

                text_parts.append(item)

            elif isinstance(item, dict):

                text = item.get("text")

                if text:
                    text_parts.append(text)

        return "\n".join(text_parts)

    return str(content)


# ============================================================
# RUN AGENT
# ============================================================

def run_agent(user_input, history=None):

    if history is None:
        history = []

    messages = history + [
        HumanMessage(
            content=user_input
        )
    ]

    tool_results = []

    while True:

        # ====================================================
        # RUN MULTI-MODEL RUNNABLE
        # ====================================================

        response = chain.invoke(
            {
                "messages": messages
            }
        )

        messages.append(response)

        # ====================================================
        # NO TOOL CALL
        # ====================================================

        if not response.tool_calls:

            answer = clean_content(
                response.content
            )

            return {
                "answer": answer,
                "history": messages,
                "tool_results": tool_results
            }

        # ====================================================
        # AUTOMATIC TOOL EXECUTION
        # ====================================================

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call["args"]

            tool_call_id = tool_call["id"]

            selected_tool = tool_map.get(
                tool_name
            )

            # ------------------------------------------------
            # TOOL NOT FOUND
            # ------------------------------------------------

            if selected_tool is None:

                result = (
                    f"Tool '{tool_name}' "
                    f"was not found."
                )

            # ------------------------------------------------
            # EXECUTE TOOL
            # ------------------------------------------------

            else:

                try:

                    result = selected_tool.invoke(
                        tool_args
                    )

                except Exception as e:

                    result = (
                        f"Tool execution error: "
                        f"{str(e)}"
                    )

            # ------------------------------------------------
            # SAVE RESULT
            # ------------------------------------------------

            tool_results.append(
                {
                    "name": tool_name,
                    "args": tool_args,
                    "result": str(result)
                }
            )

            # ------------------------------------------------
            # SEND RESULT BACK TO MODEL
            # ------------------------------------------------

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call_id
                )
            )