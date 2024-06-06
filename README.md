# LLM-training-project-AI-Alignment


## Description
* The purpose of this repo is to use one LLM to train a smaller one to generate examples and nonexamples of a given concept so that the learning process of a user can be speed up. Still under construction

## Setup .env file
* Copy the contents of .env.example into a new file called .env
* Assign to each variable the proper key or data

## Install python libraries

* Run the command `pip install -r requirements.txt`

# How to use it
* execute the main file like this: `py main.py "<YOUR_CONCEPT>" -m gpt-4o`
* The project supports gpt models, anthropic and gemini models.
* Note: For now the project only uses the files in the data folder so the concepts to use are limited 