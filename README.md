# langchain-tavily-weather-agent
An AI-powered weather and search agent built with LangChain, leveraging Gemini LLM, Tavily Search, and WeatherStack tools for real-time weather and general web insights.

#Installation & Setup Instructions
#Follow these steps to install and run the application.

1. Download the Required Files
Download the following files and place them in the same directory/folder:
app.py
requirements.txt

2. Install Required Packages
Open Bash / Terminal in the project directory and run:
pip install -r requirements.txt

3. Create the .env File
Create a new file named .env in the same directory as app.py.
Add your API keys:
GEMENI_API_KEY="your_gemini_api_key"
TAVILY_API_KEY="your_tavily_api_key"
WEATHERSTACK_API_KEY="your_weatherstack_api_key"
Replace the placeholder values with your actual API keys.
Important: Keep your API keys private. Do not upload the .env file to GitHub or share it publicly.


4. Run the Application
Open Bash / Terminal in the project directory and run:
streamlit run app.py
The application will start and Streamlit will provide a local URL, usually:
http://localhost:8501
Open that URL in your web browser to use the application


#UI Structure
┌──────────────────────────────────────────────────────────────┐

│  ⚙️ CONFIGURATION        │  🌤️ AI Weather Agent             │

│                          │                                   │

│  API STATUS              │  Ask questions about cities,     │
│  ✅ Gemini               │  weather and current information │
│  ✅ Tavily               │                                   │
│  ✅ WeatherStack         │  ┌────────┐ ┌────────┐ ┌────────┐│
│                          │  │Weather │ │ Search │ │  AI    ││
│  TOOLS                   │  │  🌤️   │ │  🔎   │ │  🤖   ││
│  🔎 Tavily Search        │  └────────┘ └────────┘ └────────┘│
│  🌤️ WeatherStack        │                                   │
│  🤖 Gemini              │  👤 What is the weather in Dhaka?│
│                          │                                   │
│  🗑️ Clear Conversation  │  🤖 The current weather in Dhaka │
│                          │     is ...                        │
│                          │                                   │
│                          │  ┌──────────────────────────────┐ │
│                          │  │ Ask me anything...           │ │
│                          │  └──────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
