import streamlit as st
from datetime import datetime
import json
import re
import ast

from agent import run_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="City AI Agent",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_history" not in st.session_state:
    st.session_state.agent_history = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f6f8fb;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1rem;
        padding-bottom: 6rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #102a43 0%,
            #163a59 55%,
            #0d2439 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: #e7f0f8;
    }

    section[data-testid="stSidebar"]
    button[kind="secondary"] {

        background: #287df5 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        min-height: 44px;
        font-weight: 600;
    }

    .sidebar-heading {

        font-size: 16px;
        font-weight: 700;
        margin-top: 22px;
        margin-bottom: 10px;
        padding-top: 18px;
        border-top: 1px solid #38536b;
    }

    .header-title {

        font-size: 27px;
        font-weight: 750;
        color: #102a43;
        margin-bottom: 3px;
    }

    .header-subtitle {

        font-size: 13px;
        color: #64748b;
    }

    .online-badge {

        background: #ecfdf5;
        border: 1px solid #bbf7d0;
        color: #15803d;
        border-radius: 20px;
        padding: 7px 13px;
        font-size: 12px;
        font-weight: 650;
        text-align: center;
    }

    .welcome-title {

        text-align: center;
        color: #102a43;
        font-size: 28px;
        font-weight: 750;
        margin-top: 35px;
    }

    .welcome-subtitle {

        text-align: center;
        color: #64748b;
        font-size: 14px;
        margin-bottom: 25px;
    }

    div.stButton > button {

        border-radius: 10px;
        border: 1px solid #d5dde7;
        background: white;
        color: #17324d;
        min-height: 42px;
        font-size: 13px;
        transition: 0.2s;
    }

    div.stButton > button:hover {

        border-color: #3b82f6;
        color: #2563eb;
        background: #f8fbff;
    }

    [data-testid="stChatMessage"] {

        border-radius: 14px;
        margin-bottom: 10px;
    }

    .tool-status {

        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
        padding: 9px 12px;
        border-radius: 9px;
        font-size: 12px;
        margin: 8px 0;
    }

    @media (max-width: 800px) {

        .header-title {
            font-size: 21px;
        }

        .welcome-title {
            font-size: 23px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🏙️ City AI Agent"
    )

    st.caption(
        "AI companion for weather "
        "and latest city news."
    )

    st.write("")


    # ========================================================
    # NEW CHAT
    # ========================================================

    if st.button(
        "＋  New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.agent_history = []

        st.rerun()


    # ========================================================
    # AVAILABLE TOOLS
    # ========================================================

    st.markdown(
        '<div class="sidebar-heading">'
        '🔧 Available Tools'
        '</div>',
        unsafe_allow_html=True
    )


    with st.container(border=True):

        st.markdown(
            "### 🌦️ Weather"
        )

        st.caption(
            "Get current weather information "
            "for any city in India."
        )


    with st.container(border=True):

        st.markdown(
            "### 📰 Latest News"
        )

        st.caption(
            "Search the latest news about "
            "any city using Tavily."
        )


    # ========================================================
    # EXAMPLES
    # ========================================================

    st.markdown(
        '<div class="sidebar-heading">'
        '💡 Example Questions'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "🌤️ Weather in Mumbai"
    )

    st.caption(
        "📰 News in Pune"
    )

    st.caption(
        "🌦️ Weather and news in Delhi"
    )


    # ========================================================
    # STATUS
    # ========================================================

    st.markdown(
        '<div class="sidebar-heading">'
        '⚡ Agent Status'
        '</div>',
        unsafe_allow_html=True
    )

    st.success(
        "● Online"
    )

    st.caption(
        "Powered by LangChain • Gemini • Tavily"
    )

    st.caption(
        "Designed & Developed by Yogesh Bhore."
    )

    st.caption(
        "© 2026. All rights reserved."
    )


# ============================================================
# MAIN HEADER
# ============================================================

header_col1, header_col2 = st.columns(
    [5, 1]
)


with header_col1:

    st.markdown(
        '<div class="header-title">'
        '🏙️ City AI Agent'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="header-subtitle">'
        'Ask about weather and latest news '
        'from any city in India.'
        '</div>',
        unsafe_allow_html=True
    )


with header_col2:

    st.markdown(
        '<div class="online-badge">'
        '● Online'
        '</div>',
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="welcome-title">'
        '🌆 Explore Cities'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">'
        'Get real-time weather and latest news '
        'from cities across India.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")


    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button(
            "🌤️  Weather in Mumbai",
            use_container_width=True
        ):

            st.session_state.example_prompt = (
                "What is the current weather in Mumbai?"
            )

            st.rerun()


    with col2:

        if st.button(
            "📰  News in Pune",
            use_container_width=True
        ):

            st.session_state.example_prompt = (
                "What is the latest news in Pune?"
            )

            st.rerun()


    with col3:

        if st.button(
            "🌦️  Weather & News in Delhi",
            use_container_width=True
        ):

            st.session_state.example_prompt = (
                "Give me the current weather "
                "and latest news in Delhi."
            )

            st.rerun()


# ============================================================
# DISPLAY PREVIOUS CHAT
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(role):

        st.markdown(
            message["content"]
        )

        if message.get("time"):

            st.caption(
                message["time"]
            )


# ============================================================
# INPUT
# ============================================================

example_prompt = st.session_state.pop(
    "example_prompt",
    None
)


user_prompt = st.chat_input(
    "Ask about weather or latest city news..."
)


prompt_to_process = (

    user_prompt

    if user_prompt

    else example_prompt
)


# ============================================================
# PROCESS USER REQUEST
# ============================================================

if prompt_to_process:

    current_time = datetime.now().strftime(
        "%I:%M %p"
    )


    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    st.session_state.messages.append({

        "role": "user",

        "content": prompt_to_process,

        "time": current_time

    })


    # ========================================================
    # DISPLAY USER MESSAGE
    # ========================================================

    with st.chat_message("user"):

        st.markdown(
            prompt_to_process
        )

        st.caption(
            current_time
        )


    # ========================================================
    # RUN AGENT
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "City AI is thinking..."
        ):

            try:

                result = run_agent(

                    prompt_to_process,

                    st.session_state.agent_history
                )


                answer = result["answer"]

                history = result["history"]

                tool_results = result["tool_results"]


                # =================================================
                # SAVE HISTORY
                # =================================================

                st.session_state.agent_history = history


                # =================================================
                # TOOL ACTIVITY
                # =================================================

                for tool in tool_results:

                    tool_name = tool["name"]

                    st.markdown(

                        f"""
                        <div class="tool-status">

                        🔧 <b>{tool_name}</b>

                        &nbsp; • &nbsp;

                        Automatically executed

                        </div>
                        """,

                        unsafe_allow_html=True
                    )


                # =================================================
                # ASSISTANT ANSWER
                # =================================================

                st.markdown(
                    answer
                )


                st.caption(
                    datetime.now().strftime(
                        "%I:%M %p"
                    )
                )


                # =================================================
                # WEATHER RESULT
                # =================================================

                for tool in tool_results:

                    if tool["name"] != "get_weather":
                        continue


                    result_text = tool["result"]


                    # =================================================
                    # PARSE WEATHER RESULT
                    # =================================================

                    weather = None


                    # -------------------------------------------------
                    # METHOD 1: JSON
                    # -------------------------------------------------

                    try:

                        weather = json.loads(
                            result_text
                        )

                    except (
                        json.JSONDecodeError,
                        TypeError
                    ):

                        weather = None


                    # -------------------------------------------------
                    # METHOD 2: Python dictionary string
                    # -------------------------------------------------

                    if weather is None:

                        try:

                            weather = ast.literal_eval(
                                result_text
                            )

                        except (
                            ValueError,
                            SyntaxError,
                            TypeError
                        ):

                            weather = None


                    # -------------------------------------------------
                    # IF WEATHER CANNOT BE PARSED
                    # -------------------------------------------------

                    if not isinstance(weather, dict):

                        st.warning(
                            "Weather data could not be displayed."
                        )

                        continue


                    # =================================================
                    # CHECK ERROR
                    # =================================================

                    if not weather.get(
                        "success",
                        True
                    ):

                        st.error(
                            weather.get(
                                "error",
                                "Weather data unavailable."
                            )
                        )

                        continue


                    # =================================================
                    # EXTRACT SIX FIELDS
                    # =================================================

                    city = weather.get(
                        "city",
                        "--"
                    )

                    latitude = weather.get(
                        "latitude",
                        "--"
                    )

                    longitude = weather.get(
                        "longitude",
                        "--"
                    )

                    temperature = weather.get(
                        "temperature",
                        "--"
                    )

                    pressure = weather.get(
                        "pressure",
                        "--"
                    )

                    humidity = weather.get(
                        "humidity",
                        "--"
                    )


                    # =================================================
                    # WEATHER DASHBOARD
                    # =================================================

                    st.markdown(
                        "### 🌦️ Current Weather"
                    )

                    st.markdown(
                        f"## 📍 {city}"
                    )


                    # =================================================
                    # MAIN WEATHER METRICS
                    # =================================================

                    col1, col2, col3 = st.columns(3)


                    with col1:

                        st.metric(
                            "🌡️ Temperature",
                            f"{temperature} °C"
                        )


                    with col2:

                        st.metric(
                            "🔽 Pressure",
                            f"{pressure} hPa"
                        )


                    with col3:

                        st.metric(
                            "💧 Humidity",
                            f"{humidity}%"
                        )


                    # =================================================
                    # LOCATION
                    # =================================================

                    st.markdown(
                        "#### 📍 Location"
                    )


                    location1, location2 = st.columns(2)


                    with location1:

                        st.metric(
                            "Latitude",
                            latitude
                        )


                    with location2:

                        st.metric(
                            "Longitude",
                            longitude
                        )


                # =================================================
                # NEWS RESULT
                # =================================================

                for tool in tool_results:

                    if tool["name"] != "get_news":
                        continue


                    city = tool["args"].get(
                        "city",
                        "City"
                    )


                    result_text = tool["result"]


                    news_items = []


                    sections = result_text.split(
                        "\n\n"
                    )


                    for section in sections:

                        lines = section.splitlines()


                        if not lines:
                            continue


                        first_line = lines[0]


                        if not re.match(
                            r"^\d+\.",
                            first_line
                        ):

                            continue


                        title = re.sub(

                            r"^\d+\.\s*",

                            "",

                            first_line
                        )


                        url = ""

                        summary = ""


                        for line in lines:

                            if line.startswith(
                                "URL:"
                            ):

                                url = line.replace(
                                    "URL:",
                                    "",
                                    1
                                ).strip()


                            elif line.startswith(
                                "Summary:"
                            ):

                                summary = line.replace(
                                    "Summary:",
                                    "",
                                    1
                                ).strip()


                        news_items.append({

                            "title": title,

                            "url": url,

                            "summary": summary

                        })


                    # =================================================
                    # DISPLAY NEWS
                    # =================================================

                    if news_items:

                        st.markdown(
                            f"### 📰 Latest News — {city}"
                        )


                        news_columns = st.columns(
                            min(
                                len(news_items),
                                3
                            )
                        )


                        for index, item in enumerate(
                            news_items
                        ):

                            column = news_columns[
                                index % len(news_columns)
                            ]


                            with column:

                                with st.container(
                                    border=True
                                ):

                                    st.markdown(
                                        f"**{item['title']}**"
                                    )

                                    st.caption(
                                        item["summary"]
                                    )


                                    if item["url"]:

                                        st.link_button(
                                            "↗ Read Full Article",
                                            item["url"],
                                            use_container_width=True
                                        )


                # =================================================
                # SAVE ASSISTANT MESSAGE
                # =================================================

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": answer,

                    "time": datetime.now().strftime(
                        "%I:%M %p"
                    )

                })


            except Exception as e:

                error_message = (

                    "⚠️ Something went wrong.\n\n"

                    f"`{str(e)}`"

                )


                st.error(
                    error_message
                )


                st.session_state.messages.append({

                    "role": "assistant",

                    "content": error_message,

                    "time": datetime.now().strftime(
                        "%I:%M %p"
                    )

                })
