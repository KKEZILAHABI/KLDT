import requests
import os
from backend.nllb_service import NLLBTranslator
from backend.phrase_database import PhraseDatabase

class TranslationEngine:
    def __init__(self):
        self.phrase_db = PhraseDatabase()
        self.nllb = NLLBTranslator()
    
    def translate(self, text, source_lang, target_lang):
        """Main translation method"""
        # 1. Check phrase database
        phrase_trans = self.phrase_db.lookup(text, source_lang, target_lang)
        if phrase_trans:
            return phrase_trans
        
        # 2. Try NLLB (primary)
        try:
            return self.nllb.translate(text, source_lang, target_lang)
        except Exception as e:
            print(f"NLLB failed: {e}")
            return "Translation temporarily unavailable"
            # 3. Fallback to Google
    
    def get_languages(self):
        """Return supported languages"""
        return self.phrase_db.get_supported_languages()