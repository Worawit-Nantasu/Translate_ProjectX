import os
import sys
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Adjust sys.path to include the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils import translate_content, count_translatable_strings
from config.settings import SOURCE_LANG, TARGET_LANG

# ตั้งค่า logging
logging.basicConfig(
    filename=os.path.join(parent_dir, 'logs', 'translation.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def translate_json(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logging.info(f"Successfully loaded input file: {input_path}")

        total_strings = count_translatable_strings(data)
        with tqdm(total=total_strings, desc=f"Translating {os.path.basename(input_path)}", unit="string") as progress_bar:
            translated_data = translate_content(data, progress_bar)

        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(translated_data, file, ensure_ascii=False, indent=4)
            logging.info(f"Successfully saved translated file: {output_path}")

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON file: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def translate_multiple_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    def process_file(input_file):
        try:
            input_path = os.path.join(input_dir, input_file)
            output_path = os.path.join(output_dir, input_file)
            logging.info(f"Processing file: {input_file}")
            translate_json(input_path, output_path)
        except Exception as e:
            logging.error(f"Failed to process file: {input_file}. Error: {e}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(process_file, input_files))

if __name__ == "__main__":
    # ตั้งค่า directories
    input_dir = os.path.join(parent_dir, 'data', 'input')
    output_dir = os.path.join(parent_dir, 'data', 'output')

    # เริ่มการแปล
    translate_multiple_files(input_dir, output_dir)
