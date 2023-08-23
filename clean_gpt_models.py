import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import glob
import shutil
import json

import io
df = pd.read_csv('urlViolations1.csv')

# or upload the csv using the file button and use this line
df = pd.read_csv('urlViolations1.csv')

# drop rows where the 'DOM' column contains potential issues
indices_to_drop = [31, 54, 55, 56, 57]
df = df.drop(indices_to_drop)

# adds a severity score column with specified name at given index
def add_severity_score(df, column_name, insert_index):
    # create dictionary to map impact types to numerical values
    impact_values = {
      'critical': 5,
      'serious': 4,
      'moderate': 3,
      'minor': 2,
      'cosmetic': 1,
    }
    # asssign numerical values to the 'impactValue' column
    df['impactValue'] = df['impact'].map(impact_values)

    # group by 'webURL' and calculate the score by summing the 'impactValue' for each group
    score_df = df.groupby('webURL')['impactValue'].sum().reset_index()

    # merge  'score_df' dataframe back into the original df based on 'webURL'
    df = pd.merge(df, score_df.rename(columns={'impactValue': column_name}), on='webURL')
    # insert score column at specified index
    df.insert(insert_index, column_name, df.pop(column_name))
    # drop the intermediary 'impactValue' column
    df.drop(columns='impactValue', inplace=True)

    return df

df = add_severity_score(df, 'initialScore', 5)


print(df['initialScore'].sum())
print(df['initialScore'].mean())
print("initial mean severity score: ", df['initialScore'].unique().sum() / df['webURL'].nunique())

"""#GPT Stuff"""

#run in terminal
#pip install openai
#pip install panel
#pip install mykeys

import openai
import panel as pn

openai.api_key = "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"

"""Function to count num tokens"""

#pip install tiktoken

import tiktoken
def count_tokens(text):
  enc = tiktoken.get_encoding("cl100k_base")
  assert enc.decode(enc.encode(text)) == text
  enc = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
  return len(enc.encode(text))

count_tokens("hello world!")

# function to get responses given system and user messages - using GPT-4
def GPT_response(system, user):
  print("system tokens: ", count_tokens(system))
  print("user tokens: ", count_tokens(user))
  response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
  {"role": "system", "content": system}, {"role": "user", "content": user}]
  )
  return response.choices[0].message.content

# function to get responses given system and user messages - using GPT-3.5-turbo-16K
"""def GPT_response(system, user):
  print("system tokens: ", count_tokens(system))
  print("user tokens: ", count_tokens(user))
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-16k",
  messages=[
  {"role": "system", "content": system}, {"role": "user", "content": user}]
  )
  return response.choices[0].message.content"""

"""###Testing System & User Messages"""

# testing function on row 2 of df
system_msg = """You are a helpful assistant who will correct accessibility issues of a provided website.
                Provide your thought before you provide a fixed version of the results.

                E.g.
                Incorrect: [['<span>Search</span>']]
                Thought: because ... I will ...
                Correct: [['<span class="DocSearch-Button-Placeholder">Search</span>']]"""
user_msg = """You are operating on this website: www.playwright.dev

Error: empty-heading
Description: Ensures headings have discernible text
Suggested change: Headings should not be empty

Incorrect: [['<h3></h3>', '<h3></h3>', '<h3></h3>', '<h3></h3>']]"""

GPT_response(system_msg, user_msg)

# row 1 of df
system_msg = """You are a helpful assistant who will correct accessibility issues of a provided website.
                Provide your thought before you provide a fixed version of the results.

                E.g.
                Incorrect: [['<h3></h3>', '<h3></h3>', '<h3></h3>', '<h3></h3>']]
                Thought: because ... I will ...
                Correct: [['<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>']]"""
user_msg = """You are operating on this website: www.playwright.dev

Error: color-contrast
Description: Ensures the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds
Suggested change: Elements must meet minimum color contrast ratio thresholds

Incorrect: [['<span class="DocSearch-Button-Placeholder">Search</span>']]"""

GPT_response(system_msg, user_msg)

"""### Prompt Engineering"""

