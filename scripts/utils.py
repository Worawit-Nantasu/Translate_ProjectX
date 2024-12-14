import os
import sys
import logging
import time
from threading import Lock
from deep_translator import GoogleTranslator

# Adjust sys.path to include the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config.settings import DO_NOT_TRANSLATE_KEYS, SOURCE_LANG, TARGET_LANG

# ล็อกสำหรับจัดการแคช
cache_lock = Lock()
translation_cache = {}

def safe_translate(content, retries=3, delay=5, timeout=10):
    """
    Translate text with retry mechanism and timeout.
    """
    for attempt in range(retries):
        try:
            translated = GoogleTranslator(
                source=SOURCE_LANG, target=TARGET_LANG, timeout=timeout
            ).translate(content)
            return translated
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    logging.error(f"Failed to translate after {retries} attempts: {content}")
    return content  # Return the original content if all retries fail

def translate_content(content, progress_bar=None, current_key=None):
    if isinstance(content, dict):
        translated_dict = {}
        for key, value in content.items():
            if key in DO_NOT_TRANSLATE_KEYS:
                translated_dict[key] = value  # ไม่ต้องแปลคีย์นี้
            elif key == 'full_href':
                if isinstance(value, str):
                    # แทนที่ '/en/' ด้วย '/hi/' หรือภาษาปลายทาง
                    translated_value = value.replace(f'/{SOURCE_LANG}/', f'/{TARGET_LANG}/')
                    translated_dict[key] = translated_value
                else:
                    translated_dict[key] = value
            else:
                translated_dict[key] = translate_content(value, progress_bar, current_key=key)
        return translated_dict
    elif isinstance(content, list):
        return [translate_content(item, progress_bar, current_key=current_key) for item in content]
    elif isinstance(content, str):
        with cache_lock:
            if content in translation_cache:
                return translation_cache[content]
        translated = safe_translate(content)
        with cache_lock:
            translation_cache[content] = translated
        if progress_bar:
            progress_bar.update(1)
        return translated
    else:
        return content

def count_translatable_strings(content):
    if isinstance(content, dict):
        return sum(count_translatable_strings(value) for key, value in content.items() if key not in DO_NOT_TRANSLATE_KEYS)
    elif isinstance(content, list):
        return sum(count_translatable_strings(item) for item in content)
    elif isinstance(content, str):
        return 1
    return 0
