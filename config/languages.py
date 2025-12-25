# Language configuration
SUPPORTED_LANGUAGES = {
    "english": {
        "code": "eng_Latn",
        "name": "English",
        "native": "English"
    },
    "swahili": {
        "code": "swh_Latn", 
        "name": "Swahili",
        "native": "Kiswahili"
    },
    "luo": {
        "code": "luo_Latn",
        "name": "Luo",
        "native": "Dholuo"
    },
    "kikuyu": {
        "code": "kik_Latn",
        "name": "Kikuyu", 
        "native": "Gikuyu"
    }
}

def get_language_code(language_key):
    """Get NLLB language code"""
    return SUPPORTED_LANGUAGES.get(language_key, {}).get("code", "eng_Latn")

def get_language_name(language_key):
    """Get display name"""
    return SUPPORTED_LANGUAGES.get(language_key, {}).get("name", "English")