import os # To get env vars in code
import time 

import requests
from dotenv import load_dotenv


from flask import Flask, render_template, request, jsonify

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END # Creates different nodes , END is the end node

load_dotenv() # Loading env objects from .env

# Converting them into Python Constants

BRIGHTDATA_API_KEY = os.getenv('BRIGHTDATA_API_KEY')
BRIGHTDATA_SERP_ZONE = os.getenv('BRIGHTDATA_SERP_ZONE')
BRIGHTDATA_GPT_DATASET_ID  = os.getenv('BRIGHTDATA_GPT_DATASET_ID')
BRIGHTDATA_PERPLEXITY_DATASET_ID = os.getenv('BRIGHTDATA_PERPLEXITY_DATASET_ID')

# Creating headers for requests that contain bright data API Key
#`headers` variable contains the authorization token and content type required for the request.
HEADERS = {
    'Authorization' : f'Bearer {BRIGHTDATA_API_KEY}',
    'Content-Type': 'application/json',
    'Accept' : 'application/json'
}

# Defining tools that Agent can use and decide how to use

@tool(description = 'Search using Google')  # to mark functions as "tools" that can be called by AI agents
def google_search(query):
    print('Google tool is being used...')
    # payload is passed in req to BrightData
    payload = {
        'zone' : BRIGHTDATA_SERP_ZONE,
        'url' : f'https://google.com/search?q={requests.utils.quote(query)}&brd_json=1',
        # requests.utils.quote(query) formats query in url encoding and brd_json defines we want a json file in return
        'format': 'raw',
        'country' : 'IN' # Request is gonna be sent from a Indian IP address
    }
   # This line of code is making a POST request to the BrightData API endpoint - Creating new data, .get retrieves data , .put updates existing,  
  
   # The 'json' parameter is used to send the payload data in JSON format.
    data = requests.post('https://api.brightdata.com/requests?async=true', headers = HEADERS, json = payload).json() 

    results = []
    for item in data.get('organic'):
        results.append(f"Title: {item['title']}\nLink: {item['link']}\n Snippet: {item.get('description', '')}")
    
    return '\n\n'.join(results)[:10000]     

@tool(description = 'Search using Bing')
def bing_search(query):
    print('Bing tool is being used...')
    # payload is passed in req to BrightData
    #A payload in JSON requests refers to the actual data being sent in the body of an HTTP request.
    payload = {
        'zone' : BRIGHTDATA_SERP_ZONE,
        'url' : f'https://bing.com/search?q={requests.utils.quote(query)}&brd_json=1',
        # requests.utils.quote(query) formats query in url encoding and brd_json defines we want a json file in return
        'format': 'raw',
        'country' : 'IN' # Request is gonna be sent from a Indian IP address
    }
   # This line of code is making a POST request to the BrightData API endpoint
  
   # The `json` parameter is used to send the payload data in JSON format.
    data = requests.post('https://api.brightdata.com/requests?async=true', headers = HEADERS, json = payload).json() 

    results = []
    for item in data.get('organic'):
        results.append(f"Title: {item['title']}\nLink: {item['link']}\n Snippet: {item.get('description', '')}")
    
    return '\n\n'.join(results)[:10000]     
@tool(description = 'Search using Reddit')
def reddit_search(query):
    print('Reddit tool is being used...')
    # payload is passed in req to BrightData
    payload = {
        'zone' : BRIGHTDATA_SERP_ZONE,
        'url' : f'https://google.com/search?q={requests.utils.quote('site:reddit.com' + query)}&brd_json=1',
        # requests.utils.quote(query) formats query in url encoding and brd_json defines we want a json file in return
        'format': 'raw',
        'country' : 'IN' # Request is gonna be sent from a Indian IP address
    }
   # This line of code is making a POST request to the BrightData API endpoint
  
   # The `json` parameter is used to send the payload data in JSON format.
    data = requests.post('https://api.brightdata.com/requests?async=true', headers = HEADERS, json = payload).json() 

    results = []
    for item in data.get('organic'):
        results.append(f"Title: {item['title']}\nLink: {item['link']}\n Snippet: {item.get('description', '')}")
    
    return '\n\n'.join(results)[:10000]     
