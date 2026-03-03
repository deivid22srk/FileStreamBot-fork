import json
import os
from datetime import datetime

JSON_PATH = "filestream_data.json"

def init_json():
    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)

def add_file_json(file_id, sender_id, secret_code, file_name, file_size, mime_type, dl_link, stream_link=None, direct_link=None):
    init_json()
    
    new_entry = {
        "file_id": file_id,
        "sender_id": sender_id,
        "secret_code": secret_code,
        "file_name": file_name,
        "file_size": file_size,
        "mime_type": mime_type,
        "dl_link": dl_link,
        "stream_link": stream_link,
        "direct_link": direct_link,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        with open(JSON_PATH, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            # Evitar duplicatas
            data = [entry for entry in data if entry["file_id"] != file_id]
            data.append(new_entry)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()
        print(f"JSON DB: File {file_name} saved successfully.")
    except Exception as e:
        print(f"JSON DB Error: {e}")

def get_all_files_json():
    init_json()
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []
