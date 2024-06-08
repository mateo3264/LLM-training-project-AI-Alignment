import argparse
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

def init_cli_tool(verbose=False):

    parser = argparse.ArgumentParser(description='Generate rational set given a concept')

    parser.add_argument('concept', type=str, help='define the concept')

    parser.add_argument('-m', '--model', type=str, help='define the llm model', default='gpt-3.5-turbo-0125')
    
    parser.add_argument('-f', '--format', type=str, help='define the response format of the model', default='json')


    
    args = parser.parse_args()

    model_name = args.model
    
    if 'gpt' in model_name:
        llm = ChatOpenAI(model=model_name, temperature=1)
    elif 'gemini' in model_name:
        llm = ChatGoogleGenerativeAI(model=model_name)
    elif 'claude' in model_name:
        llm = ChatAnthropic(model=model_name)
    
    if args.concept != '':
        main_concept = args.concept
    else:
        raise ValueError('Concept must be non null string')

    if verbose:
        print('Main Concept:')
        input(main_concept)
        print('LLM:')
        try:
            print(llm.model_name)
        except:
            print(llm.model)

    format = args.format
    arguments = {'LLM':llm, 'main_concept':main_concept, 'format':format}

    return arguments

        