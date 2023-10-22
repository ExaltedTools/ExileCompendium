from haystack import Pipeline
from haystack.document_stores import WeaviateDocumentStore
from haystack.nodes import EmbeddingRetriever, PreProcessor
from rag.fetch.poe_wiki_fetcher import WikiFetcher


class IndexPipeline:
    def index():
        document_store = WeaviateDocumentStore(
            host="http://localhost", port=8080, embedding_dim=1024
        )
        converter = WikiFetcher()
        preprocessor = PreProcessor()
        retriever = EmbeddingRetriever(
            document_store=document_store, embedding_model="BAAI/bge-large-en-v1.5"
        )

        pipeline = Pipeline()

        pipeline.add_node(component=converter, name="POEWikiFetcher", inputs=["File"])
        pipeline.add_node(
            component=preprocessor, name="PreProcessor", inputs=["POEWikiFetcher"]
        )
        pipeline.add_node(
            component=retriever, name="Retriever", inputs=["PreProcessor"]
        )
        pipeline.add_node(
            component=document_store, name="DocumentStore", inputs=["Retriever"]
        )

        pipeline.run()
