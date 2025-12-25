import json
import os

class PhraseDatabase:
    def __init__(self):
        self.data_file = "data/common_phrases.json"
        self.phrases = self._load_phrases()
    
    def _load_phrases(self):
        """Load phrases from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default structure if file doesn't exist
            return {
                "greetings": [],
                "common": [],
                "emergency": [],
                "healthcare": []
            }
    
    def lookup(self, text, source_lang, target_lang):
        """Look up a phrase in the database"""
        text_lower = text.lower().strip()
        
        for category in self.phrases.values():
            for phrase in category:
                if phrase.get(source_lang, "").lower() == text_lower:
                    return phrase.get(target_lang)
        
        return None
    
    def get_categories(self):
        """Return available categories"""
        return list(self.phrases.keys())
    
    def get_phrases_by_category(self, category):
        """Return phrases for a specific category"""
        return self.phrases.get(category, [])
    
    def get_supported_languages(self):
        """Return all languages that have at least one phrase"""
        languages = set()
        for category in self.phrases.values():
            for phrase in category:
                languages.update(phrase.keys())
        return list(languages)