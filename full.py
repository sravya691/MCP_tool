import os
import json
import subprocess
import time
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

CONFIG_PATH = "browser_mcp.json"

def load_mcp_config(path):
    with open(path, "r") as f:
        return json.load(f)["mcpServers"]

import subprocess

def start_mcp_server(name, config):
    command = [config["command"]] + config["args"]
    print(f"Starting MCP server '{name}' with command: {' '.join(command)}")
    process = subprocess.Popen(' '.join(command), shell=True)
    return process
def query_duckduckgo(query):
    url = "http://localhost:3000/search"
    try:
        res = requests.post(url, json={"query": query})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return f"Failed to query server: {e}"

def summarize_with_groq(text):
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise ValueError("Missing GROQ_API_KEY in .env")

    llm = ChatGroq(groq_api_key=groq_key, model="llama3-8b-8192")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}")
    ])
    chain = prompt | llm
    response = chain.invoke({"input": text})
    return response.content

if __name__ == "__main__":
    mcp_config = load_mcp_config(CONFIG_PATH)
    mcp_name = "duckduckgo-search"

    # Start MCP server
    server_process = start_mcp_server(mcp_name, mcp_config)
    
    # Wait for the server to start
    print("Waiting for server to boot...")
    time.sleep(5)

    # Query the server
    search_term = "Top open source LLMs in 2024"
    print(f"\nQuerying MCP Server ({mcp_name}) for: {search_term}")
    mcp_result = query_duckduckgo(search_term)
    print("\nMCP Server Output:\n", mcp_result)

    # Summarize via Groq
    summary_input = str(mcp_result)
    groq_response = summarize_with_groq(summary_input)
    print("\nGroq Summary:\n", groq_response)

    # Optional: kill server
    server_process.terminate()
