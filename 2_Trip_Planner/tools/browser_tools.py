import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from unstructured.partition.html import partition_html
from crewai import Agent, Task
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai import LLM
from crewai import Crew

import os
from dotenv import load_dotenv
load_dotenv()

class WebsiteInput(BaseModel):
    website: str = Field(..., description="The website URL to scrape")

class BrowserTools(BaseTool):
    name: str = "Scrape website content"
    description: str = "Useful to scrape and summarize a website content. Input should be a valid URL in a string format. Example: 'https://docs.crewai.com/en/concepts/tools'. "
    args_schema: type[BaseModel] = WebsiteInput

    def _run(self, website: str) -> str:
        try:
            url = f"https://production-sfo.browserless.io/content?token={os.getenv('BROWSERLESS_API_KEY')}"
            headers = {"Cache-Control": "no-cache","Content-Type": "application/json"}
            data = {"url": website, "rejectResourceTypes": ["image"],"rejectRequestPattern": ["/^.*\\.(css)"]}
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code != 200:
                return f"Error: Failed to fetch website content. Status code: {response.status_code}"
            
            elements = partition_html(text=response.text)
            content = "\n\n".join([str(el) for el in elements])
            # print(content)
            content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
            summaries = []
            
            #llm = LLM(model="groq/deepseek-r1-distill-llama-70b")
            llm = LLM(model="gemini/gemini-2.0-flash")
            
            for chunk in content:
                agent = Agent(
                    role='Principal Researcher',
                    goal='Do amazing researches and summaries based on the content you are working with',
                    backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                    allow_delegation=False,
                    llm=llm
                )
                task = Task(
                    description=f"""Analyze and summarize the content below, 
                    make sure to include the most relevant information in the summary, 
                    return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}""",
                    expected_output="A concise summary of the content provided",
                    agent=agent
                )
                # crew = Crew(agents=[agent], tasks=[task], verbose=True)
                # summary = crew.kickoff()
                summary = agent.execute_task(task = task)
                summaries.append(summary)
            return "\n\n".join(summaries)
        except Exception as e:
            return f"Error while processing website: {str(e)}"

    async def _arun(self, website: str) -> str:
        raise NotImplementedError("Async not implemented")

if __name__ == "__main__":
    # Example usage
    browser_tool = BrowserTools()
    website = "https://docs.crewai.com/en/concepts/tools"
    result = browser_tool._run(website)
    print(result)