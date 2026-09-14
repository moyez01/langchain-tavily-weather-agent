# langchain-tavily-weather-agent
An AI-powered weather and search agent built with LangChain, leveraging Gemini LLM, Tavily Search, and WeatherStack tools for real-time weather and general web insights.

#Installation & Setup Instructions
#Follow these steps to install and run the application.

1. Download the Required Files<br>
Download the following files and place them in the same directory/folder:<br>
app.py<br>
requirements.txt<br>

2. Install Required Packages
Open Bash / Terminal in the project directory and run:<br>
pip install -r requirements.txt<br>

3. Create the .env File
Create a new file named .env in the same directory as app.py.
Add your API keys:<br>
GEMENI_API_KEY="your_gemini_api_key"<br>
TAVILY_API_KEY="your_tavily_api_key"<br>
WEATHERSTACK_API_KEY="your_weatherstack_api_key"<br>
Replace the placeholder values with your actual API keys.

4. Run the Application
Open Bash / Terminal in the project directory and run:<br>
streamlit run app.py<br>
The application will start and Streamlit will provide a local URL, usually:<br>
http://localhost:8501<br>
Open that URL in your web browser to use the application


#UI Structure
┌──────────────────────────────────────────────────────────────┐<br>
│  ⚙️ CONFIGURATION        │  🌤️ AI Weather Agent             │<br>
│                          │                                   │<br>
│  API STATUS              │  Ask questions about cities,      │<br>
│  ✅ Gemini               │  weather and current information  │<br>
│  ✅ Tavily               │                                   │<br>
│  ✅ WeatherStack         │  ┌────────┐ ┌────────┐ ┌────────┐ │<br>
│                          │  │Weather │ │ Search │ │  AI     ││<br>
│  TOOLS                   │  │  🌤️   │ │  🔎   │ │  🤖     ││<br>
│  🔎 Tavily Search        │  └────────┘ └────────┘ └────────┘│<br>
│  🌤️ WeatherStack        │                                   │<br>
│  🤖 Gemini              │  👤 What is the weather in Dhaka?│<br>
│                          │                                   │<br>
│  🗑️ Clear Conversation  │  🤖 The current weather in Dhaka  │<br>
│                          │     is ...                        │<br>
│                          │                                   │<br>
│                          │  ┌──────────────────────────────┐ │<br>
│                          │  │ Ask me anything...           │ │<br>
│                          │  └──────────────────────────────┘ │<br>
└──────────────────────────────────────────────────────────────┘<br>
