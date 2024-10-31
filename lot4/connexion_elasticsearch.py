import happybase
import pandas as pd
from elasticsearch import Elasticsearch, helpers

"""
Script de migration de données depuis HBase vers Elasticsearch.

Ce script effectue les opérations suivantes :
1. Connexion à Elasticsearch.
2. Vérification de la connexion Elasticsearch et suppression de l'index existant (si nécessaire).
3. Création d'un index Elasticsearch avec un mapping spécifique pour les données.
4. Connexion à HBase et récupération de toutes les données de la table 'fromagerie'.
5. Nettoyage et transformation des données en format JSON compatible avec Elasticsearch.
6. Insertion des données par lots de 500 documents dans l'index Elasticsearch.

Configuration :
- Adresse d'Elasticsearch: `http://localhost:9200`
- Nom de l'index Elasticsearch : `dataw_fro03`
- Adresse HBase : `'node183722-env-1839015-2024-m05-etudiant08.sh1.hidora.com'` (port 11986)
- Table HBase : `fromagerie`

Fonctionnalités :
- Vérifie l'existence de l'index dans Elasticsearch et le recrée si nécessaire.
- Récupère les données de HBase, nettoie les champs, et les convertit au format JSON pour l'insertion dans Elasticsearch.
- Insère les données en utilisant des lots pour optimiser la performance et gérer les erreurs d'indexation.

Exceptions :
- Gère les erreurs de connexion HBase et Elasticsearch.
- Gère les erreurs d'indexation en affichant les documents échoués.

"""


# Connexion Elasticsearch
ELASTIC_ADDRESS_HOST = "http://localhost:9200"
ELASTIC_INDEX_NAME = "dataw_fro03"
ELASTIC_USER = "*****"
ELASTIC_PASSWORD = "******"

es_connect = Elasticsearch(
    [ELASTIC_ADDRESS_HOST],
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
)

# Vérification de la connexion Elasticsearch
if not es_connect.ping():
    raise ValueError("Connexion à Elasticsearch échouée")

# Vérification de l'existence de l'index et suppression s'il existe
if es_connect.indices.exists(index=ELASTIC_INDEX_NAME):
    es_connect.indices.delete(index=ELASTIC_INDEX_NAME)
    print(f"L'index '{ELASTIC_INDEX_NAME}' a été supprimé.")

# Création d'un nouvel index avec le mapping modifié
index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "codcli": {"type": "integer"},
            "genrecli": {"type": "keyword"},
            "nomcli": {"type": "keyword"},
            "prenomcli": {"type": "keyword"},
            "cpcli": {"type": "keyword"},
            "villecli": {"type": "keyword"},
            "codcde": {"type": "integer"},
            "datcde": {"type": "date", "format": "yyyy-MM-dd"},
            "timbrecli": {"type": "float"},
            "timbrecde": {"type": "float"},
            "Nbcolis": {"type": "integer"},
            "cheqcli": {"type": "float"},
            "barchive": {"type": "boolean"},
            "bstock": {"type": "boolean"},
            "codobj": {"type": "integer"},
            "qte": {"type": "integer"},
            "Colis": {"type": "integer"},
            "libobj": {"type": "keyword"},
            "Tailleobj": {"type": "keyword"},
            "Poidsobj": {"type": "float"},
            "points": {"type": "integer"},
            "indispobj": {"type": "boolean"},
            "libcondit": {"type": "keyword"},
            "prixcond": {"type": "float"},
            "puobj": {"type": "float"}
        }
    }
}

# Création de l'index
es_connect.indices.create(index=ELASTIC_INDEX_NAME, body=index_settings)
print(f"Index '{ELASTIC_INDEX_NAME}' créé avec succès.")

# Connexion à HBase
HBASE_HOST = '*******'
HBASE_PORT = *****
connection = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
table = connection.table('fromagerie')


def get_data_hbase():
    """
    Récupère toutes les données de la table 'fromagerie' de HBase et les convertit en un DataFrame pandas.
    
    Retourne :
        pd.DataFrame : Les données de HBase sous forme de DataFrame.
    """
    data_list = []
    for key, data in table.scan():
        # Nettoyage préfixe "details:" - décodage des valeurs
        data_cleaned = {k.decode().split(':')[1]: v.decode('utf-8', errors='ignore') for k, v in data.items()}
        data_list.append(data_cleaned)
    return pd.DataFrame(data_list)


# Récupération des données de HBase
hbase_data = get_data_hbase()


def transform_to_elastic_format(data):
    """
    Transforme les données du DataFrame en un format compatible JSON pour Elasticsearch.
    
    Arguments :
        data (pd.DataFrame) : Les données de HBase sous forme de DataFrame.
        
    Retourne :
        list : Liste de dictionnaires au format JSON pour Elasticsearch.
    """
    actions = []
    for index, row in data.iterrows():
        # Convertir les valeurs boolean en format Elasticsearch pour les champs barchive, bstock et indispobj
        row_dict = row.to_dict()
        row_dict['barchive'] = row_dict['barchive'].lower() == 'true'
        row_dict['bstock'] = row_dict['bstock'].lower() == 'true'
        row_dict['indispobj'] = row_dict['indispobj'].lower() == 'true'

        action = {
            "_index": ELASTIC_INDEX_NAME,
            "_source": row_dict
        }
        actions.append(action)
    return actions


# Transformation des données en format compatible pour Elasticsearch
elastic_data = transform_to_elastic_format(hbase_data)


# Fonction pour insérer les données par lots de 500
def insert_data_batch(data, batch_size=500):
    """
    Insère les données par lots dans Elasticsearch.
    
    Arguments :
        data (list) : Liste de données transformées au format JSON pour Elasticsearch.
        batch_size (int) : Taille du lot pour chaque insertion dans Elasticsearch. Par défaut, 500.
    
    Affiche :
        Messages de confirmation pour chaque lot inséré et les erreurs d'indexation (le cas échéant).
    """
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        try:
            # Envoi du lot dans Elasticsearch
            helpers.bulk(es_connect, batch)
            print(f"Lot {i // batch_size + 1} inséré avec succès.")
        except helpers.BulkIndexError as bulk_error:
            print(f"Erreurs d'indexation pour le lot {i // batch_size + 1} :")
            for error in bulk_error.errors:
                print(f"Erreur d'indexation pour le document {error}")


# Envoi des données par lots de 500 vers Elasticsearch
insert_data_batch(elastic_data, batch_size=500)

# Fermeture de la connexion HBase
connection.close()
