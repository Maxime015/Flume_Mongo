
# 📦 Projet de Simulation Big Data avec Flume, MongoDB et Flask

## 🧠 Objectif du Projet

Ce projet a pour but de simuler un pipeline d’ingestion de données en continu, typique des architectures **Big Data temps réel**. Il permet de :

- Générer un grand volume de logs aléatoires
- Les acheminer via **Apache Flume**
- Les stocker efficacement dans **MongoDB**
- Les visualiser dynamiquement grâce à **Flask** et **Chart.js**
- Les explorer en profondeur via **MongoDB Compass**

---

## 🔁 Architecture du Pipeline

```text
Python (sendlogs.py)
        ↓ (TCP)
Apache Flume (source Netcat)
        ↓ (Sink → fichiers)
Fichiers (/flume/log)
        ↓
Python (insertToMongo.py)
        ↓
MongoDB
        ↓
Flask + Chart.js (Dashboard)
```

---

## 🧱 Composants et Rôles

### ✅ 1. Docker (optionnel mais recommandé)
- Simplifie le déploiement des services Flume, MongoDB et Flask
- Utilisation d’un fichier `docker-compose.yml` pour tout orchestrer automatiquement

### ✅ 2. Apache Flume
- Agent d’ingestion configuré avec :
  - Une **source Netcat** (port `44444`) recevant les logs via TCP
  - Un **sink `file_roll`** écrivant les logs dans `/flume/log`

### ✅ 3. MongoDB + Script Python
- Le script `insertToMongo.py` lit les fichiers générés par Flume
- Insère les logs en **batch** dans MongoDB via `insert_many` pour plus d'efficacité

### ✅ 4. MongoDB Compass
- Interface graphique pour **explorer, trier et filtrer** les données insérées

### ✅ 5. Dashboard Flask + Chart.js
- Une API REST (`/api/data`) expose les données pour le frontend
- Interface web responsive avec :
  - 📈 Un graphique linéaire : nombre d’événements par minute
  - 🥧 Un graphique circulaire : répartition des logs par statut
- Mise à jour automatique toutes les **10 secondes**

---

## 📊 Résumé

Ce projet constitue un socle idéal pour :

- Simuler des flux **massifs et continus** de données
- Tester et observer les mécanismes d’ingestion temps réel
- Visualiser l’état des données via un **dashboard moderne**
- Étendre facilement le système vers des solutions plus avancées (Kafka, Spark, Elastic, etc.)
