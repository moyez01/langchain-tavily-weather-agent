import os
import requests
import streamlit as st

from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langsmith import Client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Weather Agent",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GEMENI_API_KEY = os.getenv("GEMENI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Header */
    .main-header {
        padding: 20px 0 10px 0;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #172033;
        margin-bottom: 5px;
    }

    .main-subtitle {
        font-size: 16px;
        color: #667085;
    }

    /* Cards */
    .info-card {
        background: white;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #e6eaf0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }

    .info-card h3 {
        margin-top: 0;
        color: #172033;
    }

    .info-card p {
        color: #667085;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e6eaf0;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 14px;
    }

    /* Button */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Status */
    .status-box {
        padding: 12px 15px;
        border-radius: 10px;
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        color: #475569;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Configuration")

    st.markdown("---")

    st.markdown("### API Status")

    if GEMENI_API_KEY:
        st.success("✅ Gemini API configured")
    else:
        st.error("❌ Gemini API missing")

    if TAVILY_API_KEY:
        st.success("✅ Tavily API configured")
    else:
        st.warning("⚠️ Tavily API missing")

    if WEATHERSTACK_API_KEY:
        st.success("✅ WeatherStack configured")
    else:
        st.warning("⚠️ WeatherStack API missing")

    st.markdown("---")

    st.markdown("### 🛠️ Available Tools")

    st.markdown(
        """
        **🔎 Tavily Search**

        Used for web search and current information.

        **🌤️ WeatherStack**

        Used for current weather data.

        **🤖 Gemini**

        Used as the AI reasoning model.
        """
    )

    st.markdown("---")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-header">
        <div class="main-title">🌤️ AI Weather Agent</div>
        <div class="main-subtitle">
            Ask questions about cities, weather, locations and current information.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")


# ============================================================
# API VALIDATION
# ============================================================

if not GEMENI_API_KEY:
    st.error(
        "Gemini API key not found. Please add GEMENI_API_KEY to your .env file."
    )
    st.stop()


# ============================================================
# LLM
# ============================================================

@st.cache_resource
def create_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
        api_key=GEMENI_API_KEY,
    )


# ============================================================
# TAVILY TOOL
# ============================================================

@st.cache_resource
def create_search_tool():

    return TavilySearchResults(
        max_results=2,
    )


# ============================================================
# WEATHER TOOL
# ============================================================

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    if not WEATHERSTACK_API_KEY:
        return "WeatherStack API key is not configured."

    url = (
        "https://api.weatherstack.com/current"
        f"?access_key={WEATHERSTACK_API_KEY}"
        f"&query={city}"
    )

    try:

        response = requests.get(
            url,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if "current" not in data:
            error_info = data.get("error", {})

            if isinstance(error_info, dict):
                error_message = error_info.get(
                    "info",
                    "Unknown WeatherStack error.",
                )
            else:
                error_message = "Unknown WeatherStack error."

            return f"Could not fetch weather data for {city}: {error_message}"

        current = data["current"]

        description = current.get(
            "weather_descriptions",
            ["Unknown"],
        )[0]

        return (
            f"City: {city}\n"
            f"Temperature: {current.get('temperature')}°C\n"
            f"Weather: {description}\n"
            f"Humidity: {current.get('humidity')}%\n"
            f"Wind Speed: {current.get('wind_speed')} km/h"
        )

    except requests.RequestException as e:

        return f"Weather request failed: {str(e)}"


# ============================================================
# CREATE AGENT
# ============================================================

@st.cache_resource
def create_agent():

    llm = create_llm()

    search_tool = create_search_tool()

    tools = [
        search_tool,
        get_weather_data,
    ]

    client = Client()

    prompt = client.pull_prompt(
        "hwchase17/react",
        dangerously_pull_public_prompt=True,
    )

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

    return agent_executor


# ============================================================
# INITIALIZE CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# WELCOME CARDS
# ============================================================

if len(st.session_state.messages) == 0:

    st.markdown("### 👋 What can I help you with?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="info-card">

            <h3>🌤️ Weather</h3>

            <p>
            Get current weather information
            for any city.
            </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="info-card">

            <h3>🔎 Search</h3>

            <p>
            Search the web for current
            information.
            </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="info-card">

            <h3>🤖 AI Agent</h3>

            <p>
            Gemini decides which tool
            should be used.
            </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    st.markdown("**Try one of these:**")

    examples = [
        "What is the current weather in Dhaka?",
        "Find the capital of Bangladesh and its current weather.",
        "What is the current weather in Dubai?",
    ]

    example_cols = st.columns(3)

    for i, example in enumerate(examples):

        with example_cols[i]:

            if st.button(
                example,
                use_container_width=True,
            ):

                st.session_state.pending_prompt = example
                st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# USER INPUT
# ============================================================

pending_prompt = st.session_state.pop(
    "pending_prompt",
    None,
)

prompt = st.chat_input(
    "Ask me about weather, cities or current information..."
)

if pending_prompt:

    prompt = pending_prompt


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if prompt:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            try:

                agent_executor = create_agent()

                response = agent_executor.invoke(
                    {
                        "input": prompt
                    }
                )

                output = response.get(
                    "output",
                    "I couldn't generate a response.",
                )

            except Exception as e:

                output = f"""
                ❌ **Something went wrong**

                `{str(e)}`
                """

        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": output,
        }
    )