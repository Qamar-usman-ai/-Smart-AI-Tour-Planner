import streamlit as st
import aisuite as ai
import os
from typing import Optional

# Configuration - make these mutable by using a config dictionary
CONFIG = {
    "MODEL_NAME": "groq:llama-3.1-8b-instant",
    "TEMPERATURE": 0.7,
    "MAX_TOKENS_RESEARCH": 500,
    "MAX_TOKENS_WRITER": 300
}

class TwoAgentFlow:
    def __init__(self, api_key: Optional[str] = None, temperature: float = 0.7, 
                 max_tokens_research: int = 500, max_tokens_writer: int = 300):
        """Initialize the two-agent flow with Groq API key."""
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
        
        if not os.environ.get("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY is not set. Please provide your API key.")
        
        self.client = ai.Client()
        self.temperature = temperature
        self.max_tokens_research = max_tokens_research
        self.max_tokens_writer = max_tokens_writer
        self.model_name = CONFIG["MODEL_NAME"]
    
    def research_agent(self, topic: str) -> str:
        """Agent 1: Research agent that gathers raw data."""
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
                model=self.model_name,
                messages=research_prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens_research
            )
            
            raw_data = response.choices[0].message.content
            return raw_data
            
        except Exception as e:
            st.error(f"❌ Research agent failed: {str(e)}")
            raise
    
    def writer_agent(self, raw_data: str) -> str:
        """Agent 2: Writer agent that creates final output."""
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
                model=self.model_name,
                messages=writer_prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens_writer
            )
            
            final_output = response.choices[0].message.content
            return final_output
            
        except Exception as e:
            st.error(f"❌ Writer agent failed: {str(e)}")
            raise
    
    def run(self, topic: str) -> dict:
        """Run the complete two-agent workflow."""
        try:
            # Step 1: Research
            raw_data = self.research_agent(topic)
            
            # Step 2: Write final report
            final_output = self.writer_agent(raw_data)
            
            return {
                "success": True,
                "raw_data": raw_data,
                "final_output": final_output
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Page configuration
st.set_page_config(
    page_title="Two-Agent AI Workflow",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff6b6b;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e7f3ff;
        border: 1px solid #b8daff;
        margin-bottom: 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 Two-Agent AI Workflow Assistant")
st.markdown("""
<div class="info-box">
    <b>How it works:</b><br>
    1️⃣ <b>Research Agent</b> - Gathers factual information and provides raw data<br>
    2️⃣ <b>Writer Agent</b> - Transforms raw data into a friendly, engaging summary<br>
    <br>
    <b>Powered by:</b> Groq's Llama 3.1 8B model
</div>
""", unsafe_allow_html=True)

# Sidebar for API configuration
with st.sidebar:
    st.header("🔐 Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter your Groq API key",
        help="Get your API key from https://console.groq.com/keys"
    )
    
    st.markdown("---")
    
    # Model configuration
    st.subheader("⚙️ Model Settings")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )
    
    max_tokens_research = st.number_input(
        "Max Tokens (Research)",
        min_value=100,
        max_value=1000,
        value=500,
        step=50,
        help="Maximum tokens for research agent response"
    )
    
    max_tokens_writer = st.number_input(
        "Max Tokens (Writer)",
        min_value=100,
        max_value=500,
        value=300,
        step=50,
        help="Maximum tokens for writer agent response"
    )
    
    st.markdown("---")
    st.markdown("""
    <small>
    <b>Tips:</b><br>
    • Use a valid Groq API key<br>
    • Start with simple topics<br>
    • Adjust temperature for creativity
    </small>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Topic to Research")
    topic = st.text_area(
        "Enter your topic:",
        placeholder="e.g., The future of Mars colonization, Impact of AI on healthcare, Renewable energy trends...",
        height=100,
        value="The future of Mars colonization"
    )
    
    # Run button
    run_button = st.button("🚀 Run Two-Agent Workflow", type="primary", use_container_width=True)

with col2:
    st.subheader("ℹ️ Example Topics")
    example_topics = [
        "The future of renewable energy",
        "Impact of quantum computing",
        "Sustainable agriculture practices",
        "Future of remote work",
        "AI in education"
    ]
    for example in example_topics:
        if st.button(f"📌 {example}", key=example, use_container_width=True):
            topic = example
            st.rerun()

# Session state to store results
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""

# Process the workflow
if run_button and topic:
    if not api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar")
    else:
        st.session_state.processing = True
        st.session_state.workflow_results = None
        st.session_state.current_topic = topic
        
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize workflow with dynamic parameters
            status_text.text("🔄 Initializing workflow...")
            progress_bar.progress(10)
            
            workflow = TwoAgentFlow(
                api_key=api_key,
                temperature=temperature,
                max_tokens_research=max_tokens_research,
                max_tokens_writer=max_tokens_writer
            )
            
            # Run the workflow
            status_text.text("🔍 Research Agent is gathering information...")
            progress_bar.progress(30)
            
            # Create placeholder for real-time updates
            research_placeholder = st.empty()
            writer_placeholder = st.empty()
            
            # Research phase
            with st.spinner("Researching..."):
                raw_data = workflow.research_agent(topic)
                research_placeholder.markdown("""
                <div class="success-message">
                    ✅ <b>Research Complete!</b>
                </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(60)
            
            status_text.text("✍️ Writer Agent is creating the final report...")
            
            # Writing phase
            with st.spinner("Writing..."):
                final_output = workflow.writer_agent(raw_data)
                writer_placeholder.markdown("""
                <div class="success-message">
                    ✅ <b>Writing Complete!</b>
                </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(90)
            
            # Store results
            st.session_state.workflow_results = {
                "success": True,
                "raw_data": raw_data,
                "final_output": final_output,
                "topic": topic,
                "temperature": temperature,
                "max_tokens_research": max_tokens_research,
                "max_tokens_writer": max_tokens_writer
            }
            
            progress_bar.progress(100)
            status_text.text("✅ Workflow completed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.workflow_results = {
                "success": False,
                "error": str(e),
                "topic": topic
            }
        
        finally:
            st.session_state.processing = False

# Display results
if st.session_state.workflow_results and not st.session_state.processing:
    results = st.session_state.workflow_results
    
    if results["success"]:
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📄 Final Summary", "🔍 Raw Research Data", "📊 Workflow Info"])
        
        with tab1:
            st.markdown("### 📝 Final Report")
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #ff4b4b;">
                {results["final_output"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Copy button functionality with JavaScript
            st.markdown("""
            <script>
            function copyToClipboard() {
                const text = document.querySelector('.final-report').innerText;
                navigator.clipboard.writeText(text);
            }
            </script>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy to Clipboard"):
                    st.info("Copied to clipboard! (Note: Copy manually in web interface)")
            with col2:
                st.download_button(
                    label="💾 Download Summary",
                    data=results["final_output"],
                    file_name=f"{results['topic'].replace(' ', '_')}_summary.txt",
                    mime="text/plain"
                )
        
        with tab2:
            st.markdown("### 🔍 Research Data")
            st.code(results["raw_data"], language="markdown")
            
            # Download button for raw data
            st.download_button(
                label="💾 Download Raw Data",
                data=results["raw_data"],
                file_name=f"{results['topic'].replace(' ', '_')}_research.txt",
                mime="text/plain"
            )
        
        with tab3:
            st.markdown("### 📊 Workflow Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Model Used", CONFIG["MODEL_NAME"])
                st.metric("Temperature", results["temperature"])
            with col2:
                st.metric("Research Tokens", results["max_tokens_research"])
                st.metric("Writer Tokens", results["max_tokens_writer"])
            with col3:
                st.metric("Status", "✅ Completed")
            
            st.markdown("#### Topic Analyzed")
            st.info(results["topic"])
    
    else:
        st.error(f"❌ Workflow failed: {results['error']}")
        
        # Show troubleshooting tips
        with st.expander("🔧 Troubleshooting Tips"):
            st.markdown("""
            **Common issues and solutions:**
            1. **Invalid API Key**: Make sure your Groq API key is correct and active
            2. **Network Issues**: Check your internet connection
            3. **Rate Limits**: You might have exceeded API rate limits, wait a moment and try again
            4. **Topic Too Complex**: Try a simpler topic first
            5. **Token Limits**: Adjust max tokens in sidebar if responses are being truncated
            
            **Get help:**
            - Get API key: https://console.groq.com/keys
            - Check Groq status: https://status.groq.com
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>🤖 Powered by Groq's Llama 3.1 8B | Two-Agent Architecture</small>
</div>
""", unsafe_allow_html=True)

# Clear results button
if st.session_state.workflow_results:
    if st.button("🔄 Clear Results & Start Over", use_container_width=True):
        st.session_state.workflow_results = None
        st.session_state.processing = False
        st.rerun()