#few shot prompting + chain of thought
system_msg = """You are an assistant who will correct web accessibility issues of a provided website.
                I will prompt you with an incorrect line of HTML.
                Provide a thought of what you think should be corrected before you provide a final correction.
                Here are a few examples:

                E.g.
                Input:
                Incorrect: [['<h3></h3>', '<h3></h3>']]
                Your Output:
                Thought: Because there are empty headings, I will add text in between the empty h3 tags.
                Correct: [['<h3>Some heading text</h3>', '<h3>Some heading text</h3>']]

                Input:
                Incorrect: [['<img src="image.png">', '<img src="image.png">']]
                Your Output:
                Thought: Because the images lack alt attributes, I will add them for accessibility.
                Correct: [['<img src="image.png" alt="Description">', '<img src="image.png" alt="Description">']]

                Input:
                Incorrect: [['<a href=""></a>', '<a href=""></a>']]
                Your Output:
                Thought: Because the links are empty, I will add a URL and text description.
                Correct: [['<a href="url">Link text</a>', '<a href="url">Link text</a>']]

                """


count_tokens(system_msg)

# function returns system message and user message for given row index of dataframe - no more DOM
def generate_prompt (row_index):
  system_msg = """You are an assistant who will correct web accessibility issues of a provided website.
                I will prompt you with an incorrect line of HTML.
                Provide a thought of what you think should be corrected before you provide a final correction.
                Here are a few examples:

                E.g.
                Input:
                Incorrect: [['<h3></h3>', '<h3></h3>']]
                Your Output:
                Thought: Because there are empty headings, I will add text in between the empty h3 tags.
                Correct: [['<h3>Some heading text</h3>', '<h3>Some heading text</h3>']]

                Input:
                Incorrect: [['<img src="image.png">', '<img src="image.png">']]
                Your Output:
                Thought: Because the images lack alt attributes, I will add them for accessibility.
                Correct: [['<img src="image.png" alt="Description">', '<img src="image.png" alt="Description">']]

                Input:
                Incorrect: [['<a href=""></a>', '<a href=""></a>']]
                Your Output:
                Thought: Because the links are empty, I will add a URL and text description.
                Correct: [['<a href="url">Link text</a>', '<a href="url">Link text</a>']]

                """
  user_msg = f"""You are operating on this website: {df['webURL'][row_index]}
  Error: {df['id'][row_index]}
  Description: {df['description'][row_index]}
  Suggested change: {df['help'][row_index]}

  Incorrect: {df['html'][row_index]}"""
  return system_msg, user_msg

#tree of thought
system_msg = """You are an assistant who will correct web accessibility issues of a provided website.
                I will prompt you with an incorrect line of HTML.
                Provide a thought of what you think should be corrected before you provide a final correction.
                Here are a few examples:

                E.g.
                Input:
                Incorrect: [['<h3></h3>', '<h3></h3>']]
                Your Output:
                Thought: Because there are empty headings, I will add text in between the empty h3 tags.
                Correct: [['<h3>Some heading text</h3>', '<h3>Some heading text</h3>']]

                Input:
                Incorrect: [['<img src="image.png">', '<img src="image.png">']]
                Your Output:
                Thought: Because the images lack alt attributes, I will add them for accessibility.
                Correct: [['<img src="image.png" alt="Description">', '<img src="image.png" alt="Description">']]

                Input:
                Incorrect: [['<a href=""></a>', '<a href=""></a>']]
                Your Output:
                Thought: Because the links are empty, I will add a URL and text description.
                Correct: [['<a href="url">Link text</a>', '<a href="url">Link text</a>']]

                """


count_tokens(system_msg)

"""###Generate Prompt"""

# function returns system message and user message for given row index of dataframe - no more DOM
def generate_prompt (row_index):
  system_msg = """You are a helpful assistant who will correct accessibility issues of a provided website.
                Provide your thought before you provide a fixed version of the results.

                E.g.
                Incorrect: [['<span>Search</span>']]
                Thought: because ... I will ...
                Correct: [['<span class="DocSearch-Button-Placeholder">Search</span>']]"""
  user_msg = f"""You are operating on this website: {df['webURL'][row_index]}
  Error: {df['id'][row_index]}
  Description: {df['description'][row_index]}
  Suggested change: {df['help'][row_index]}

  Incorrect: {df['html'][row_index]}"""
  return system_msg, user_msg

