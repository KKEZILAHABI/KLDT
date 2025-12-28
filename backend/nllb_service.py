"""
Offline NLLB Translation Service
Uses locally downloaded model instead of API
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import os

class NLLBTranslator:
    def __init__(self):
        self.model_dir = "./nllb_model"
        
        # Check if model exists
        if not os.path.exists(self.model_dir):
            raise ValueError(
                f"Model not found at {self.model_dir}. "
                "Please run 'python download_model.py' first."
            )
        
        print("[INFO] Loading NLLB model from local directory...")
        
        try:
            # Always load to CPU first to avoid meta tensor issues
            # We'll move to GPU later if needed and possible
            self.device = "cpu"
            
            # Load tokenizer and model from local directory
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_dir,
                local_files_only=True
            )
            
            # Load model to CPU explicitly to avoid meta tensor issues
            # Don't specify torch_dtype to let it use default, which avoids meta tensor issues
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_dir,
                local_files_only=True,
                low_cpu_mem_usage=False
            )
            
            # Set to evaluation mode before any device movement
            self.model.eval()
            
            # Try to move to GPU if available (only after successful CPU load)
            if torch.cuda.is_available():
                try:
                    self.model = self.model.to("cuda")
                    self.device = "cuda"
                    print(f"[INFO] Model moved to CUDA")
                except (NotImplementedError, RuntimeError, Exception) as e:
                    error_msg = str(e).lower()
                    if "meta tensor" in error_msg or "to_empty" in error_msg:
                        print(f"[WARNING] Could not move model to CUDA (meta tensor issue), keeping on CPU")
                        self.device = "cpu"
                    else:
                        # For other errors, log but keep on CPU
                        print(f"[WARNING] Could not move model to CUDA: {e}, keeping on CPU")
                        self.device = "cpu"
            
            print(f"[INFO] Model loaded successfully on {self.device}")
            
        except Exception as e:
            raise ValueError(f"Failed to load model: {e}")
    
    def translate(self, text, source_lang, target_lang):
        """Translate text using local NLLB model"""
        from config.languages import get_language_code
        
        src_code = get_language_code(source_lang)
        tgt_code = get_language_code(target_lang)
        
        print(f"[DEBUG] Translating: '{text}' from {src_code} to {tgt_code}")
        
        try:
            # Set source language for tokenizer
            self.tokenizer.src_lang = src_code
            
            # Tokenize input
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Generate translation with target language
            translated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(tgt_code),
                max_length=512,
                num_beams=5,
                early_stopping=True
            )
            
            # Decode output
            translation = self.tokenizer.batch_decode(
                translated_tokens, 
                skip_special_tokens=True
            )[0]
            
            print(f"[DEBUG] Translation result: '{translation}'")
            return translation
            
        except KeyError as e:
            return f"Error: Language code not supported - {e}"
        except Exception as e:
            print(f"[ERROR] Translation failed: {e}")
            return "Translation failed. Please try again."