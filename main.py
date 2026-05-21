import streamlit as st

st.title("Cold email generator for job applications")
st.text_input("Enter the job link:", key="job_link")
if st.button("Submit"):
    job_link = st.session_state.job_link
    if job_link:
        st.code(f"Hello hiring manager, I am interested in this job: {job_link}. Please let me know if you have any questions.")