import streamlit as st
import json
import time
from snowflake.snowpark.functions import ai_complete

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Cached LLM Function
@st.cache_data
def call_cortex_llm(prompt_text):
    """Makes a call to Cortex AI with the given prompt."""
    model = "claude-3-5-sonnet"
    df = session.range(1).select(
        ai_complete(model=model, prompt=prompt_text).alias("response")
    )
    
    # Get and parse response
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    return response_json

# --- App UI ---

# Input widgets
st.subheader(":material/input: Input content")
content = st.text_input("Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")

with st.sidebar:
    st.title(":material/post: Add some flair to your data")
    st.success("An app for generating a sonnet post using the input text as inspiration.")
    tone = st.selectbox("Tone:", ["Romantic", "Tragic", "Witty"])
    word_count = st.slider("Approximate word count:", 50, 300, 100)

# Generate button
if st.button("Generate Poem"):
    
    # Initialize the status container
    with st.status("Starting engine...", expanded=True) as status:
        
        # Step 1: Construct Prompt
        st.write(":material/psychology: Thinking: Analyzing constraints and tone...")

        # Add a slight delay
        time.sleep(2)
        
        prompt = f"""
        You are a poet with fire in your heart. Generate a sonnet based on the following:

        Tone: {tone}
        Desired Length: Approximately {word_count} words
        Use content from this input: {content}

        Generate only the text and format it accordingly.
        """
        
        # Step 2: Call API
        st.write(":material/flash_on: Generating: contacting Snowflake Cortex...")

        # Add a slight delay
        time.sleep(2)
        
        # This is the blocking call that takes time
        response = call_cortex_llm(prompt)
        
        # Step 3: Update Status to Complete
        st.write(":material/check_circle: Poem generation completed!")
        status.update(label="Poem Generated Successfully!", state="complete", expanded=False)

    # Display Result
    with st.container(border=True):
        st.subheader(":material/output: Generated poem:")
        st.markdown(response)