import os

import weaviate
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.llms.llamacpp import LlamaCpp
from langchain.vectorstores.weaviate import Weaviate


class QueryPipeline:
    def query(self, question: str):
        llm = LlamaCpp(
            model_path="/home/cedtoup/.cache/huggingface/hub/mistral-7b-openorca/mistral-7b-openorca.Q4_K_M.gguf",
            n_gpu_layers=1,
            n_batch=512,
            n_ctx=2048,
            f16_kv=True,
            verbose=True,
        )

        embedder = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={"device": "cuda"},
            encode_kwargs={"normalize_embeddings": True},
            query_instruction="Represent this question for searching relevant passages: ",
        )

        client = weaviate.Client(url=os.environ["WEAVIATE_URL"])
        weaviate_store = Weaviate(
            client=client,
            embedding=embedder,
            index_name="PoEWiki",
            text_key="text",
            by_text=False,
        )
        retriever = weaviate_store.as_retriever()

        chain = ConversationalRetrievalChain.from_llm(
            llm, retriever=retriever, verbose=True
        )

        answer = chain({"question": question, "chat_history": []})
        print(answer)