system_message = (generate_prompt(0))[0]
print(system_message)

user_message = (generate_prompt(0))[1]
print(user_message)

system_message = (generate_prompt(7))[0]
print(system_message)
user_message = (generate_prompt(7))[1]
print(user_message)

GPT_response(system_message, user_message)

"""##Function for generating prompt"""

# function returns system message and user message for given row index of dataframe - no more DOM
def generate_prompt (row_index):
  system_msg = """You are a helpful assistant who will correct accessibility issues of a provided website.
                Provide your thought before you provide a fixed version of the results.

                E.g.
                Incorrect: [['<span>Search</span>']]
                Thought: because ... I will ...
                Correct: [['<span class="DocSearch-Button-Placeholder">Search</span>']]"""
  user_msg = f"""You are operating on this website: {df['webURL'][row_index]}
  Error: {df['id'][row_index]}
  Description: {df['description'][row_index]}
  Suggested change: {df['help'][row_index]}

  Incorrect: {df['html'][row_index]}"""
  return system_msg, user_msg

system_message = (generate_prompt(0))[0]
print(system_message)

user_message = (generate_prompt(0))[1]
print(user_message)

system_message = (generate_prompt(7))[0]
print(system_message)
user_message = (generate_prompt(7))[1]
print(user_message)

GPT_response(system_message, user_message)

"""##Function for getting corrections"""

# assign system and user message by calling generate prompt message
system_message = (generate_prompt(0))[0]
user_message = (generate_prompt(0))[1]

print(user_message)

response = GPT_response(system_message, user_message)
response

import re
import requests
from bs4 import BeautifulSoup

# function returns corrected part of GPT response
def get_correction(row_index):
    # obtain response from GPT by calling prompt generation and chat functions
    system_msg = generate_prompt(row_index)[0]
    user_msg = generate_prompt(row_index)[1]
    response = GPT_response(system_msg, user_msg)

    # extract the "correct" part using regex
    correct_headers = re.search(r"Correct:\s*(\[\[.*\]\])", response)
    if correct_headers:
        return correct_headers.group(1)
    # means no corrections needed
    else:
        return df['html'][row_index]

df['html'][7]

get_correction(7)

"""##Create corrected DOM column"""

# group df by 'webURLs'
grouped_df = df.groupby('webURL')

# initialize  dictionary to store the corrected DOMs for each error row
corrected_doms_dict = {}

# iterate through groups with the same URL
for weburl, group_indices in grouped_df.groups.items():
    # get the group df using group indices
    group_df = df.loc[group_indices]

    # initialize  dictionary to store html corrections as an error fix pair
    error_fix_dict = {}

    # generate corrections for all html errors in a group
    dom = ''
    for index, row in group_df.iterrows():
        # print(row['webURL'], row['html'])
        # if at first row of group, initialize dom to be original group DOM
        if dom == '':
          dom = row['DOM']
        # call get_correction function and store correction in dictionary
        # error_fix_dict[row['html']] = get_correction(index)
        error = row['html']
        fix = get_correction(index)
        error_fix_dict[error] = fix
        print(row['webURL'], error, fix)

    dom_corrected = dom
    # iterate through error_fix dictionary and replace errors with fixes
    for error, fix in error_fix_dict.items():
      # insert corrections into current fixed DOM
      # print(error[3:-3], fix[3:-3])
      # dom_corrected = dom_corrected.replace(error[3:-3], fix[3:-3])  # [3:-3] removes enclosing [[ ]]
      dom_corrected = dom_corrected.replace(error[3:-3], fix[3:-3])  # [3:-3] removes enclosing [[ ]]


    for index, row in group_df.iterrows():
      # store all corrected DOMs in the dictionary indexed by row
      # basically every row of same URL group corresponds to the final corrected DOM created above
      corrected_doms_dict[index] = dom_corrected

# create new column with the final corrected DOMs
df['DOMCorrected'] = df.index.map(corrected_doms_dict)

df.to_csv('corrections.csv')

"""#Running corrections through Playwright"""

