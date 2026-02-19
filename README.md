<div align="center">

# 🌍 Smart AI Tour Planner

**An agentic travel assistant that combines real-time weather, restaurant discovery,**  
**and multi-LLM power to craft personalized trip itineraries — all in your browser.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![AISuite](https://img.shields.io/badge/AISuite-Multi--LLM-8B5CF6?style=for-the-badge)](https://github.com/andrewyng/aisuite)
[![License: MIT](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)

</div>

---

## ✨ Features

| | Feature | Description |
|---|---|---|
| 🤖 | **Multi-LLM Support** | Choose between Grok (xAI), GPT-4o, or Gemini 1.5 Pro |
| 🌤️ | **Live Weather Forecasts** | Real-time weather data via OpenWeatherMap API |
| 🍽️ | **Restaurant Discovery** | Top nearby restaurants via Google Maps Places API |
| 🔄 | **Agentic Tool Use** | LLM autonomously calls tools — up to 5 turns |
| 🔒 | **Secure Key Handling** | Keys are session-only and never stored |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| UI Framework | [Streamlit](https://streamlit.io/) |
| LLM Orchestration | [AISuite](https://github.com/andrewyng/aisuite) |
| Weather Data | [OpenWeatherMap API](https://openweathermap.org/api) |
| Places Data | [Google Maps Places API](https://developers.google.com/maps/documentation/places/web-service) |
| Language Models | xAI Grok-2 · OpenAI GPT-4o · Google Gemini 1.5 Pro |

---

## 📋 Prerequisites

- **Python 3.9+**
- API keys for:
  - [xAI (Grok)](https://console.x.ai/) — or OpenAI / Google depending on your model choice
  - [OpenWeatherMap](https://home.openweathermap.org/api_keys) — free tier is sufficient
  - [Google Maps Platform](https://console.cloud.google.com/) — with Places API enabled

---

## 🚀 Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/your-username/smart-ai-tour-planner.git
cd smart-ai-tour-planner
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

> ⚠️ **Note:** AISuite requires provider-specific packages. Install based on your chosen model:
> ```bash
> pip install openai              # for GPT-4o
> pip install google-generativeai # for Gemini
> pip install anthropic           # for Claude
> ```

**3. Run the app**

```bash
streamlit run app.py
```

**4. Enter your API keys**

Once the app opens in your browser, enter your **Grok**, **OpenWeatherMap**, and **Google Maps** API keys in the sidebar — then type a destination and click **Plan My Trip**!

---

## 📦 Requirements

`requirements.txt`:

```
streamlit
aisuite
requests
```

---

## 📁 Project Structure

```
smart-ai-tour-planner/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ How It Works

The app follows a simple **agentic loop**:

```
User Input  →  Agent Invocation  →  Tool Calls  →  Data Fetching  →  Plan Output
```

1. **User Input** — Enter a destination and select an LLM model from the sidebar
2. **Agent Invocation** — AISuite sends the request to the chosen LLM with tool definitions
3. **Tool Calls** — The LLM autonomously decides when to call `get_weather` and `find_restaurants`
4. **Data Fetching** — Tools hit the OpenWeatherMap and Google Maps APIs in real time
5. **Plan Generation** — The LLM synthesizes all data into a complete, readable itinerary

---

## 🧩 Extending the App

Add more tools by defining new Python functions and including them in the `tools` list:

```python
def find_hotels(location: str):
    # Call a hotels API here
    ...

response = client.chat.completions.create(
    model=selected_model,
    messages=messages,
    tools=[get_weather, find_restaurants, find_hotels],  # ← Add here
    max_turns=5
)
```

---

## 🔒 Privacy & Security

> 🛡️ API keys are entered as `type="password"` inputs — masked in the UI, stored **only** in `os.environ` for the duration of the session, and **never persisted** to disk or any external service. No user data or trip plans are logged.

---

## ⚠️ Known Limitations

- Weather forecast is simplified to the first **3 time slots** from the 5-day OpenWeatherMap endpoint
- Restaurant results are limited to the **top 3** from the Google Places text search query
- Mismatched API keys and model selection will cause runtime errors — ensure keys match your chosen model

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [**AISuite** by Andrew Ng](https://github.com/andrewyng/aisuite) — unified LLM interface that powers multi-model support
- [**Streamlit**](https://streamlit.io/) — making Python web apps effortlessly beautiful
- [**OpenWeatherMap**](https://openweathermap.org/) & [**Google Maps Platform**](https://developers.google.com/maps) — real-time data APIs

---

<div align="center">

Built with ❤️ using [Streamlit](https://streamlit.io) · [AISuite](https://github.com/andrewyng/aisuite) · [OpenWeatherMap](https://openweathermap.org) · [Google Maps](https://developers.google.com/maps)

</div>
