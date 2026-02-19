import aisuite as ai
import os

# 1. Setup your API Keys
os.environ["XAI_API_KEY"] = "your-grok-key"
os.environ["GOOGLE_API_KEY"] = "your-gemini-key"

client = ai.Client()

def run_two_agent_flow(topic):
    print(f"🚀 Starting workflow for: {topic}\n")

    # --- AGENT 1: The Researcher (using Grok) ---
    print("🕵️ Agent 1 (Grok) is researching...")
    research_prompt = [
        {"role": "system", "content": "You are a factual researcher. Provide 3 bullet points of raw data."},
        {"role": "user", "content": f"Research this topic: {topic}"}
    ]
    
    research_res = client.chat.completions.create(
        model="xai:grok-2",
        messages=research_prompt
    )
    raw_data = research_res.choices[0].message.content
    print(f"✅ Research Complete.\n")

    # --- AGENT 2: The Writer (using Gemini) ---
    print("✍️ Agent 2 (Gemini) is writing the final report...")
    writer_prompt = [
        {"role": "system", "content": "You are a professional editor. Turn raw data into a friendly 1-paragraph summary."},
        {"role": "user", "content": f"Here is the research data: {raw_data}"}
    ]
    
    writer_res = client.chat.completions.create(
        model="google:gemini-1.5-pro",
        messages=writer_prompt
    )
    final_output = writer_res.choices[0].message.content

    return final_output

# Run the flow
result = run_two_agent_flow("The future of Mars colonization")
print("--- FINAL OUTPUT ---")
print(result)
