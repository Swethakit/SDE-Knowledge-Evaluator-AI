import os
from groq import Groq
import streamlit as st
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def ask_question(level):
    with st.spinner("Fetching question... 🕒"):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI Mock Interviewer for an SDE Intern role."
                },
                {
                    "role": "user",
                    "content": f"Ask ONE interview question for an SDE Intern at {level} level. Do not give the answer."
                }
            ]
        )
    return response.choices[0].message.content
def evaluate_answer(answer):
    with st.spinner("Evaluating answer... 🕒"):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI Mock Interviewer for an SDE Intern role."
                },
                {
                    "role": "user",
                    "content": f"""
Evaluate the candidate's answer below.
Answer:
{answer}
Give:
1. Score out of 10
2. Two strengths
3. Two areas for improvement
4. A short ideal answer (4–5 lines)
"""
                }
            ]
        )
    return response.choices[0].message.content
st.set_page_config(page_title="AI Mock Interview Buddy", page_icon="💎")
st.title("SDE Knowledge Evaluator AI")
st.write("Answer the questions and get instant feedback!")
level = st.selectbox("Select Level:", ["Beginner", "Intermediate", "Pro"])
if st.button("Get Question"):
    question = ask_question(level)
    st.session_state['current_question'] = question
    st.subheader(" Interview Question:")
    st.write(question)
answer = st.text_area(" Type your answer here:")
if st.button("Submit Answer"):
    if not answer.strip():
        st.warning("Please type your answer before submitting!")
    else:
        feedback = evaluate_answer(answer)
        st.subheader("📊 Feedback:")
        st.write(feedback)