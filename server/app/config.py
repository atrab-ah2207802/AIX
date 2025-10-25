"""
Configuration settings for the AIX CLM system
"""

class Settings:
    """Settings class for the hackathon"""
    
    # API Keys
    GEMINI_API_KEY = "AIzaSyC33f5pZ1c2TTQ0n2Ucw1zADUMm236GPH4"  
    
    # Other settings (keep your existing ones)
    OPENAI_API_KEY = "mock-key-for-testing"
    AZURE_FORM_RECOGNIZER_ENDPOINT = ""
    AZURE_FORM_RECOGNIZER_KEY = ""
    
    def __init__(self):
        pass

# Create settings instance
settings = Settings()