@tool(description = 'Search using X')
def x_search(query):
    print('X tool is being used...')
    # payload is passed in req to BrightData
    payload = {
        'zone' : BRIGHTDATA_SERP_ZONE,
        'url' : f'https://google.com/search?q={requests.utils.quote('site:x.com' + query)}&brd_json=1',
        # requests.utils.quote(query) formats query in url encoding and brd_json defines we want a json file in return
        'format': 'raw',
        'country' : 'IN' # Request is gonna be sent from a Indian IP address
    }
   # This line of code is making a POST request to the BrightData API endpoint
  
   # The `json` parameter is used to send the payload data in JSON format.
    data = requests.post('https://api.brightdata.com/requests?async=true', headers = HEADERS, json = payload).json() 

    results = []
    for item in data.get('organic'):
        results.append(f"Title: {item['title']}\nLink: {item['link']}\n Snippet: {item.get('description', '')}")
    
    return '\n\n'.join(results)[:10000]    

@tool(description='Use ChatGPT to get the answer')
def gpt_prompt(query):
    print('GPT tool is being used...')
    
    payload = [
        {
            "url": "https://chatgpt.com",
            "prompt": query 
        }
    ]
    # We get an ID which points at a snapshot, we need to query if the snapshot is ready and then we need to fetch the info when it's ready
    
    url = f'https://api.brightdata.com/datasets/v3/trigger?dataset_id={BRIGHTDATA_GPT_DATASET_ID}&format=json&custom_output_fields=answer_text_markdown'
    
    response = requests.post(url, headers=HEADERS, json = payload)
    snapshot_id = response.json()['snapshot_id']
    
    while requests.get(f'https://api.brightdata.com/datasets/v3/progress/{snapshot_id}', headers= HEADERS).json()['status'] != 'ready':
        time.sleep(5)
    data = requests.get(f'https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json', headers=HEADERS).json()[0]
    
    return data['answer_text_markdown']
     
@tool(description='Use Perplexity to get the answer')
def perplexity_prompt(query):
    print('Perplexity tool is being used...')
    
    payload = [
        {
            "url": "https://perplexity.ai",
            "prompt": query 
        }
    ]
    # We get an ID which points at a snapshot, we need to query if the snapshot is ready and then we need to fetch the info when it's ready
    
    url = f'https://api.brightdata.com/datasets/v3/trigger?dataset_id={BRIGHTDATA_PERPLEXITY_DATASET_ID}&format=json&custom_output_fields=answer_text_markdown|sources'
    
    response = requests.post(url, headers=HEADERS, json = payload)
    snapshot_id = response.json()['snapshot_id']
    
    while requests.get(f'https://api.brightdata.com/datasets/v3/progress/{snapshot_id}', headers= HEADERS).json()['status'] != 'ready':
        time.sleep(5)
    data = requests.get(f'https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json', headers=HEADERS).json()[0]
    
    return data['answer_text_markdown'] + '\n\n' + str(data.get('sources', []))


llm = ChatOpenAI(model_name = 'gpt-4o', temperature= 0) #Automatically takes OPEN AI API key

agent = create_react_agent(
    model = llm,
    tools = [google_search, bing_search, gpt_prompt, perplexity_prompt, reddit_search, x_search],
    debug = False,
    prompt = "Use all tools at your disposal to answer user questions. Always use at least two tools. Preferably more. When giving an answer aggregate and summarize all information you get. Always provide a complete list of all sources which you used to find the information you provided. Make sure to add ALL links and sources here. Not just a few superficial ones."
)

# Creating an Agent node function

def agent_node(state):
    result = agent.invoke({'messages': [('human', state['query'])]})
    state['answer'] = result['messages'][-1].content
    return state # Every node takes in a state and returs a state

graph = StateGraph(dict)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)
app = graph.compile()

flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.is_json:
            query = request.get_json(silent=True).get("query", "").strip()
            if not query:
                return jsonify({"error": "No query provided"}), 400

            answer = app.invoke({"query": query})["answer"]
            return jsonify({"answer": answer})

        query = request.form.get("query", "").strip()
        if not query:
            return render_template("index.html", error="Please enter a query")

        answer = app.invoke({"query": query})["answer"]
        return render_template("index.html", query=query, answer=answer)

    return render_template("index.html")


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000, debug=True)

     




