# 🇰🇪 Kenyan Local Dialect Translator - Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the Translation Model and necessary Files
https://huggingface.co/facebook/nllb-200-distilled-600M/tree/main
(No need for readme and gitattributes)

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
your_project/
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore file
├── nllb_model/                # Downloaded model (NOT in Git)
│   ├── config.json
│   ├── tokenizer.json
│   ├── pytorch_model.bin      # ~2.5GB
│   └── ...
├── backend/
│   ├── nllb_service.py        # Offline translation engine
│   ├── translation_engine.py
│   ├── phrase_database.py
│   └── voice_service.py       # Voice input/output
├── frontend/
│   ├── chat_interface.py
│   ├── language_selector.py
│   ├── quick_phrases.py
│   └── ui_main.py
└── config/
    └── languages.py
```

---

## ⚠️ Important Notes

### Model Size & Git

The NLLB model is **~2.5GB** and should **NOT** be committed to Git:

- ✅ The model is in `.gitignore`
- ❌ Don't force-add it to Git