"""
Groq API service for LLM interactions.
Handles chat completions and streaming responses.
"""

from typing import AsyncGenerator, List, Dict, Any, Optional
from groq import AsyncGroq
from loguru import logger

from app.config.settings import settings


class GroqService:
    """Service for interacting with Groq API."""
    
    def __init__(self):
        """Initialize Groq client."""
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.max_tokens = settings.GROQ_MAX_TOKENS
        self.temperature = settings.GROQ_TEMPERATURE
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Get non-streaming chat completion.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (overrides default)
            max_tokens: Maximum tokens to generate (overrides default)
            
        Returns:
            Complete response text
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            
            content = response.choices[0].message.content
            logger.info(f"Generated response: {len(content)} chars")
            return content
            
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise
    
    async def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Get streaming chat completion.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (overrides default)
            max_tokens: Maximum tokens to generate (overrides default)
            
        Yields:
            Response text chunks
        """
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=True,
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
            logger.info("Streaming response completed")
            
        except Exception as e:
            logger.error(f"Groq streaming error: {str(e)}")
            raise
    
    async def analyze_medical_report(
        self,
        report_text: str,
        user_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze medical report using Groq LLM.
        
        Args:
            report_text: Extracted text from medical report
            user_context: Optional user context (age, medical history, etc.)
            
        Returns:
            Dictionary with analysis results
        """
        try:
            system_prompt = """You are a medical AI assistant specialized in analyzing medical reports.
Your role is to:
1. Extract key medical metrics (blood pressure, cholesterol, glucose, etc.)
2. Identify abnormal values
3. Provide simple, clear explanations
4. Give actionable health recommendations

Format your response as JSON with these keys:
- summary: Brief overview of the report
- key_findings: List of important findings
- abnormal_values: List of values outside normal range with explanations
- recommendations: List of health recommendations
- risk_assessment: Overall health risk level (low, moderate, high)
"""
            
            user_message = f"Analyze this medical report:\n\n{report_text}"
            if user_context:
                user_message += f"\n\nPatient context: {user_context}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = await self.chat_completion(messages, temperature=0.3)
            
            # Parse JSON response
            import json
            try:
                analysis = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, wrap in summary
                analysis = {
                    "summary": response,
                    "key_findings": [],
                    "abnormal_values": [],
                    "recommendations": [],
                    "risk_assessment": "unknown"
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Report analysis error: {str(e)}")
            raise
    
    def build_medical_chat_context(
        self,
        user_question: str,
        chat_history: List[Dict[str, str]],
        medical_reports: Optional[List[str]] = None,
        rag_context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Build context for medical chat.
        
        Args:
            user_question: Current user question
            chat_history: Previous chat messages
            medical_reports: User's medical report summaries
            rag_context: Retrieved medical knowledge from vector DB
            
        Returns:
            List of formatted messages for LLM
        """
        system_prompt = """You are MedicoChatbot, a friendly and knowledgeable AI medical assistant.
Your role is to help users understand their health reports and answer medical questions in simple, easy-to-understand language.

Guidelines:
- Use simple words, avoid complex medical jargon
- When explaining medical terms, use analogies and examples
- Always be supportive and encouraging
- Never provide definitive diagnoses - recommend consulting healthcare providers
- Focus on education and understanding
- Use emojis occasionally to be friendly (but not excessively)
"""
        
        # Add user's medical context if available
        if medical_reports:
            reports_text = "\n\n".join(medical_reports)
            system_prompt += f"\n\nUser's Medical Reports:\n{reports_text}"
        
        # Add RAG context if available
        if rag_context:
            system_prompt += f"\n\nRelevant Medical Knowledge:\n{rag_context}"
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent chat history (last 10 messages)
        messages.extend(chat_history[-10:])
        
        # Add current question
        messages.append({"role": "user", "content": user_question})
        
        logger.debug(f"Built chat context with {len(messages)} messages")
        return messages


# Global instance
groq_service = GroqService()
