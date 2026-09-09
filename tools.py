import os
import json
import requests

from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# WEATHER
# ============================================================

@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a city in India.

    Returns only:
    City, Latitude, Longitude, Temperature, Pressure, Humidity
    """

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return json.dumps({
            "success": False,
            "error": "OPENWEATHER_API_KEY is not configured."
        })

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

        response.raise_for_status()

        data = response.json()

        # ====================================================
        # API ERROR
        # ====================================================

        if str(data.get("cod")) != "200":

            return json.dumps({
                "success": False,
                "error": data.get(
                    "message",
                    "Could not fetch weather."
                )
            })

        # ====================================================
        # ONLY REQUIRED DATA
        # ====================================================

        result = {
            "city": data.get(
                "name",
                city
            ),

            "latitude": data.get(
                "coord",
                {}
            ).get(
                "lat"
            ),

            "longitude": data.get(
                "coord",
                {}
            ).get(
                "lon"
            ),

            "temperature": data.get(
                "main",
                {}
            ).get(
                "temp"
            ),

            "pressure": data.get(
                "main",
                {}
            ).get(
                "pressure"
            ),

            "humidity": data.get(
                "main",
                {}
            ).get(
                "humidity"
            )
        }

        return json.dumps(
            result,
            separators=(",", ":")
        )

    except requests.exceptions.RequestException as e:

        return json.dumps({
            "success": False,
            "error": f"Weather API error: {str(e)}"
        })

    except Exception as e:

        return json.dumps({
            "success": False,
            "error": f"Weather API error: {str(e)}"
        })


# ============================================================
# TAVILY CLIENT
# ============================================================

tavily_api_key = os.getenv(
    "TAVILY_API_KEY"
)

if tavily_api_key:

    tavily_client = TavilyClient(
        api_key=tavily_api_key
    )

else:

    tavily_client = None


# ============================================================
# NEWS
# ============================================================

@tool
def get_news(city: str) -> str:
    """
    Get latest news about a city.
    """

    if tavily_client is None:

        return (
            "Error: TAVILY_API_KEY is not configured."
        )

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

        return (
            f"News API error: {str(e)}"
        )