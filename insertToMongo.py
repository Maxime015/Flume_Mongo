import json
import time
from datetime import datetime
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Set

# Configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "flume_logs"
COLLECTION_NAME = "logs"
LOG_DIR = Path("log")
STATE_FILE = Path("processed_files.json")
POLL_INTERVAL = 5  # secondes

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

def load_processed_files() -> Set[str]:
    if STATE_FILE.exists():
        try:
            with STATE_FILE.open("r", encoding="utf-8") as f:
                return set(json.load(f))
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Erreur lors du chargement de l'état : {e}")
    return set()

def save_processed_files(processed: Set[str]) -> None:
    try:
        with STATE_FILE.open("w", encoding="utf-8") as f:
            json.dump(sorted(processed), f, indent=2)
    except IOError as e:
        print(f"❌ Erreur lors de la sauvegarde de l'état : {e}")

def is_iso_format(s: str) -> bool:
    try:
        datetime.fromisoformat(s)
        return True
    except (ValueError, TypeError):
        return False

def ensure_log_dir_exists():
    if not LOG_DIR.exists():
        print(f"📁 Dossier '{LOG_DIR}' introuvable. Création...")
        LOG_DIR.mkdir(parents=True, exist_ok=True)

def process_file(file_path: Path) -> list[dict]:
    batch = []
    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    doc = json.loads(line)
                    # Nettoyage et enrichissement
                    if not is_iso_format(doc.get("timestamp", "")):
                        doc["timestamp"] = datetime.utcnow().isoformat()
                    doc.setdefault("status", "UNKNOWN")
                    batch.append(doc)
                except json.JSONDecodeError:
                    print(f"⚠️ Erreur JSON dans {file_path.name} (ligne {line_num}) : {line}")
    except IOError as e:
        print(f"❌ Impossible de lire le fichier {file_path.name} : {e}")
    return batch

def insert_logs_to_mongo(processed_files: Set[str]):
    ensure_log_dir_exists()
    for file_path in LOG_DIR.glob("*"):
        if file_path.name in processed_files or not file_path.is_file():
            continue

        batch = process_file(file_path)

        if not batch:
            print(f"⚠️ Aucun document valide trouvé dans : {file_path.name}")
            continue

        try:
            collection.insert_many(batch, ordered=False)
            print(f"✅ {len(batch)} documents insérés depuis : {file_path.name}")
        except PyMongoError as e:
            print(f"❌ Erreur MongoDB lors de l'insertion depuis {file_path.name} : {e}")
            continue  # on NE marque PAS le fichier comme traité
        else:
            processed_files.add(file_path.name)
            save_processed_files(processed_files)
            print(f"📝 Fichier marqué comme traité : {file_path.name}")



def main():
    print("📡 Surveillance du dossier 'log/' en cours...")
    processed_files = load_processed_files()
    while True:
        insert_logs_to_mongo(processed_files)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

