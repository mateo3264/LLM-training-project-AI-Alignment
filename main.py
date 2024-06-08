from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache
from langchain_mongodb import MongoDBAtlasSemanticCache, MongoDBCache
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.callbacks import get_openai_callback
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langsmith import Client
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.load import loads, dumps
from langchain_core.runnables import RunnablePassthrough
from llm_prompts import *
from decorators import get_data_from_openai, time_taken
from operator import itemgetter
from load_whole_dir import DocsHandler
from mha_finders import MHAFinder
from cli_tool import init_cli_tool
import time
import os
import json
import pandas as pd
import ast
from extract_already_created_concept_examples import get_titles_of_examples


# llm, main_concept, format
arguments = init_cli_tool(True)

llm_inputs = LLMInputs(arguments['main_concept'])




#load env vars
load_dotenv()

#record in langsmith
Client()



#--------------Must Have/Can Have Attributes Phase--------------
concept_mhas_filename = 'concept_mhas.json'
json_file = open(concept_mhas_filename)

queried_concepts_with_mhas = json.load(json_file)

if queried_concepts_with_mhas.get(arguments['main_concept'], None) is None:
    initial_time = time.perf_counter()
    defining_characteristics = MHAFinder(llm_inputs).get_MHAs(arguments['LLM'])
    print('Time taken to find the MHAs: ', time.perf_counter() - initial_time)
    queried_concepts_with_mhas[arguments['main_concept']] = defining_characteristics
    print('queried_concepts_with_mhas')
    print(queried_concepts_with_mhas)
    json_file_write = open(concept_mhas_filename, 'w')
    json.dump(queried_concepts_with_mhas, json_file_write)
else:
    print('from already queried concept')
    defining_characteristics = queried_concepts_with_mhas[arguments['main_concept']]
input('continue with examples?')


#--------------RATIONAL SET PHASE--------------

prompt = ChatPromptTemplate.from_template(EXAMPLES_TEMPLATE)
prompt_nonexamples = ChatPromptTemplate.from_template(NONEXAMPLES_TEMPLATE)




chain = prompt | arguments['LLM'] | StrOutputParser()
chain_nonexample = prompt_nonexamples | arguments['LLM'] | StrOutputParser()

#chair_concept = {'concept':'chair', 'characteristics':'''1- Has a back.\n2- Sits one person.\n3- Legs rest at a 90 degree angle approximately'''}
#belief_concept = {'concept':'to believe', 'characteristics':'''1- Some event missing. 2- Action taken to affirm the likelihood of the event.'''}
print(10*'0','defining_characteristics',10*'0')
print(defining_characteristics)
main_concept = {'concept':arguments['main_concept'], 'defining_characteristics':defining_characteristics}


concept_examples_filename = 'concept_examples.jsonl'

with open(concept_examples_filename, 'r') as file:
        concept_examples = json.load(file)


existing_examples = get_titles_of_examples(concept_examples, arguments['main_concept'])
existing_examples = '\n'.join(existing_examples)
print('existing_examples:')
print(existing_examples)
print('defining_characteristics')
print(defining_characteristics)

if arguments['format'] == 'json':
    chain_input = {
        'concept':arguments['main_concept'],
        'defining_characteristics':defining_characteristics,
        'examples_format':json_examples_format,
        'existing_examples':existing_examples
        }
else:
    chain_input = {
        'concept':arguments['main_concept'], 
        'defining_characteristics':defining_characteristics, 
        'examples_format':csv_examples_format,
        'existing_examples':existing_examples
        }

with get_openai_callback() as c:
    print(15*'*', 'EXAMPLES', 15*'*')
    examples_of_rational_set = chain.invoke(chain_input)
    

    
    
    if concept_examples.get(main_concept['concept'], None) is not None:
        concept_examples[main_concept['concept']] += examples_of_rational_set
    else:
        concept_examples[main_concept['concept']] = examples_of_rational_set

    
    
    # for concept in concept_examples:
    #    concept_examples[concept] = ast.literal_eval(concept_examples[concept])

    print(concept_examples)
    #print(type(concept_examples))
    # df = pd.DataFrame(concept_examples)
    # df.to_json(concept_examples_filename, orient='records', lines=True)

    with open(concept_examples_filename, 'w') as file:

        json.dump(concept_examples, file)
        # csv.writer()

    
    # print(examples_of_rational_set)
    #json_examples_of_rational_set = json.loads(examples_of_rational_set)
    #print(json_examples_of_rational_set)
    usu_response = input('Continue with nonexamples?')
    if 'y' in usu_response.lower():
        print(15*'*', 'NONEXAMPLES', 15*'*')
        print(chain_nonexample.invoke(main_concept))
    print(c)





