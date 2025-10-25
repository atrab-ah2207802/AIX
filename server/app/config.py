# """
# Configuration settings for the AIX CLM system
# """

# class Settings:
#     """Settings class for the hackathon"""
    
#     # API Keys
#     GEMINI_API_KEY = "AIzaSyC33f5pZ1c2TTQ0n2Ucw1zADUMm236GPH4"  
    
#     # Other settings (keep your existing ones)
#     OPENAI_API_KEY = "mock-key-for-testing"
#     AZURE_FORM_RECOGNIZER_ENDPOINT = ""
#     AZURE_FORM_RECOGNIZER_KEY = ""
    
#     def __init__(self):
#         pass

# # Create settings instance
#settings = Settings()
"""
Configuration - SECURE VERSION
"""
import os

class Settings:
    def __init__(self):
        # LOAD FROM ENVIRONMENT VARIABLE
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        
        if not self.GEMINI_API_KEY:
            print("❌ WARNING: GEMINI_API_KEY environment variable not set!")
            print("   Run: export GEMINI_API_KEY='your-actual-key-here'")

settings = Settings()
# """
# Configuration - Updated for OpenRouter
# """
# import os

# class Settings:
#     def __init__(self):
#         # OpenRouter API Key
#         self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
        
#         if not self.OPENROUTER_API_KEY:
#             print("❌ WARNING: OPENROUTER_API_KEY environment variable not set!")
#             print("   Get free key from: https://openrouter.ai/")
#             print("   Then run: export OPENROUTER_API_KEY='your-key-here'")

# settings = Settings()