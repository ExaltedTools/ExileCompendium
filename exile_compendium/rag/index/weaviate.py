from haystack import Pipeline
from haystack.document_stores import WeaviateDocumentStore
from haystack.nodes import EmbeddingRetriever, MarkdownConverter, PreProcessor


def index():
    document_store = WeaviateDocumentStore(
        host="http://localhost", port=8080, embedding_dim=1024
    )
    converter = MarkdownConverter()
    preprocessor = PreProcessor()
    retriever = EmbeddingRetriever(
        document_store=document_store, embedding_model="BAAI/bge-large-en-v1.5"
    )

    indexing_pipeline = Pipeline()
    indexing_pipeline.add_node(
        component=converter, name="HTMLConverter", inputs=["File"]
    )
    indexing_pipeline.add_node(
        component=preprocessor, name="PreProcessor", inputs=["HTMLConverter"]
    )
    indexing_pipeline.add_node(
        component=retriever, name="Retriever", inputs=["PreProcessor"]
    )
    indexing_pipeline.add_node(
        component=document_store, name="DocumentStore", inputs=["Retriever"]
    )

    indexing_pipeline.run(file_paths=["filename.pdf"])
