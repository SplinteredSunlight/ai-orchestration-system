from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import json
from datetime import datetime

from app.core.config import settings

class RAGManager:
    """Manages the shared knowledge base using ChromaDB"""

    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
            is_persistent=True
        ))
        
        # Use OpenAI's embedding function
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name="text-embedding-ada-002"
        )

        # Collections for different types of knowledge
        self.collections = {
            "task_results": self.client.get_or_create_collection(
                name="task_results",
                embedding_function=self.embedding_function
            ),
            "code_snippets": self.client.get_or_create_collection(
                name="code_snippets",
                embedding_function=self.embedding_function
            ),
            "design_assets": self.client.get_or_create_collection(
                name="design_assets",
                embedding_function=self.embedding_function
            ),
            "marketing_content": self.client.get_or_create_collection(
                name="marketing_content",
                embedding_function=self.embedding_function
            )
        }

    async def store_task_result(
        self,
        task_id: str,
        task_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store task result in the appropriate collection"""
        try:
            # Prepare the document
            document = {
                "task_id": task_id,
                "task_type": task_type,
                "content": json.dumps(content),
                "timestamp": datetime.utcnow().isoformat()
            }
            if metadata:
                document.update(metadata)

            # Store in task_results collection
            self.collections["task_results"].add(
                documents=[json.dumps(document)],
                metadatas=[document],
                ids=[task_id]
            )

            # Store in type-specific collection if applicable
            if content.get("code"):
                self.collections["code_snippets"].add(
                    documents=[content["code"]],
                    metadatas=[{
                        "task_id": task_id,
                        "language": metadata.get("language", "unknown"),
                        "framework": metadata.get("framework", "none"),
                        "timestamp": document["timestamp"]
                    }],
                    ids=[f"code_{task_id}"]
                )
            elif content.get("image_url"):
                self.collections["design_assets"].add(
                    documents=[content["description"]],
                    metadatas=[{
                        "task_id": task_id,
                        "image_url": content["image_url"],
                        "style": metadata.get("style", "none"),
                        "timestamp": document["timestamp"]
                    }],
                    ids=[f"design_{task_id}"]
                )
            elif content.get("marketing_content"):
                self.collections["marketing_content"].add(
                    documents=[content["marketing_content"]],
                    metadatas=[{
                        "task_id": task_id,
                        "content_type": metadata.get("content_type", "general"),
                        "target_audience": metadata.get("target_audience", "general"),
                        "timestamp": document["timestamp"]
                    }],
                    ids=[f"marketing_{task_id}"]
                )

            return True
        except Exception as e:
            print(f"Failed to store task result: {str(e)}")
            return False

    async def query_knowledge_base(
        self,
        query: str,
        task_type: Optional[str] = None,
        n_results: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Query the knowledge base for relevant information"""
        try:
            # Determine which collections to query based on task_type
            collections_to_query = []
            if task_type == "code":
                collections_to_query = ["task_results", "code_snippets"]
            elif task_type == "design":
                collections_to_query = ["task_results", "design_assets"]
            elif task_type == "marketing":
                collections_to_query = ["task_results", "marketing_content"]
            else:
                collections_to_query = ["task_results"]

            results = []
            for collection_name in collections_to_query:
                collection = self.collections[collection_name]
                
                # Prepare query parameters
                query_params = {
                    "query_texts": [query],
                    "n_results": n_results
                }
                if metadata_filter:
                    query_params["where"] = metadata_filter

                # Execute query
                response = collection.query(**query_params)
                
                # Process results
                for idx, doc in enumerate(response["documents"][0]):
                    try:
                        # Parse document content
                        if collection_name == "task_results":
                            content = json.loads(doc)
                        else:
                            content = doc

                        # Add metadata
                        result = {
                            "content": content,
                            "metadata": response["metadatas"][0][idx],
                            "distance": response["distances"][0][idx],
                            "collection": collection_name
                        }
                        results.append(result)
                    except json.JSONDecodeError:
                        # Handle non-JSON documents
                        results.append({
                            "content": doc,
                            "metadata": response["metadatas"][0][idx],
                            "distance": response["distances"][0][idx],
                            "collection": collection_name
                        })

            # Sort results by relevance (distance)
            results.sort(key=lambda x: x["distance"])
            return results[:n_results]

        except Exception as e:
            print(f"Failed to query knowledge base: {str(e)}")
            return []

    async def get_task_history(
        self,
        task_id: Optional[str] = None,
        task_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Retrieve task execution history"""
        try:
            # Prepare query parameters
            where_clause = {}
            if task_id:
                where_clause["task_id"] = task_id
            if task_type:
                where_clause["task_type"] = task_type

            # Query task_results collection
            response = self.collections["task_results"].query(
                query_texts=[""],
                where=where_clause if where_clause else None,
                n_results=limit
            )

            # Process and return results
            results = []
            for idx, doc in enumerate(response["documents"][0]):
                try:
                    content = json.loads(doc)
                    results.append({
                        "content": content,
                        "metadata": response["metadatas"][0][idx]
                    })
                except json.JSONDecodeError:
                    continue

            return results

        except Exception as e:
            print(f"Failed to get task history: {str(e)}")
            return []

# Global RAG manager instance
rag_manager = RAGManager()
