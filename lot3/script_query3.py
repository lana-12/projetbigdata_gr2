from collections import defaultdict
import os
import happybase
import pandas as pd

"""
Script de recherche du client ayant les frais de timbre les plus élevés dans la table HBase 'fromagerie' et export des résultats en Excel.

Ce script se connecte à HBase, lit les données de la table 'fromagerie' pour identifier le client ayant les frais de timbre les plus élevés.
Les informations sur ce client sont ensuite exportées dans un fichier Excel pour une analyse ultérieure.

Fonctionnalités:
- Connexion à HBase et accès à la table 'fromagerie'.
- Calcul des frais de timbre cumulés pour chaque client, ainsi que du nombre de commandes et de la quantité totale de produits commandés.
- Identification du client avec les frais de timbre les plus élevés.
- Export des informations du client dans un fichier Excel dans le répertoire spécifié.

Configuration:
- Hôte: `127.0.0.1`
- Port: `9090`
- Répertoire de sortie: `/datavolume1/results_lot3`
- Nom du fichier de sortie: `client_max_timbre.xlsx`

Structure des données dans HBase:
- `data_fro:codcli`: ID client
- `data_fro:qte`: Quantité de produits commandés
- `data_fro:timbrecli`: Frais de timbre associés au client
- `data_fro:nomcli`: Nom du client
- `data_fro:prenomcli`: Prénom du client

"""

# Connect to HBase
connection = happybase.Connection('127.0.0.1', port=9090)
table = connection.table('fromagerie')

# 3. Client with the highest postage fees
def client_with_max_timbre():
    clients_data = defaultdict(lambda: {'count': 0, 'total_qty': 0, 'nom': '', 'prenom': ''})

    for key, data in table.scan():
        # Retrieve necessary information
        client_id = data[b'data_fro:codcli'].decode()
        quantity = int(data[b'data_fro:qte'].decode())
        timbre = float(data[b'data_fro:timbrecli'].decode())
        nom = data[b'data_fro:nomcli'].decode()
        prenom = data[b'data_fro:prenomcli'].decode()

        clients_data[client_id]['count'] += 1
        clients_data[client_id]['total_qty'] += quantity
        clients_data[client_id]['nom'] = nom
        clients_data[client_id]['prenom'] = prenom
        
        # Find the client with the highest postage fees
    max_timbre_client = max(clients_data.items(), key=lambda x: x[1]['total_qty'])
    
    return max_timbre_client[1]  

client_max_timbre = client_with_max_timbre()

print("\nClient with the highest postage fees:")
print(client_max_timbre)

# Output directory
output_dir = '/datavolume1/results_lot3'
os.makedirs(output_dir, exist_ok=True)  

# Export results to an Excel file
def export_to_excel(data, output_directory, filename='client_max_timbre.xlsx'):
    df = pd.DataFrame([data])
    file_path = os.path.join(output_directory, filename)  
    df.to_excel(file_path, index=False)
    print("Results exported to " + file_path)  

# Call the export function
export_to_excel(client_max_timbre, output_dir)
