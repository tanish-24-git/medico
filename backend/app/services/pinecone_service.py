"""
Pinecone vector database service for medical knowledge retrieval (RAG).
"""

from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from loguru import logger
from sentence_transformers import SentenceTransformer

from app.config.settings import settings


class PineconeService:
    """Service for vector database operations with Pinecone."""
    
    def __init__(self):
        """Initialize Pinecone client and embedding model."""
        try:
            # Initialize Pinecone
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Get or create index
            self.index_name = settings.PINECONE_INDEX_NAME
            self._ensure_index_exists()
            
            self.index = self.pc.Index(self.index_name)
            
            # Initialize embedding model (using sentence-transformers)
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.dimension = 384  # Dimension for all-MiniLM-L6-v2
            
            logger.info(f"Pinecone initialized with index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Pinecone initialization failed: {str(e)}")
            raise
    
    def _ensure_index_exists(self):
        """Create Pinecone index if it doesn't exist."""
        try:
            existing_indexes = [idx.name for idx in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=384,  # Dimension for all-MiniLM-L6-v2
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region=settings.PINECONE_ENVIRONMENT
                    )
                )
                logger.info(f"Index {self.index_name} created successfully")
            else:
                logger.info(f"Index {self.index_name} already exists")
                
        except Exception as e:
            logger.warning(f"Could not create index (might already exist): {str(e)}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Embedding generation error: {str(e)}")
            raise
    
    async def upsert_medical_knowledge(
        self,
        doc_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add medical knowledge to vector database.
        
        Args:
            doc_id: Unique document ID
            text: Medical knowledge text
            metadata: Optional metadata (source, category, etc.)
            
        Returns:
            Success status
        """
        try:
            logger.info(f"Generating embedding for doc_id: {doc_id}")
            # Generate embedding
            embedding = self.generate_embedding(text)
            
            # Prepare metadata
            meta = metadata or {}
            meta['text'] = text[:500]  # Store snippet for quick reference
            
            # Upsert to Pinecone
            self.index.upsert(
                vectors=[{
                    'id': doc_id,
                    'values': embedding,
                    'metadata': meta
                }]
            )
            
            logger.info(f"Upserted document: {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"Upsert error: {str(e)}")
            return False
    
    async def upsert_user_report(
        self,
        report_id: int,
        user_id: int,
        report_text: str,
        report_summary: Optional[str] = None
    ) -> bool:
        """
        Index user's medical report for personalized retrieval.
        
        Args:
            report_id: Report database ID
            user_id: User ID
            report_text: Full report text
            report_summary: AI-generated summary
            
        Returns:
            Success status
        """
        try:
            text_to_embed = report_summary if report_summary else report_text
            doc_id = f"user_{user_id}_report_{report_id}"
            
            metadata = {
                'user_id': user_id,
                'report_id': report_id,
                'type': 'user_report'
            }
            
            return await self.upsert_medical_knowledge(doc_id, text_to_embed, metadata)
            
        except Exception as e:
            logger.error(f"Report indexing error: {str(e)}")
            return False
    
    async def search_medical_knowledge(
        self,
        query: str,
        user_id: Optional[int] = None,
        top_k: int = 5,
        include_user_reports: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant medical knowledge.
        
        Args:
            query: Search query
            user_id: Optional user ID to include their reports
            top_k: Number of results to return
            include_user_reports: Whether to include user's personal reports
            
        Returns:
            List of matching documents with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            
            # Build filter
            filter_dict = {}
            if user_id and include_user_reports:
                # Search both general knowledge and user's reports
                filter_dict = None  # No filter - search all
            elif user_id:
                # Only general knowledge (exclude user reports)
                filter_dict = {"type": {"$ne": "user_report"}}
            
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict
            )
            
            # Format results
            matches = []
            for match in results.matches:
                matches.append({
                    'id': match.id,
                    'score': match.score,
                    'text': match.metadata.get('text', ''),
                    'metadata': match.metadata
                })
            
            logger.info(f"Found {len(matches)} matches for query")
            return matches
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    async def delete_user_reports(self, user_id: int) -> bool:
        """
        Delete all reports for a user from vector database.
        
        Args:
            user_id: User ID
            
        Returns:
            Success status
        """
        try:
            # Delete by filter
            self.index.delete(filter={'user_id': user_id, 'type': 'user_report'})
            logger.info(f"Deleted reports for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Delete error: {str(e)}")
            return False


# Global instance
pinecone_service = PineconeService()
