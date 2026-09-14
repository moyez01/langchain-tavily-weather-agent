# IMPORT
from dotenv import load_dotenv
import os
from langchain_community.tools.tavily_search import TavilySearchResults
import requests
from langchain.tools import tool
from langsmith import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_react_agent, AgentExecutor

# LOAD ENVIRONMENT
load_dotenv()
GEMENI_API_KEY = os.getenv('GEMENI_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    api_key=GEMENI_API_KEY
)

# PREDEFINED TAVILY TOOL
search_tool = TavilySearchResults(max_results=2)
result = search_tool.invoke("Give me the Current weather at Dhaka")
result

# CUStOM WEATHER TOOL
@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """
    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )
    response = requests.get(url)
    data = response.json()
    if "current" not in data:
        return f"Could not fetch weather data for {city}"
    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )

# TOOLS CALLING
tools = [search_tool, get_weather_data]

# ReAct PROMPT
client = Client()
# This modern client accepts the parameter and handles the safety barrier correctly
prompt = client.pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)

# CREATE AGENT
agent = create_react_agent(
    llm= llm,
    tools=tools,
    prompt=prompt
)

# AGENT EXECUTOR
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools,
    verbose=True
)

# INPUT
response = agent_executor.invoke({
    "input": (
        "Find the capital of Bangladesh"
        "and then find its current weather."
    )
})


print("\n========================")
print("FINAL OUTPUT")
print("========================\n")
print(response["output"])


