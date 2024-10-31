# Exécuter le lot4

Assurez-vous d'avoir : voir => Mettre en place l'espace de travail dans la VM + Hadoop dans le fichier README.md

1. Lancer les services Hadoop + HBase
2. Créer le répertoire input et transférer le fichier de cleaned_data.csv
3. Remplacer les variable pour Elasticsearch + HBase

# Connexion Elasticsearch ligne 37 - 38
ELASTIC_USER = "*****"
ELASTIC_PASSWORD = "******"

# Connexion à HBase ligne 96 - 97 
HBASE_HOST = '*******'
HBASE_PORT = *****


Sur le terminal de votre ide préféré excécuter la commande suivante 
```bash
cd lot4
python .\lot4\connexion_elastiseach.py

```