import os
import requests

from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()


# ============================================================
# WEATHER
# ============================================================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city in India."""

    api_key = os.getenv(
        "OPENWEATHER_API_KEY"
    )

    if not api_key:
        return (
            "Error: OPENWEATHER_API_KEY "
            "is not configured."
        )

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN"
        f"&appid={api_key}"
        "&units=metric"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        if str(data.get("cod")) != "200":

            return (
                "Error: "
                + data.get(
                    "message",
                    "Could not fetch weather"
                )
            )

        temp = data["main"]["temp"]

        feels_like = data["main"]["feels_like"]

        humidity = data["main"]["humidity"]

        description = data["weather"][0]["description"]

        return (
            f"Weather in {city}:\n"
            f"Condition: {description}\n"
            f"Temperature: {temp}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%"
        )

    except Exception as e:

        return f"Weather API error: {str(e)}"


# ============================================================
# TAVILY
# ============================================================

tavily_client = TavilyClient(
    api_key=os.getenv(
        "TAVILY_API_KEY"
    )
)


# ============================================================
# NEWS
# ============================================================

@tool
def get_news(city: str) -> str:
    """Get latest news about a city."""

    try:

        response = tavily_client.search(
            query=f"latest news in {city}",
            search_depth="basic",
            max_results=3
        )

        results = response.get(
            "results",
            []
        )

        if not results:

            return (
                f"No latest news found for {city}."
            )

        news = []

        for index, result in enumerate(
            results,
            start=1
        ):

            title = result.get(
                "title",
                "No title"
            )

            url = result.get(
                "url",
                ""
            )

            content = result.get(
                "content",
                ""
            )

            news.append(
                f"{index}. {title}\n"
                f"URL: {url}\n"
                f"Summary: {content[:350]}"
            )

        return (
            f"Latest news in {city}:\n\n"
            + "\n\n".join(news)
        )

    except Exception as e:

        return f"News API error: {str(e)}"