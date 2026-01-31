"""
Firebase Admin SDK initialization and configuration.
"""

import firebase_admin
from firebase_admin import credentials, auth
from .settings import settings
from loguru import logger


class FirebaseConfig:
    """Firebase configuration and initialization."""
    
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """Initialize Firebase Admin SDK."""
        if cls._initialized:
            logger.info("Firebase already initialized")
            return
        
        try:
            # Create credentials from settings
            cred_dict = {
                "type": "service_account",
                "project_id": settings.FIREBASE_PROJECT_ID,
                "private_key": settings.FIREBASE_PRIVATE_KEY,
                "client_email": settings.FIREBASE_CLIENT_EMAIL,
                "token_uri": "https://oauth2.googleapis.com/token",
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            
            cls._initialized = True
            logger.info(f"Firebase initialized for project: {settings.FIREBASE_PROJECT_ID}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify Firebase ID token.
        
        Args:
            token: Firebase ID token from client
            
        Returns:
            Decoded token with user information
            
        Raises:
            ValueError: If token is invalid
        """
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception as e:
            logger.warning(f"Token verification failed: {str(e)}")
            raise ValueError(f"Invalid authentication token: {str(e)}")
    
    @staticmethod
    def get_user(uid: str):
        """
        Get user by UID.
        
        Args:
            uid: Firebase user ID
            
        Returns:
            UserRecord object
        """
        try:
            user = auth.get_user(uid)
            return user
        except Exception as e:
            logger.error(f"Failed to get user {uid}: {str(e)}")
            raise


# Initialize on import
firebase_config = FirebaseConfig()
