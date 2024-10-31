import happybase
import pandas as pd
"""
Script de connexion à HBase et insertion de données d'un fichier CSV dans une table HBase.

Ce script se connecte à une instance HBase, crée une table pour stocker les données de fromagerie, puis insère
les données ligne par ligne depuis un fichier CSV spécifié. La table est recréée si elle existe déjà.

Configuration:
- `host` (str): Adresse IP du serveur HBase.
- `port` (int): Port du serveur HBase.
- `input_file` (str): Chemin du fichier CSV d'entrée à charger.

Fonctionnalités:
- Se connecte à HBase avec Happybase.
- Vérifie si la table 'fromagerie' existe et la recrée si elle est présente.
- Charge le fichier CSV en mémoire avec Pandas et encode chaque ligne en UTF-8.
- Pour chaque ligne du DataFrame, insère les données dans HBase, avec gestion des erreurs de décodage UTF-8.

Détails des colonnes:
- Les colonnes de données sont préfixées par la famille de colonnes `data_fro:` et encodées en UTF-8.
- En cas d'erreur d'encodage, les valeurs sont remplacées par `ENCODING_ERROR`.

"""

# Configuration connexion
host = '127.0.0.1'
port = 9090
input_file = 'dataw_fro03_final.csv'

# Connexion HBase 
try:
    connection = happybase.Connection(host, port)
    connection.open()
    print("Connexion HBase reussie!")

    df = pd.read_csv(input_file, encoding='utf-8')
    print("Initial number of rows:", len(df))

    # Verif if exist table
    if b'fromagerie' in connection.tables():
        print("La table existe. Suppression en cours...")
        connection.delete_table('fromagerie', disable=True)

    # Create table with col family 
    connection.create_table(
        'fromagerie',
        {'data_fro': dict()}
    )
    table = connection.table('fromagerie')
    print("La table est creer: ", table)

    # Insert with error handling
    for index, row in df.iterrows():
        key = str(index)

        data = {}
        for col, value in row.items():
            try:
                encoded_value = str(value).encode('utf-8', errors='replace')
            except UnicodeEncodeError:
                encoded_value = b'ENCODING_ERROR'
            data[b'data_fro:' + col.encode('utf-8')] = encoded_value

        try:
            table.put(key.encode('utf-8'), data)
        except Exception as e:
            print("Error inserting row", {index}, ":", {e})

    print("Donnees inserees dans HBase avec succes.")

    # Close connection
    connection.close()

except Exception as e:
    print("Erreur de connexion HBase :", e)