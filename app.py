import numpy as np
import pandas as pd
import streamlit as st 
from resume_scoring import predict_resume_scoring

def main():
    st.title("Welcome to Resume Scoring Process of Stratlytic")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Resume Scoring App </h2>
    <p style="color:white;text-align:center;">Please fill up following inputs </p>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    job_title = st.text_input("Job Title","Enter job title you are looking for")
    skill = st.text_input("Skills(comma-seperated)","Enter all required skills you are looking for")
    education= st.selectbox("Education", ["Bachelor's Degree", "Master's Degree", "PhD"])
    experience = st.slider("Experience (in years)", min_value=0, max_value=20, value=0)
    result=""
    if st.button("Predict"):
        result=predict_resume_scoring(job_title,skill,education,experience)
    st.success('The output is {}'.format(result))
    if st.button("About"):
        st.text("Lets LEarn")
        st.text("Built with Streamlit")

if __name__=='__main__':
    main()