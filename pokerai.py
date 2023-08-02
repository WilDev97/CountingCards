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
poker_info = "6 of diamonds denoted as 6d and ten of hearts as Th. Seperate cards by commas and no spaces. DISPLAY 10 as (T)"

poker_advice_func = {
    "name": "poker_advice",
    "description": "return json representation of poker cards",
    "parameters": {
        "type": "object",
        "properties": {
            "board": {
                "type": "string",
                "description": "list of 3 community cards"
            },
            "hole": {
                "type": "string",
                "description": "list of two cards in user's hand"
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
    prompt = input("What cards are on the flop and in your hand?: ")
    """Takes the actual cards in your hand, opponents' numbers of cards and game stage to provide game advice
    """
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0613",
        messages = [
            {'role':'system', 'content': "no two cards returned should be duplicates"},
            {'role':'assistant', 'content': poker_info},
            {'role':'user', 'content': prompt}
        ],
        temperature = 0,
        max_tokens = 300,
        functions = [poker_advice_func]
        
    )
   # response['choices'][0]['message']['function_call']['arguments'] 
    if response['choices'][0]["finish_reason"] == "function_call":
            # this means we should call a function
            name = response['choices'][0]['message']['function_call']['name']
            objectx = json.loads(response['choices'][0]['message']['function_call']['arguments'])
            if name == 'poker_advice':
                
                url = "https://sf-api-on-demand-poker-odds-v1.p.rapidapi.com/flop"
                hole = objectx["hole"]
                hole
                querystring = {"board": objectx["board"],"hole": objectx["hole"]}
                print(f"Board: {objectx['board']} \nHole: {objectx['hole']}")
                
                headers = {
                	"X-RapidAPI-Key": "0d38365192mshb8b71b48a871484p1c51b2jsn1934cb48b5f5",
                	"X-RapidAPI-Host": "sf-api-on-demand-poker-odds-v1.p.rapidapi.com"
                }
                
                response = requests.get(url, headers=headers, params=querystring)               
                card_analytics = response.json()
                
                system = """You are an AI Texas Hold'em expert. Your goal is to provide pre-flop advice \
                    to the user based on the information provided about their hand and the\
                    community cards. The poker terms to be familiar with are: 
                        Hole Cards: The two private cards dealt to each player at the beginning of a hand.
                        Community Cards: The cards dealt face-up on the table, shared by all players, in the center of the table.
                        Flop: The first three community cards dealt face-up after the first betting round.
                        Turn: The fourth community card dealt after the second betting round.
                        River: The fifth and final community card dealt after the third betting round.
                        Preflop: The betting round that occurs before the flop is dealt.
                        Postflop: The betting rounds that occur after the flop, including the turn and river.
                        Check: To pass the action to the next player without betting.
                        Bet: To place chips into the pot as the first action in a betting round.
                        Raise: To increase the bet made by a previous player.
                        Call: To match the bet made by a previous player.
                        Fold: To discard your hand and forfeit the current hand.
                        All-In: To bet all of your remaining chips on a single hand.
                        High Card: When you don't have any pairs or higher combinations, your hand is ranked based on the highest card you hold. The player with the highest card wins in a showdown if no one has a pair or better.
                        
                        One Pair: This hand consists of two cards of the same rank, along with three unrelated cards. The hand is ranked by the pair, and in case of a tie, the highest side card determines the winner.
                        Two Pair: Two Pair consists of two sets of cards with the same rank, along with one unrelated card. The hand is ranked by the higher pair first, then the lower pair, and finally, the side card in case of a tie.Three of a Kind: This hand contains three cards of the same rank, along with two unrelated cards. The ranking is based on the three cards of the same rank.
                        Straight: A Straight consists of five consecutive cards of any suit. The hand is ranked by the highest card in the sequence.
                        Flush: A Flush contains five cards of the same suit, but they don't need to be in sequence. If multiple players have a Flush, the one with the highest card wins.
                        Full House: A Full House consists of three cards of the same rank and a pair of another rank. The ranking is determined by the three cards first and then the pair.
                        Four of a Kind: This hand contains four cards of the same rank, along with one unrelated card. The ranking is based on the four cards of the same rank.
                        Straight Flush: A Straight Flush is a combination of a Straight and a Flush. It consists of five consecutive cards of the same suit, and the ranking is determined by the highest card in the sequence.
                        Royal Flush: This is the best hand in poker. It is a Straight Flush but specifically contains the top five highest cards: 10, Jack, Queen, King, and Ace, all of the same suit.
                    Remember to keep the advice clear and concise. Use markdown for formatting if necessary.

                    Your advice should include:
                    - The probability of the user getting specific poker hands like one pair (1P), two pairs (2P), three of a kind (3K), etc.
                    - The odds of achieving these hands based on the current cards.
                    - The overall strength of the user's hand and its rank compared to other possible hands.
                    The cards being evaluated are {objectx['board']} and {objectx['hole']}.
                    x% corresponds to the likelyhood of the user hitting that hand.
                    Example Response:
                    High Card: x% \n
                    One-Pair: x% \n
                    Two-Pair: x% \n
                    Three of a Kind: x% \n
                    Straight: x% \n
                    Flush: x% \n
                    Full House: x% \n
                    Four of a Kind: x% \n
                    Straight Flush: x% \n
                    Royal Flush: x% \n
                    I would recommend based off these statistics, that you:
                    (check, fold, or raise)"""
                    
                generated_response = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [
                        {'role':'system', 'content': system},
                        {'role':'user', 'content': json.dumps(card_analytics)}
                    ],
                    temperature = 0,
                    max_tokens = 300,
                )
            
                print(generated_response.choices[0].message.content)
                # print(type(response))
                # print(type(response.json))
                # print(response["average"])

            else:
                raise ValueError(f"Function name `{name}` not recognized!")
                
            
# card_analytics = poker_advice()
# card_analytics_json = json.dumps(card_analytics)
# card_analytics['data']['me']['rank']

poker_advice()
