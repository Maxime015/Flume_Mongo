import socket
import json
import random
import string
from datetime import datetime
import time
import os

HOST = 'localhost'
PORT = 44444
LOG_DIR = 'log'

def generate_random_log():
    return {
        "event": ''.join(random.choices(string.ascii_lowercase, k=10)),
        "status": random.choice(["ok", "error", "warning"]),
        "timestamp": datetime.utcnow().isoformat(),
        "value": round(random.uniform(0, 1000), 2),
        "user": ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    }

# Créer le dossier log s'il n'existe pas
os.makedirs(LOG_DIR, exist_ok=True)

# Générer un nom unique de fichier log
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = os.path.join(LOG_DIR, f"log_{timestamp_str}.txt")

# Paramètres de simulation
TOTAL_MESSAGES = 6500
BATCH_SIZE = 500
DELAY_BETWEEN_BATCHES = 0.05  # facultatif

start = time.time()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, open(log_file_path, "w", encoding="utf-8") as log_file:
        s.connect((HOST, PORT))
        for i in range(0, TOTAL_MESSAGES, BATCH_SIZE):
            for _ in range(BATCH_SIZE):
                log = generate_random_log()
                message = json.dumps(log)
                s.sendall((message + "\n").encode('utf-8'))
                log_file.write(message + "\n")
            print(f"✅ Batch envoyé : {i + BATCH_SIZE}/{TOTAL_MESSAGES}")
            time.sleep(DELAY_BETWEEN_BATCHES)
except Exception as e:
    print(f"❌ Erreur lors de l'envoi : {e}")

end = time.time()
duration = end - start

print("\n📊 Résumé Benchmark")
print(f"⏱️ Temps total     : {duration:.2f} secondes")
print(f"📦 Messages envoyés : {TOTAL_MESSAGES}")
print(f"⚡ Débit moyen      : {TOTAL_MESSAGES / duration:.2f} messages/sec")
print(f"📝 Fichier log généré : {log_file_path}")

