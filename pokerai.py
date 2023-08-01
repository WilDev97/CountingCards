import itertools
import pinecone
import pandas as pd
import random
import os
import random
import time
import openai
import requests
import json

openai.api_key = "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"
prompt = "On the table there is ace of hearts, 4 of diamonds, 8 of spades on the table. 10 of clubs and king of spades in my hand."
poker_info = "6 of diamonds denoted as 6d and ten of hearts as Th. Seperate cards by commas and no spaces. DISPLAY 10 as (T)"

poker_advice_func = {
    "name": "poker_advice",
    "description": "return json representation of poker cards",
    "parameters": {
        "type": "object",
        "properties": {
            "board": {
                "type": "string",
                "description": "Community Cards"
            },
            "hole": {
                "type": "string",
                "description": "cards in user's hand"
            },
            # "stage": {
            #     "type": "string",
            #     "description": "stage of poker game"
            # }
        },
        "required": ["board", "hole"]
    }
}
def poker_advice():
    prompt = input()
    """Takes the actual cards in your hand, opponents' numbers of cards and game stage to provide game advice
    """
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0613",
        messages = [
            {'role':'system', 'content': poker_info},
            {'role':'user', 'content': prompt}
        ],
        temperature = 0,
        max_tokens = 300,
        functions = [poker_advice_func]
        
    )
    
    if response['choices'][0]["finish_reason"] == "function_call":
            # this means we should call a function
            name = response['choices'][0]['message']['function_call']['name']
            objectx = json.loads(response['choices'][0]['message']['function_call']['arguments'])
            if name == 'poker_advice':
                
                url = "https://sf-api-on-demand-poker-odds-v1.p.rapidapi.com/flop"
                hole = objectx["hole"]
                hole
                querystring = {"board": objectx["board"],"hole": objectx["hole"]}
                objectx["board"]
                
                headers = {
                	"X-RapidAPI-Key": "0d38365192mshb8b71b48a871484p1c51b2jsn1934cb48b5f5",
                	"X-RapidAPI-Host": "sf-api-on-demand-poker-odds-v1.p.rapidapi.com"
                }
                
                response = requests.get(url, headers=headers, params=querystring)
                
                print(response.json())
            else:
                raise ValueError(f"Function name `{name}` not recognized!")
                
            
poker_advice()








