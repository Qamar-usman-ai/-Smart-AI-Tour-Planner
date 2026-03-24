import streamlit as st
import aisuite as ai
import requests
import json
import os
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta

# Configuration
AVAILABLE_MODELS = {
    "Grok (xAI)": "grok:grok-2-latest",
    "GPT-4o (OpenAI)": "openai:gpt-4o",
    "Gemini 1.5 Pro (Google)": "google:gemini-1.5-pro"
}

class SmartTourPlanner:
    """Agentic AI Tour Planner with tool calling capabilities"""
    
    def __init__(self, api_keys: Dict[str, str], model: str = "grok:grok-2-latest"):
        """Initialize the tour planner with API keys and model"""
        self.api_keys = api_keys
        self.model = model
        
        # Set environment variables for AISuite
        if model.startswith("openai:"):
            os.environ["OPENAI_API_KEY"] = api_keys.get("openai", "")
        elif model.startswith("google:"):
            os.environ["GOOGLE_API_KEY"] = api_keys.get("google", "")
        elif model.startswith("grok:"):
            os.environ["GROQ_API_KEY"] = api_keys.get("grok", "")
        
        self.client = ai.Client()
        self.tools = self._define_tools()
    
    def _define_tools(self) -> List[Dict]:
        """Define tools available for the agent"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather and forecast for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city name to get weather for"
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days for forecast (1-5)",
                                "default": 3
                            }
                        },
                        "required": ["city"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_restaurants",
                    "description": "Find top restaurants in a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City or area to search for restaurants"
                            },
                            "radius": {
                                "type": "integer",
                                "description": "Search radius in meters",
                                "default": 5000
                            },
                            "cuisine": {
                                "type": "string",
                                "description": "Type of cuisine (optional)",
                                "default": ""
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_attractions",
                    "description": "Find top tourist attractions in a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "City to find attractions in"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of attractions to return",
                                "default": 5
                            }
                        },
                        "required": ["city"]
                    }
                }
            }
        ]
    
    def get_weather(self, city: str, days: int = 3) -> Dict:
        """Fetch weather data from OpenWeatherMap API"""
        try:
            api_key = self.api_keys.get("openweather")
            if not api_key:
                return {"error": "OpenWeatherMap API key not configured"}
            
            # Get coordinates first
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            geo_response = requests.get(geo_url)
            
            if geo_response.status_code != 200:
                return {"error": f"Could not find city: {city}"}
            
            geo_data = geo_response.json()
            if not geo_data:
                return {"error": f"City '{city}' not found"}
            
            lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
            
            # Get weather data
            weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"
            weather_response = requests.get(weather_url)
            
            if weather_response.status_code != 200:
                return {"error": "Failed to fetch weather data"}
            
            weather_data = weather_response.json()
            
            # Process forecast data
            forecast = []
            seen_dates = set()
            
            for item in weather_data["list"]:
                date = item["dt_txt"].split()[0]
                if date not in seen_dates and len(forecast) < days:
                    seen_dates.add(date)
                    forecast.append({
                        "date": date,
                        "temp": round(item["main"]["temp"], 1),
                        "description": item["weather"][0]["description"],
                        "humidity": item["main"]["humidity"],
                        "wind_speed": item["wind"]["speed"]
                    })
            
            return {
                "city": city,
                "current": forecast[0] if forecast else None,
                "forecast": forecast[1:] if len(forecast) > 1 else []
            }
            
        except Exception as e:
            return {"error": f"Weather API error: {str(e)}"}
    
    def find_restaurants(self, location: str, radius: int = 5000, cuisine: str = "") -> Dict:
        """Find restaurants using Google Places API"""
        try:
            api_key = self.api_keys.get("google_maps")
            if not api_key:
                return {"error": "Google Maps API key not configured"}
            
            # First, geocode the location
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
            geocode_response = requests.get(geocode_url)
            
            if geocode_response.status_code != 200:
                return {"error": "Failed to geocode location"}
            
            geocode_data = geocode_response.json()
            if not geocode_data.get("results"):
                return {"error": f"Location '{location}' not found"}
            
            lat = geocode_data["results"][0]["geometry"]["location"]["lat"]
            lng = geocode_data["results"][0]["geometry"]["location"]["lng"]
            
            # Search for restaurants
            search_query = f"restaurants in {location}"
            if cuisine:
                search_query = f"{cuisine} restaurants in {location}"
            
            places_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_query}&location={lat},{lng}&radius={radius}&key={api_key}"
            places_response = requests.get(places_url)
            
            if places_response.status_code != 200:
                return {"error": "Failed to fetch restaurants"}
            
            places_data = places_response.json()
            
            restaurants = []
            for place in places_data.get("results", [])[:10]:
                restaurants.append({
                    "name": place.get("name"),
                    "rating": place.get("rating", "N/A"),
                    "total_ratings": place.get("user_ratings_total", 0),
                    "address": place.get("formatted_address", place.get("vicinity", "Address not available")),
                    "price_level": "💲" * place.get("price_level", 1) if place.get("price_level") else "Not specified"
                })
            
            return {
                "location": location,
                "restaurants": restaurants,
                "total_found": len(restaurants)
            }
            
        except Exception as e:
            return {"error": f"Places API error: {str(e)}"}
    
    def get_attractions(self, city: str, limit: int = 5) -> Dict:
        """Find top attractions using Google Places API"""
        try:
            api_key = self.api_keys.get("google_maps")
            if not api_key:
                return {"error": "Google Maps API key not configured"}
            
            # Search for tourist attractions
            search_query = f"tourist attractions in {city}"
            
            places_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_query}&key={api_key}"
            places_response = requests.get(places_url)
            
            if places_response.status_code != 200:
                return {"error": "Failed to fetch attractions"}
            
            places_data = places_response.json()
            
            attractions = []
            for place in places_data.get("results", [])[:limit]:
                attractions.append({
                    "name": place.get("name"),
                    "rating": place.get("rating", "N/A"),
                    "total_ratings": place.get("user_ratings_total", 0),
                    "address": place.get("formatted_address", place.get("vicinity", "Address not available")),
                    "types": ", ".join(place.get("types", [])[:3])
                })
            
            return {
                "city": city,
                "attractions": attractions,
                "total_found": len(attractions)
            }
            
        except Exception as e:
            return {"error": f"Places API error: {str(e)}"}
    
    def execute_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """Execute a tool based on name and arguments"""
        if tool_name == "get_weather":
            return self.get_weather(**arguments)
        elif tool_name == "find_restaurants":
            return self.find_restaurants(**arguments)
        elif tool_name == "get_attractions":
            return self.get_attractions(**arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def plan_trip(self, destination: str, max_turns: int = 5) -> Dict:
        """Main agentic loop for trip planning"""
        
        messages = [
            {
                "role": "system",
                "content": """You are a smart AI tour planner. Your task is to create a comprehensive travel itinerary.
                
                You have access to these tools:
                1. get_weather - Get current weather and forecast
                2. find_restaurants - Find top restaurants
                3. get_attractions - Find tourist attractions
                
                Guidelines:
                - First, gather weather information to advise on suitable activities
                - Then, find attractions and restaurants
                - Create a day-by-day itinerary
                - Consider weather conditions when suggesting activities
                - Provide practical tips like what to pack, best times to visit
                - Be engaging and helpful
                
                Always call tools to get real data before making recommendations.
                Create a complete, actionable travel plan."""
            },
            {
                "role": "user",
                "content": f"Create a detailed travel plan for {destination}. Include weather considerations, top attractions, and restaurant recommendations."
            }
        ]
        
        turns_used = 0
        tool_results = []
        
        while turns_used < max_turns:
            try:
                # Call the LLM
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto",
                    temperature=0.7
                )
                
                message = response.choices[0].message
                messages.append(message)
                
                # Check for tool calls
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        tool_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)
                        
                        # Execute tool
                        result = self.execute_tool(tool_name, arguments)
                        tool_results.append({
                            "tool": tool_name,
                            "arguments": arguments,
                            "result": result
                        })
                        
                        # Add tool result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result, indent=2)
                        })
                    
                    turns_used += 1
                else:
                    # No more tool calls, we have the final response
                    return {
                        "success": True,
                        "plan": message.content,
                        "tool_results": tool_results,
                        "turns_used": turns_used
                    }
                    
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "turns_used": turns_used
                }
        
        # Max turns reached
        return {
            "success": False,
            "error": "Maximum tool call turns reached",
            "turns_used": turns_used,
            "partial_result": messages[-1].content if messages else None
        }

# Streamlit UI
st.set_page_config(
    page_title="Smart AI Tour Planner",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 1rem;
    }
    .tool-result {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 2rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        color: white;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #e7f3ff;
        border: 1px solid #b8daff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌍 Smart AI Tour Planner</h1>
    <p>Multi-LLM Agentic Travel Assistant with Real-Time Data</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔐 API Configuration")
    st.markdown("Your API keys are session-only and never stored")
    
    # Model selection
    st.subheader("🤖 Model Selection")
    selected_model_name = st.selectbox(
        "Choose LLM",
        options=list(AVAILABLE_MODELS.keys()),
        help="Select which AI model to use for trip planning"
    )
    selected_model = AVAILABLE_MODELS[selected_model_name]
    
    st.markdown("---")
    
    # API Keys
    st.subheader("🔑 API Keys")
    grok_key = st.text_input(
        "Grok (xAI) API Key",
        type="password",
        placeholder="Enter your Grok API key",
        help="Get from https://console.x.ai"
    )
    
    openai_key = st.text_input(
        "OpenAI API Key (for GPT-4o)",
        type="password",
        placeholder="Enter your OpenAI API key",
        help="Get from https://platform.openai.com/api-keys"
    )
    
    google_key = st.text_input(
        "Google API Key",
        type="password",
        placeholder="Enter your Google API key",
        help="Enable Places API and Geocoding API"
    )
    
    weather_key = st.text_input(
        "OpenWeatherMap API Key",
        type="password",
        placeholder="Enter your OpenWeatherMap API key",
        help="Get from https://openweathermap.org/api"
    )
    
    st.markdown("---")
    
    # Additional settings
    st.subheader("⚙️ Settings")
    max_turns = st.slider(
        "Max Agent Turns",
        min_value=1,
        max_value=10,
        value=5,
        help="Maximum number of tool call rounds"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.9em;">
        <b>✨ Features:</b><br>
        • Multi-LLM Support<br>
        • Live Weather Data<br>
        • Restaurant Discovery<br>
        • Attraction Finder<br>
        • Agentic Tool Use<br>
    </div>
    """, unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✈️ Plan Your Trip")
    destination = st.text_input(
        "Where would you like to go?",
        placeholder="e.g., Paris, France",
        help="Enter any city or destination"
    )
    
    plan_button = st.button("🎯 Plan My Trip!", use_container_width=True)

