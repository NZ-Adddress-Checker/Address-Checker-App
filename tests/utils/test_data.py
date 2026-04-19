"""Test data for automated tests"""
import os
from dotenv import load_dotenv

load_dotenv()


class TestData:
    """Test data constants"""
    
    # Cognito Test Credentials
    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "test-user@example.com")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "TestPassword123!")
    INVALID_PASSWORD = "WrongPassword123!"
    
    # Test Addresses
    VALID_ADDRESS = "1 Queen Street, Auckland, 1010"
    PARTIAL_ADDRESS = "123 Main"
    INVALID_ADDRESS = "999 Fake Street, Nowhere, 9999"
    EMPTY_ADDRESS = ""
    
    # API Endpoints
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    # Timeouts
    SMALL_TIMEOUT = 3000  # 3 seconds
    MEDIUM_TIMEOUT = 5000  # 5 seconds
    LARGE_TIMEOUT = 10000  # 10 seconds
    
    @classmethod
    def get_login_credentials(cls):
        """Get test user credentials"""
        return {
            "email": cls.TEST_USER_EMAIL,
            "password": cls.TEST_USER_PASSWORD
        }
    
    @classmethod
    def get_invalid_credentials(cls):
        """Get invalid credentials"""
        return {
            "email": cls.TEST_USER_EMAIL,
            "password": cls.INVALID_PASSWORD
        }