import os
import glob
import shutil
import requests
from bs4 import BeautifulSoup

import io
df = pd.read_csv('corrections.csv')

#npm install @axe-core/playwright

#npm init playwright

# "CI=1" makes it so HTML report doesn't start after tests are done running
#CI=1 npx playwright test

# use to remove all .json files starting with 'data'
def remove_files_starting_with(pattern):
    files_to_remove = glob.glob(pattern)
    for file_path in files_to_remove:
        try:
            if os.path.isfile(file_path):  # check if it's a file
                os.remove(file_path)
                #print(f"File '{file_path}' removed successfully.")
        except OSError as e:
            print(f"Error while removing file '{file_path}': {e}")

def corrections2violations(url, corrected_dom):
    with open("./tests/example.spec.ts", "w") as f:
      f.write(f"""


    // @ts-check
    const {{ test, expect }} = require('@playwright/test');
    const AxeBuilder = require('@axe-core/playwright').default;
    const fileReader = require('fs');

    test('all violations', async ({{ page }}) => {{
      await page.goto("{url}");

      await page.setContent(`{corrected_dom}`)

      const accessibilityScanResults = await new AxeBuilder({{ page }}).analyze(); // 4

      const violations = accessibilityScanResults.violations

      fileReader.writeFile("num_violations.txt", String(violations.length), function(err) {{
        if (err) console.log(err);
      }})

      // read violations individually into separate .json files
      for (let i = 0; i < violations.length; i++) {{
        fileReader.writeFile("data" + i + ".json", JSON.stringify(violations[i]), function(err) {{
          if (err) console.log(err);
        }})
      }}
    }});


    """)

    os.system("CI=1 npx playwright test")

    length = 0
    #store the num_violations in a length variable
    if os.path.exists('num_violations.txt'):
      length_file = open('num_violations.txt', "r")
      length = int(length_file.readline())

    df = pd.DataFrame()

    #build dataset by concatenating individual rows violations
    if length > 0:
      for i in range(length):
        df_temp = pd.read_json("data" + str(i) + ".json", lines=True)
        df_temp = df_temp.reset_index(drop = True)
        df = pd.concat([df, df_temp])
      df.insert(0, "webURL", url)
      df.insert(1, "numViolations", length)

      #extract html and failure summary from nodes column
      df['html'] = [[[node_item['html'] for node_item in nodes]] for nodes in df['nodes']]
      df['failureSummary'] = [[[node_item['failureSummary'] for node_item in nodes]] for nodes in df['nodes']]
      #drop the nodes column
      df.drop(['nodes'], axis = 1, inplace = True)

    #make a row of null values for a URL that has no violations
    else:
      df_temp = pd.DataFrame({'webURL' : [url], 'numViolations' : ['0'], 'id': ['None'], 'impact': ['None'], 'tags' : ['None'], 'description': ['None'], 'help' : ['None'], 'helpUrl' : ['None'], 'html' : ['None'], 'failureSummary' : ['None']})
      df_temp = df_temp.reset_index(drop = True)
      df = pd.concat([df, df_temp])

    #add row index
    df = df.reset_index(drop=True)

    #delete data.json's to reset for the next round
    remove_files_starting_with("data*")

    #remove num_violations.txt file
    if os.path.exists('num_violations.txt'):
      os.remove('num_violations.txt')

    df = add_severity_score(df,'finalScore',3)
    return df

corrections2violations(df['webURL'][0], df['DOMCorrected'][0])

df_corrections = pd.DataFrame()
first_rows = df.groupby('webURL').first()

for webURL, row in first_rows.iterrows():
    # Print current URL for progress
    print(webURL)

    # Concatenate individual rows
    df_temp = corrections2violations(webURL, row['DOMCorrected'])
    df_corrections = pd.concat([df_corrections, df_temp])

df_corrections.to_csv('correctionViolations.csv')

print(df_corrections['finalScore'].sum())
print("initial mean severity score: ", df_corrections['finalScore'].unique().sum() / df_corrections['webURL'].nunique())

"""###Prompt Engineering"""

#tree of thought prompting
import pandas as pd

explanations_dict = {}
code_fixes_dict = {}

