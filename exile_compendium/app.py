from dotenv import load_dotenv
from rag.pipeline.query_pipeline import QueryPipeline

load_dotenv()

if __name__ == "__main__":
    # IndexPipeline().index()
    QueryPipeline().query("List me some of the league mechanics")
