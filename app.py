import aisuite as ai
import os

# 🔐 Set your API key (Groq)
os.environ["GROQ_API_KEY"] = "your_groq_api_key"

client = ai.Client()

def run_two_agent_flow(topic):
    print(f"🚀 Starting workflow for: {topic}\n")

    # --- AGENT 1: Researcher ---
    print("🕵️ Agent 1 is researching...")

    research_prompt = [
        {"role": "system", "content": "You are a factual researcher. Provide 3 bullet points of raw data."},
        {"role": "user", "content": f"Research this topic: {topic}"}
    ]

    research_res = client.chat.completions.create(
        model="groq:llama-3.1-8b-instant",
        messages=research_prompt,
        temperature=0.7
    )

    raw_data = research_res.choices[0].message.content
    print("✅ Research Complete.\n")

    # --- AGENT 2: Writer ---
    print("✍️ Agent 2 is writing the final report...")

    writer_prompt = [
        {"role": "system", "content": "You are a professional editor. Turn raw data into a friendly 1-paragraph summary."},
        {"role": "user", "content": f"Here is the research data:\n{raw_data}"}
    ]

    writer_res = client.chat.completions.create(
        model="groq:llama-3.1-8b-instant",
        messages=writer_prompt,
        temperature=0.7
    )

    final_output = writer_res.choices[0].message.content

    return final_output


# ▶️ Run the flow
if __name__ == "__main__":
    result = run_two_agent_flow("The future of Mars colonization")
    print("\n--- FINAL OUTPUT ---\n")
    print(result)
