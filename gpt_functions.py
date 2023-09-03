import openai
import tiktoken
import pandas as pd
import os
import re

class GPTFunctions:
    def __init__(self):
        self.df = pd.read_csv('urlViolations.csv')

    # function to count the number of tokens
    def count_tokens(self, text):
        enc = tiktoken.get_encoding("cl100k_base")
        assert enc.decode(enc.encode(text)) == text
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
        return len(enc.encode(text))

    # function to get responses given system and user messages
    # change model name as needed
    def GPT_response(self, system, user):
        #print("system tokens: ", self.count_tokens(system))
        #print("user tokens: ", self.count_tokens(user))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        )
        return response.choices[0].message.content

    """BASELINE ReAct Prompt"""

    # function returns system message and user message for a given row index of the dataframe - no more DOM
    def generate_prompt(self, row_index):
        system_msg = """You are a helpful assistant who will correct accessibility issues of a provided website.
                      Provide your thought before you provide a fixed version of the results.

                      E.g.
                      Incorrect: [['<span>Search</span>']]
                      Thought: because ... I will ...
                      Correct: [['<span class="DocSearch-Button-Placeholder">Search</span>']]"""
        user_msg = f"""You are operating on this website: {self.df['webURL'][row_index]}
        Error: {self.df['id'][row_index]}
        Description: {self.df['description'][row_index]}
        Suggested change: {self.df['help'][row_index]}

        Incorrect: {self.df['html'][row_index]}"""
        return system_msg, user_msg

    # example system message
    #system_message = generate_prompt(0)[0]
    #print(system_message)

    # example user message
    #user_message = generate_prompt(0)[1]
    #print(user_message)

    #GPT_response(system_message, user_message)

    """Function for getting GPT corrections"""

    # function returns the corrected part of GPT response
    def get_correction(self, row_index):
        # obtain response from GPT by calling prompt generation and chat functions
        system_msg = self.generate_prompt(row_index)[0]
        user_msg = self.generate_prompt(row_index)[1]
        response = self.GPT_response(system_msg, user_msg)

        # extract the "correct" part using regex
        correct_headers = re.search(r"Correct:\s*(\[\[.*\]\])", response)
        if correct_headers:
            return correct_headers.group(1)
        # means no corrections needed
        else:
            return self.df['html'][row_index]
