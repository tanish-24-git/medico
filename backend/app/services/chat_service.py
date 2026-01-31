"""
Chat service for orchestrating AI conversations.
Combines chat history, RAG context, and user reports.
"""

from typing import AsyncGenerator, Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.models.user import User
from app.models.chat import ChatSession, ChatMessage, MessageRole
from app.models.report import MedicalReport
from app.services.groq_service import groq_service
from app.services.pinecone_service import pinecone_service


class ChatService:
    """Service for managing chat conversations."""
    
    async def get_or_create_session(
        self,
        user: User,
        session_id: Optional[int],
        db: AsyncSession
    ) -> ChatSession:
        """
        Get existing session or create new one.
        
        Args:
            user: Current user
            session_id: Optional session ID
            db: Database session
            
        Returns:
            ChatSession object
        """
        try:
            if session_id:
                # Get existing session
                result = await db.execute(
                    select(ChatSession).where(
                        ChatSession.id == session_id,
                        ChatSession.user_id == user.id
                    )
                )
                session = result.scalar_one_or_none()
                
                if not session:
                    raise ValueError(f"Session {session_id} not found for user")
                
                return session
            else:
                # Create new session
                session = ChatSession(user_id=user.id)
                db.add(session)
                await db.commit()
                await db.refresh(session)
                
                logger.info(f"Created new chat session: {session.id}")
                return session
                
        except Exception as e:
            logger.error(f"Session retrieval error: {str(e)}")
            raise
    
    async def get_chat_history(
        self,
        session: ChatSession,
        db: AsyncSession,
        limit: int = 20
    ) -> List[Dict[str, str]]:
        """
        Get formatted chat history for LLM.
        
        Args:
            session: Chat session
            db: Database session
            limit: Maximum messages to retrieve
            
        Returns:
            List of message dicts with role and content
        """
        try:
            result = await db.execute(
                select(ChatMessage)
                .where(ChatMessage.session_id == session.id)
                .order_by(ChatMessage.created_at.desc())
                .limit(limit)
            )
            messages = result.scalars().all()
            
            # Reverse to get chronological order
            messages = list(reversed(messages))
            
            # Format for LLM
            formatted = [
                {"role": msg.role.value, "content": msg.content}
                for msg in messages
            ]
            
            return formatted
            
        except Exception as e:
            logger.error(f"Chat history retrieval error: {str(e)}")
            return []
    
    async def get_user_reports_summary(
        self,
        user: User,
        db: AsyncSession,
        limit: int = 5
    ) -> List[str]:
        """
        Get summaries of user's recent medical reports.
        
        Args:
            user: Current user
            db: Database session
            limit: Number of reports to include
            
        Returns:
            List of report summaries
        """
        try:
            result = await db.execute(
                select(MedicalReport)
                .where(MedicalReport.user_id == user.id)
                .where(MedicalReport.ai_summary.isnot(None))
                .order_by(MedicalReport.created_at.desc())
                .limit(limit)
            )
            reports = result.scalars().all()
            
            summaries = []
            for report in reports:
                summary = f"Report from {report.created_at.strftime('%Y-%m-%d')}: {report.ai_summary}"
                summaries.append(summary)
            
            return summaries
            
        except Exception as e:
            logger.error(f"Reports summary error: {str(e)}")
            return []
    
    async def get_rag_context(
        self,
        query: str,
        user_id: int,
        include_user_reports: bool = True
    ) -> Optional[str]:
        """
        Get relevant context from vector database (RAG).
        
        Args:
            query: User question
            user_id: User ID
            include_user_reports: Include user's personal reports
            
        Returns:
            Combined context string
        """
        try:
            # Search Pinecone
            results = await pinecone_service.search_medical_knowledge(
                query=query,
                user_id=user_id if include_user_reports else None,
                top_k=3
            )
            
            if not results:
                return None
            
            # Combine results
            context_parts = []
            for i, result in enumerate(results, 1):
                context_parts.append(f"{i}. {result['text']}")
            
            context = "\n\n".join(context_parts)
            return context
            
        except Exception as e:
            logger.error(f"RAG context retrieval error: {str(e)}")
            return None
    
    async def save_message(
        self,
        session: ChatSession,
        role: MessageRole,
        content: str,
        db: AsyncSession
    ) -> ChatMessage:
        """
        Save message to database.
        
        Args:
            session: Chat session
            role: Message role
            content: Message content
            db: Database session
            
        Returns:
            Saved ChatMessage object
        """
        try:
            message = ChatMessage(
                session_id=session.id,
                role=role,
                content=content
            )
            db.add(message)
            await db.commit()
            await db.refresh(message)
            
            return message
            
        except Exception as e:
            logger.error(f"Message save error: {str(e)}")
            raise
    
    async def generate_session_title(
        self,
        first_message: str,
        db: AsyncSession,
        session: ChatSession
    ) -> None:
        """
        Generate descriptive title for chat session.
        
        Args:
            first_message: First user message
            db: Database session
            session: Chat session to update
        """
        try:
            # Simple title generation - first 50 chars
            title = first_message[:50]
            if len(first_message) > 50:
                title += "..."
            
            session.title = title
            await db.commit()
            
        except Exception as e:
            logger.error(f"Title generation error: {str(e)}")
    
    async def chat_stream(
        self,
        user: User,
        message: str,
        session_id: Optional[int],
        include_reports: bool,
        db: AsyncSession
    ) -> AsyncGenerator[Dict, None]:
        """
        Stream chat response.
        
        Args:
            user: Current user
            message: User message
            session_id: Optional session ID
            include_reports: Include user reports in context
            db: Database session
            
        Yields:
            Response chunks
        """
        try:
            # Get or create session
            session = await self.get_or_create_session(user, session_id, db)
            
            # Save user message
            await self.save_message(session, MessageRole.USER, message, db)
            
            logger.info(f"Starting chat stream for session {session.id}, message length: {len(message)}")

            
            # Generate title for new session
            if not session.title:
                await self.generate_session_title(message, db, session)
            
            # Get chat history
            history = await self.get_chat_history(session, db)
            
            # Get user reports summary
            reports = []
            if include_reports:
                reports = await self.get_user_reports_summary(user, db)
            
            # Get RAG context
            rag_context = await self.get_rag_context(
                message,
                user.id,
                include_reports
            )
            
            logger.info(f"RAG context retrieved: {'Yes' if rag_context else 'No'}, User reports: {'Yes' if reports else 'No'}")

            # Build context for LLM
            messages = groq_service.build_medical_chat_context(
                user_question=message,
                chat_history=history,
                medical_reports=reports if reports else None,
                rag_context=rag_context
            )
            
            # Stream response from Groq
            full_response = ""
            async for chunk in groq_service.chat_completion_stream(messages):
                full_response += chunk
                yield {
                    "content": chunk,
                    "done": False,
                    "session_id": session.id
                }
            
            # Save assistant response
            assistant_message = await self.save_message(
                session,
                MessageRole.ASSISTANT,
                full_response,
                db
            )
            
            # Send final chunk
            yield {
                "content": "",
                "done": True,
                "session_id": session.id,
                "message_id": assistant_message.id
            }
            
        except Exception as e:
            logger.error(f"Chat stream error: {str(e)}")
            yield {
                "content": f"Error: {str(e)}",
                "done": True,
                "error": True
            }


# Global instance
chat_service = ChatService()
