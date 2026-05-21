import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), temperature=0, model="llama-3.3-70b-versatile")
        
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The extract text is from the career page of a website. 
            your job is to extract the job posting and retrn then in JSON format containing the following keys: 'role', 'experience', 'skills', 'description'.
            only return the valid JSON.
            ### VALID JSON (No PREAMBLE)
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Content is too big, Unable to parse the output.")
        return res if isinstance(res, list) else [res]
    
    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            ### INSTRUCTION:
            You are sadik, a software engineer with 3 years of experience.
            your job is to write a cold email to the hiring manager of the job described above, and you want to apply for this job.
            Here is my linkedin profile: https://www.linkedin.com/in/sadik-ibrahim-1a9b4a1b2/
            Here is my github profile: https://www.github.com/sadik
            Here is some of my projects that I have already done {links_list}
            GIVE JUST EMAIL, NO PREAMBLE.
            """
        )
        chain_email = prompt_email | self.llm
        response = chain_email.invoke(input={"job_description": str(job), "links_list": links})
        return response.content
    