with col2:
    st.subheader("📌 Quick Examples")
    example_destinations = [
        "Paris, France",
        "Tokyo, Japan",
        "New York, USA",
        "Barcelona, Spain",
        "Bali, Indonesia"
    ]
    for example in example_destinations:
        if st.button(f"📍 {example}", key=example, use_container_width=True):
            destination = example
            st.rerun()

# Session state
if 'trip_plan' not in st.session_state:
    st.session_state.trip_plan = None
if 'planning' not in st.session_state:
    st.session_state.planning = False
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = None

# Process the trip plan
if plan_button and destination:
    # Validate API keys based on selected model
    api_keys = {
        "openai": openai_key,
        "google": google_key,
        "grok": grok_key,
        "openweather": weather_key
    }
    
    # Check if required API key is present
    if selected_model.startswith("openai:") and not openai_key:
        st.error("⚠️ Please enter your OpenAI API key for GPT-4o")
    elif selected_model.startswith("google:") and not google_key:
        st.error("⚠️ Please enter your Google API key for Gemini")
    elif selected_model.startswith("grok:") and not grok_key:
        st.error("⚠️ Please enter your Grok API key")
    elif not weather_key:
        st.error("⚠️ Please enter your OpenWeatherMap API key")
    elif not google_key:
        st.error("⚠️ Please enter your Google API key (required for Places API)")
    else:
        st.session_state.planning = True
        st.session_state.trip_plan = None
        
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize planner
            status_text.text("🚀 Initializing AI agent...")
            progress_bar.progress(10)
            
            planner = SmartTourPlanner(
                api_keys=api_keys,
                model=selected_model
            )
            
            # Plan the trip
            status_text.text(f"🤖 Agent is planning your trip to {destination}...")
            progress_bar.progress(30)
            
            result = planner.plan_trip(destination, max_turns=max_turns)
            
            progress_bar.progress(100)
            status_text.text("✅ Trip planning completed!")
            
            if result["success"]:
                st.session_state.trip_plan = result["plan"]
                st.session_state.debug_info = result.get("tool_results", [])
            else:
                st.error(f"❌ Planning failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.debug_info = None
        
        finally:
            st.session_state.planning = False

# Display results
if st.session_state.trip_plan:
    # Success message
    st.markdown(f"""
    <div class="success-box">
        ✅ <b>Your {destination} Travel Plan is Ready!</b><br>
        Planned using: {selected_model_name}
    </div>
    """, unsafe_allow_html=True)
    
    # Display the plan
    st.markdown("### 📋 Your Personalized Itinerary")
    st.markdown(st.session_state.trip_plan)
    
    # Download button
    st.download_button(
        label="💾 Download Travel Plan",
        data=st.session_state.trip_plan,
        file_name=f"{destination.replace(' ', '_')}_travel_plan.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    # Debug information (expandable)
    if st.session_state.debug_info:
        with st.expander("🔧 Tool Calls (Debug Info)"):
            for idx, tool_call in enumerate(st.session_state.debug_info, 1):
                st.markdown(f"**Call {idx}: {tool_call['tool']}**")
                st.json(tool_call["arguments"])
                st.markdown("**Result:**")
                st.json(tool_call["result"])
                st.markdown("---")

# Features explanation
st.markdown("---")
st.markdown("### ✨ Features")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <b>🤖 Multi-LLM Support</b><br>
        Choose between Grok, GPT-4o, or Gemini
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <b>🌤️ Live Weather</b><br>
        Real-time forecasts via OpenWeatherMap
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <b>🍽️ Restaurant Discovery</b><br>
        Top eateries from Google Places
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <b>🔄 Agentic Tool Use</b><br>
        AI autonomously calls APIs
    </div>
    """, unsafe_allow_html=True)

# How it works
with st.expander("📖 How It Works"):
    st.markdown("""
    ### The Agentic Workflow
    
    1. **User Input** → Enter destination and select model
    2. **Agent Invocation** → LLM receives task with tool definitions
    3. **Tool Calls** → AI autonomously decides to:
       - Check weather conditions
       - Find top restaurants
       - Discover attractions
    4. **Data Fetching** → Tools call real APIs
    5. **Plan Generation** → LLM synthesizes all data into complete itinerary
    
    ### Tech Stack
    - **UI**: Streamlit
    - **LLM Orchestration**: AISuite
    - **Weather**: OpenWeatherMap API
    - **Places**: Google Maps Places API
    - **Models**: Grok, GPT-4o, Gemini 1.5 Pro
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>🌍 Smart AI Tour Planner | Powered by Multi-LLM Agentic Architecture</small>
</div>
""", unsafe_allow_html=True)
