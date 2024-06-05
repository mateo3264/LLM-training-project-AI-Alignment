from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


class DocsHandler:
    def __init__(self, dirname='data'):
        self.loader = DirectoryLoader(dirname, glob='*.txt', use_multithreading=True, loader_cls=TextLoader, loader_kwargs={'autodetect_encoding':True})
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        
        self.openai_embeddings = OpenAIEmbeddings()
    
    def load_docs_in_dir(self):

        raw_docs = self.loader.load()

        return raw_docs

    def split_docs(self, docs):
        chunks = self.text_splitter.split_documents(docs)
        return chunks
    
    def get_retriever(self):
        docs = self.load_docs_in_dir()
        chunks = self.split_docs(docs)
        db = Chroma.from_documents(chunks, self.openai_embeddings)
        retriever = db.as_retriever()
        return retriever

    def get_relevant_chunks(self, input):
        # raw_docs = self.load_docs_in_dir()
    
        
        retriever = self.get_retriever()

        retrieved_docs = retriever.invoke(input)

        return retrieved_docs




