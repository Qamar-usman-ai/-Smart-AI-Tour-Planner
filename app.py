import aisuite as ai
import os
from typing import Optional

# Configuration
MODEL_NAME = "groq:llama-3.1-8b-instant"
TEMPERATURE = 0.7

class TwoAgentFlow:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the two-agent flow with Groq API key."""
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
        
        if not os.environ.get("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY is not set. Please provide your API key.")
        
        self.client = ai.Client()
    
    def research_agent(self, topic: str) -> str:
        """Agent 1: Research agent that gathers raw data."""
        print("🕵️ Agent 1 is researching...")
        
        research_prompt = [
            {
                "role": "system", 
                "content": "You are a factual researcher. Provide 3 bullet points of raw data. Be concise and factual."
            },
            {
                "role": "user", 
                "content": f"Research this topic: {topic}"
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=research_prompt,
                temperature=TEMPERATURE,
                max_tokens=500
            )
            
            raw_data = response.choices[0].message.content
            print("✅ Research Complete.\n")
            return raw_data
            
        except Exception as e:
            print(f"❌ Research agent failed: {str(e)}")
            raise
    
    def writer_agent(self, raw_data: str) -> str:
        """Agent 2: Writer agent that creates final output."""
        print("✍️ Agent 2 is writing the final report...")
        
        writer_prompt = [
            {
                "role": "system", 
                "content": "You are a professional editor. Turn raw data into a friendly 1-paragraph summary. Keep it engaging and clear."
            },
            {
                "role": "user", 
                "content": f"Here is the research data:\n{raw_data}"
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=writer_prompt,
                temperature=TEMPERATURE,
                max_tokens=300
            )
            
            final_output = response.choices[0].message.content
            print("✅ Writing Complete.\n")
            return final_output
            
        except Exception as e:
            print(f"❌ Writer agent failed: {str(e)}")
            raise
    
    def run(self, topic: str) -> str:
        """Run the complete two-agent workflow."""
        try:
            print(f"🚀 Starting workflow for: {topic}\n")
            
            # Step 1: Research
            raw_data = self.research_agent(topic)
            
            # Optional: Show raw data for debugging
            print("📊 Raw Research Data:")
            print("-" * 40)
            print(raw_data)
            print("-" * 40 + "\n")
            
            # Step 2: Write final report
            final_output = self.writer_agent(raw_data)
            
            return final_output
            
        except Exception as e:
            error_msg = f"Workflow failed: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg

# ▶️ Run the flow
if __name__ == "__main__":
    # Option 1: Set API key in code (not recommended for production)
    # API_KEY = "your_groq_api_key_here"
    
    # Option 2: Use environment variable (recommended)
    API_KEY = os.environ.get("GROQ_API_KEY")
    
    if not API_KEY:
        print("⚠️  Please set your GROQ_API_KEY environment variable")
        print("Example: export GROQ_API_KEY='your_key_here'")
        print("Or get one from: https://console.groq.com/keys")
        print("\nTrying to run with existing environment variable...")
    
    try:
        # Create and run the workflow
        workflow = TwoAgentFlow(api_key=API_KEY)
        result = workflow.run("The future of Mars colonization")
        
        print("\n" + "="*50)
        print("FINAL OUTPUT")
        print("="*50)
        print(result)
        print("="*50)
        
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
