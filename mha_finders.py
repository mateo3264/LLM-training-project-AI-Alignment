from decorators import get_data_from_openai
from langchain_core.load import loads, dumps
from langchain_core.prompts import ChatPromptTemplate
from constants import *
from load_whole_dir import DocsHandler
from langchain_core.output_parsers import StrOutputParser

class MHAFinder:
    def __init__(self, llm_input:LLMInputs):
        self.llm_input = llm_input
        self.mha_prompt = ChatPromptTemplate.from_template(MHA_TEMPLATE)
        self.retriever = DocsHandler().get_retriever()
        self.retriever_chain = (
                                    self.get_list_of_manual_multiple_queries
                                    | self.retriever.map() 
                                    | self.get_unique_union
                                )
    def get_unique_union(self, documents):

        flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]

        unique_docs = list(set(flattened_docs))

        return [loads(doc) for doc in unique_docs]

    def get_list_of_manual_multiple_queries(self, not_used_arg):
        return self.llm_input.manual_multiquery
    
    @get_data_from_openai
    def get_MHAs(self, llm, verbose=False):
        retrieved_docs = self.retriever_chain.invoke({'question':self.llm_input.mha_input})
        mha_chain = self.mha_prompt | llm | StrOutputParser()

        defining_characteristics = mha_chain.invoke({'concept':self.llm_input.main_concept, 'context':retrieved_docs})

        if verbose:
            print(defining_characteristics)
    
        return defining_characteristics