df = pd.read_csv("urlViolations1.csv")

for index, row in df.iterrows():

  url = row["URL"]
  error = row["Error"]

def get_GPT_response(system, user):

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": user}
    ]
  )

  return response.choices[0].message.content

def get_explanation(text):
  return re.search(r"Explanation: (.*)", text).group(1)

def get_code(text):
  return re.search(r"Code: (.*)", text).group(1)

  system_msg = "You are an accessibility expert. Explain issues and provide code fixes."
  user_msg_1 = f"Website {url} has error {error}. Explain the issue step-by-step."
  user_msg_2 = "Thank you. Now provide code to fix this issue."

  response_1 = get_GPT_response(system_msg, user_msg_1)
  response_2 = get_GPT_response(system_msg, user_msg_2)

  explanation = get_explanation(response_1)
  explanations_dict[url] = explanation

  code = get_code(response_2)
  code_fixes_dict[url] = code

print(explanations_dict)
print(code_fixes_dict)

#types of prompting: tree of thought, parameterized, and follow-up
#specific

import pandas as pd
import re
import openai

df = pd.read_csv("urlViolations1.csv")

explanations_dict = {}
code_fixes_dict = {}

for index, row in df.iterrows():

  url = row['URL']
  error = row['Error']

  prompt = f"Explain the accessibility issue on {url}: {error}"

  response = openai.Completion.create(
    engine="text-davinci",
    prompt=prompt,
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5,
  )

  if "specific details" not in response.choices[0].text:

    prompt2 = "Can you explain this accessibility issue again using specific details?"
    response2 = openai.Completion.create(
      engine="text-davinci",
      prompt=prompt2,
      max_tokens=100,
      n=1,
      stop=None,
      temperature=0.5,
    )

    response = response2

  explanation = re.search(r"Explanation: (.*)", response.choices[0].text).group(1)

  explanations_dict[url] = explanation

print(explanations_dict)
print(code_fixes_dict)

# function returns system message and user message for given row index of dataframe - no more DOM
def generate_prompt (row_index):
  system_msg = """You are a helpful assistant who will correct web accessibility issues of a provided website.
                Provide a thought of what you think should be done before you provide a fixed version of the results.
                Here are a few examples of a possible thought that you could give:

                E.g.
                Incorrect: [['<h3></h3>', '<h3></h3>', '<h3></h3>', '<h3></h3>']]
                Thought: Because there are empty headings, I will add some form of text in between the text
                Correct: [['<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>']]

                E.g.
                Incorrect: [['<div id="top-menubar" class="goog-menubar format-lightborder" role="menubar" tabindex="0" style="-webkit-user-select: none;">']]
                Thought: Because there are empty headings, I will add some form of text in between the text
                Correct: [['<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>']]"""

  user_msg = f"""You are operating on this website: {df['webURL'][row_index]}
  Error: {df['id'][row_index]}
  Description: {df['description'][row_index]}
  Suggested change: {df['help'][row_index]}

  Incorrect: {df['html'][row_index]}"""
  return system_msg, user_msg

#few shot prompting

system_msg = """You are a helpful assistant who will correct web accessibility issues of a provided website.
                Provide a thought of what you think should be done before you provide a fixed version of the results.
                Here are a few examples of a possible thought that you could give:

                E.g.
                Incorrect: [['<h3></h3>', '<h3></h3>', '<h3></h3>', '<h3></h3>']]
                Thought: Because there are empty headings, I will add some form of text in between the text
                Correct: [['<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>']]

                E.g.
                Incorrect: [['<div id="top-menubar" class="goog-menubar format-lightborder" role="menubar" tabindex="0" style="-webkit-user-select: none;">']]
                Thought: Because there are empty headings, I will add some form of text in between the text
                Correct: [['<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>', '<h3>Some heading text</h3>']]"""


user_msg = """You are operating on this website: www.playwright.dev

Error: color-contrast
Description: Ensures the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds
Suggested change: Elements must meet minimum color contrast ratio thresholds

Incorrect: [['<span class="DocSearch-Button-Placeholder">Search</span>']]"""

GPT_response(system_msg, user_msg)