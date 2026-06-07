import streamlit as st
import re  # 1. Import the regular expressions library
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq

# Load environment variables
_ = load_dotenv(find_dotenv())

# Initialize the LLM
llm = ChatGroq(model="qwen/qwen3-32b")

# 2. Create a quick helper function to clean the AI's output
def remove_think_tags(text):
    """Removes the <think>...</think> blocks from the text."""
    # This regex looks for <think>, anything in between, and </think>, then replaces it with nothing.
    clean = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return clean.strip()

# --- FRONTEND UI DESIGN ---
st.title("🩸 Blood Work Analyzer & Diet Planner")
st.write("Paste your medical report below to get a 50-word summary and a tailored Indian diet plan.")

user_report = st.text_area("Blood Work Report:", height=200, placeholder="Paste the text here...")

if st.button("Analyze Report"):
    if user_report.strip() == "":
        st.error("Please enter a report first!")
    else:
        with st.spinner("Analyzing data and generating diet plan..."):
            
            # Agent 1: Summarize
            prompt_1 = [
                ("system", "You are a professional highly trained physician that gives accurate summary of blood work results in 50 words. You only answer the question asked and do not provide any additional information."),
                ("human", "Here are the blood work results: " + user_report + " What is the summary of these blood work results?"),
            ]
            raw_summary = llm.invoke(prompt_1)
            
            # 3. Clean the summary before displaying it
            clean_summary = remove_think_tags(raw_summary.content)
            
            st.subheader("📋 Medical Summary")
            st.info(clean_summary)
            
            # Agent 2: Diet Plan
            prompt_2 = [
                ("system", "You are a professional highly trained physician that gives accurate Indian Diet plan based on blood work results. You only answer the question asked and do not provide any additional information."),
                ("human", "Here are the blood work summary: " + clean_summary + " What is the Indian diet plan based on this summary?"),
            ]
            raw_diet_plan = llm.invoke(prompt_2)
            
            # 4. Clean the diet plan before displaying it
            clean_diet_plan = remove_think_tags(raw_diet_plan.content)
            
            st.subheader("🥗 Recommended Indian Diet Plan")
            st.success(clean_diet_plan)