import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from src.connector.openai_connector import OpenAIConnection
from src.endpoints.content_extractor import get_website_content

instruction = "You are an assistant who will not use your existing knowledge about compliance, but will only cross refer the rules mentioned in our content and check whether the user's input content is compliant with those rules or not. You may use your reasoning abilities \n \n\n\n\n  Our Rules Content: "

if __name__ == "__main__":
    api_key = os.environ.get('OPEN_AI_API_KEY')
    url = os.environ.get('URL')
    connection = OpenAIConnection()
    content = get_website_content(url=url)
    detailed_instruction = instruction+content
    assistant = connection.client.beta.assistants.create(name="Content Compliance Checker",
                                                        instructions=detailed_instruction,
                                                        model="gpt-4-1106-preview")
    print("your assistant ID is :",{assistant.id})
    


