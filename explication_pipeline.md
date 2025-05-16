
    # 📦 Projet de Simulation Big Data avec Flume, MongoDB et Flask

    ## 🧠 Objectif du Projet

    Ce projet permet de :
    - Générer massivement des logs aléatoires
    - Les faire transiter via Apache Flume
    - Les stocker dans MongoDB
    - Les visualiser dynamiquement via Flask + Chart.js
    - Et les explorer via MongoDB Compass

    C’est une architecture orientée **ingestion de données en continu**, typique des systèmes Big Data.



    ## 🔁 Pipeline Global


    Python (sendlogs.py) 
        ↓ (TCP)
    Flume (Netcat source) 
        ↓ (Sink → fichiers)
    Fichiers (dans /flume/log)
        ↓
    Script Python (insertToMongo.py)
        ↓
    MongoDB
        ↓
    Flask Dashboard (Chart.js)




      🧱 Composants et Rôles

      ✅ 1. Docker (optionnel mais recommandé)
    - Permet de lancer les services Flume, MongoDB, Flask facilement
    - Permet d’utiliser un `docker-compose.yml` pour tout automatiser

      ✅ 2. Apache Flume
    - Agent d’ingestion de données
    - Source `netcat` (port 44444) qui reçoit des logs via TCP
    - Sink `file_roll` qui écrit les logs dans `/flume/log`

      ✅ 3. MongoDB + Script Python
    - Le script `insertToMongo.py` lit les fichiers Flume et insère les logs dans MongoDB
    - Utilise `insert_many` pour insérer efficacement par lots

      ✅ 4. MongoDB Compass
    - Interface visuelle pour naviguer et filtrer les données dans MongoDB

      ✅ 5. Flask + Chart.js Dashboard
    - Flask expose une API `/api/data` pour regrouper les logs
    - Le frontend (Chart.js + TailwindCSS) affiche :
      - Un graphique linéaire (événements/minute)
      - Un graphique circulaire (répartition par statut)
    - Interface responsive, rafraîchie automatiquement toutes les 10 secondes




     📊 Résumé

    Ce projet permet de :

    - Simuler des flux **massifs** de logs
    - Observer leur ingestion temps réel
    - Visualiser leur état dans un dashboard moderne
    - Étendre facilement vers des technologies Big Data plus avancées

