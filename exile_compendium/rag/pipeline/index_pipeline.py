from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from langchain.vectorstores.weaviate import Weaviate
from rag.loader.poe_wiki_loader import WikiLoader


class IndexPipeline:
    def index(self):
        loader = WikiLoader()
        documents = loader.load()

        text_splitter = SentenceTransformersTokenTextSplitter()
        docs = text_splitter.split_documents(documents)

        embedder = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={"device": "cuda"},
            encode_kwargs={"normalize_embeddings": True},
            query_instruction="Represent this question for searching relevant passages: ",
        )

        document_store = Weaviate.from_documents(
            docs, embedder, index_name="PoEWiki", by_text=False
        )

        print(document_store)
