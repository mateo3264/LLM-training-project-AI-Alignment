# from mha_finders import MHAFinder
from load_whole_dir import DocsHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langsmith import Client
from cli_tool import init_cli_tool
from constants import *

load_dotenv()
Client()


llm, main_concept = init_cli_tool(True)

# llm_inputs = LLMInputs(main_concept)



# retriever = mha_finder.retriever
#concepts = {'concepts':main_concept}
question = f'''Based on the article of T.V. Layng about teaching concepts 
find relevant documents of the following concepts. Make sure to get documents from each of the concepts enumerated:
Concepts:
{main_concept}
'''

print('question')
print(question)
context = DocsHandler().get_relevant_chunks(question)

# print(question.format(concepts=concepts))
# context = retriever.invoke(question.format(concepts=concepts))

print(15*'*'+'retrieved context'+15*'*')

for doc in context:
    print(doc.metadata)

template = '''Based on the context provided find the common and different characteristics of the following concepts:
Context:
{context}

Answer:'''

prompt = ChatPromptTemplate.from_template(template)


chain = (prompt | llm | StrOutputParser()).with_config({'run_name':'Finding common and exclusive characteristics between concepts'})

print(chain.invoke({'context':context}))


