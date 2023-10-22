from rag.pipeline.index_pipeline import IndexPipeline
from rag.pipeline.query_pipeline import QueryPipeline

if __name__ == "__main__":
    # IndexPipeline().index()

    result = QueryPipeline().query("What is the Automaton Halo?")
    print(result["answers"][0].answer)
