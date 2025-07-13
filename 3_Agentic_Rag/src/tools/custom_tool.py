import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(parent_dir, "db", "qdrant.db")
print(f"Using Qdrant database path: {db_path}")

class DocumentSearchToolInput(BaseModel):
    """Input schema for DocumentSearchTool."""
    query: dict = Field(..., description="Query to search the document. Must contain a 'query' key with the query string.")

class DocumentSearchTool(BaseTool):
    name: str = "DocumentSearchTool"
    description: str = "Search the document for the given query string."
    args_schema: Type[BaseModel] = DocumentSearchToolInput
    
    model_config = ConfigDict(extra="allow")
    def __init__(self, file_path: str, db_path:str = db_path):
        """Initialize the searcher with a PDF file path and set up the Qdrant collection."""
        super().__init__()
        self.file_path = file_path
        self.db_path = db_path
        self.client = QdrantClient(":memory:") 
        self._process_document()

    def _extract_text(self) -> str:
        """Extract raw text from provided file path using Firecrawl."""

        loader = PyPDFLoader(self.file_path)
        docs = loader.load()
        return docs
    
    # Assuming docs is a list of Document objects
    def _create_chunks(self, docs: list) -> list:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = text_splitter.split_documents(docs)

        return chunks

    def _process_document(self):
        """Process the document and add chunks to Qdrant collection."""
        # clear existing collection if it exists
        if self.client.collection_exists("demo_collection"):
            self.client.delete_collection("demo_collection")

        # create a new collection
        docs = self._extract_text()
        chunks = self._create_chunks(docs)
        # os.path.basename() extracts the final component (filename) from any path string, regardless of the operating system or path format.
        metadata = [{"source": os.path.basename(chunks[i].metadata['source']), 
                     "page_number": chunks[i].metadata['page_label']} for i in range(len(chunks))]
        print(metadata)
        data = [str(chunks[i].page_content) for i in range(len(chunks))]
        ids = list(range(len(chunks)))

        self.client.add(
            collection_name="demo_collection",
            documents=data,
            metadata=metadata,
            ids=ids
        )

    def _run(self, query: dict) -> list:
        """Search the document with a query string."""
        query = query['query']
        relevant_chunks = self.client.query(
            collection_name="demo_collection",
            query_text=query,
        )
        print(relevant_chunks)  # Debugging line to see the output
        docs = [(chunk.document, chunk.metadata) for chunk in relevant_chunks]
        separator = "\n___\n"
        return separator.join([f"Document: {doc}, Metadata: {meta}" for doc, meta in docs])
