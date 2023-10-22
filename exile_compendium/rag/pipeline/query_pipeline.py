from haystack import Pipeline
from haystack.document_stores import WeaviateDocumentStore
from haystack.nodes import (AnswerParser, EmbeddingRetriever, PromptModel,
                            PromptNode, PromptTemplate)
from haystack.utils import print_documents


class QueryPipeline:
    def query(self, query: str):
        document_store = WeaviateDocumentStore(
            host="http://localhost", port=8080, embedding_dim=1024
        )
        retriever = EmbeddingRetriever(
            document_store=document_store, embedding_model="BAAI/bge-large-en-v1.5"
        )

        prompt_template = PromptTemplate(
            prompt="""
            Answer the question truthfully based solely on the given documents. If the documents do not contain the answer to the question, say that answering is not possible given the available information. Your answer should be no longer than 50 words.
            Documents:{join(documents)}
            Question:{query}
            Answer:
            """,
            output_parser=AnswerParser(),
        )

        prompt_node = PromptNode(
            model_name_or_path="mistralai/Mistral-7B-Instruct-v0.1",
            default_prompt_template=prompt_template,
        )

        pipeline = Pipeline()

        pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
        pipeline.add_node(
            component=prompt_node, name="PromptNode", inputs=["Retriever"]
        )

        result = pipeline.run(
            query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 1}}
        )

        return result
