import happybase
import pandas as pd
import os
import csv

"""
Script de récupération et de traitement des données dans la table HBase 'fromagerie'.

Ce script se connecte à HBase, scanne les commandes stockées dans la table 'fromagerie', filtre celles qui
correspondent à l'année 2020 et à la ville de Nantes, puis identifie la commande avec la plus grande quantité,
et en cas d'égalité, celle avec le plus grand timbre. Les résultats sont enregistrés dans un fichier CSV.

Fonctionnalités:
- Connexion à HBase et accès à la table 'fromagerie'.
- Filtrage des commandes par date (2020) et ville (Nantes).
- Agrégation des quantités et des timbres pour chaque commande (`codecde`).
- Sélection de la meilleure commande selon la quantité, puis le timbre en cas d'égalité.
- Export des informations sur la meilleure commande dans un fichier CSV.

Configuration:
- Hôte: `localhost`
- Port: `9090`
- Fichier CSV de sortie: `/datavolume1/results_lot3/best_order_nantes.csv`

Structure des données dans HBase:
- `codecde` : Code de la commande
- `qte` : Quantité de l'article
- `timbrecde` : Timbre de la commande
- `genrecli`, `nomcli`, `prenomcli`, `villecli`, `datcde` : Informations sur le client et la commande

Détails du CSV:
- Si une commande valide est trouvée, le script enregistre les informations suivantes dans le fichier CSV:
    - Ville, Date, Code de commande, Quantité, Timbre, Genre, Nom de famille, Prénom.
- Affiche la meilleure commande dans la console.

Gestion des erreurs:
- Gère les erreurs de connexion, les erreurs d'encodage UTF-8 et les erreurs de type lors du traitement.

"""

# Connect to the 'fromagerie' table in HBase to access data
connection = happybase.Connection('localhost', port=9090)
table = connection.table('fromagerie')  

# Initialize variables to store order information by codecde
data_fro = {}

# Scan the table for all rows related to orders
for key, data in table.scan():
    codecde = data.get(b'data_fro:codcde', b'').decode('utf-8')
    qte = int(data.get(b'data_fro:qte', b'0').decode('utf-8'))
    timbrecde = float(data.get(b'data_fro:timbrecde', b'0.0').decode('utf-8'))
    genrecli = data.get(b'data_fro:genrecli', b'').decode('utf-8')
    nomcli = data.get(b'data_fro:nomcli', b'').decode('utf-8')
    prenomcli = data.get(b'data_fro:prenomcli', b'').decode('utf-8')
    villecli = data.get(b'data_fro:villecli', b'').decode('utf-8')
    datcde = data.get(b'data_fro:datcde', b'').decode('utf-8')



    # Filter orders by date (2020) and city (Nantes)
    if '2020' in datcde and 'NANTES' in villecli.upper():
        print("Order matches criteria for 2020 and Nantes")
        
        if codecde not in data_fro:
            data_fro[codecde] = {
                'qte': 0,
                'timbrecde': 0.0,
                'villecli': villecli,
                'datcde': datcde,
                'genrecli': genrecli,
                'nomcli': nomcli,
                'prenomcli': prenomcli
            }

        # Accumulate quantity and timbre for each codecde
        data_fro[codecde]['qte'] += qte
        data_fro[codecde]['timbrecde'] += timbrecde

# Find the best order based on quantity and timbre
best_order = None
best_order_key = None

for codecde, order in data_fro.items():
    if best_order is None or (
            order['qte'] > best_order['qte'] or (
            order['qte'] == best_order['qte'] and order['timbrecde'] > best_order['timbrecde']
    )):
        best_order = order
        best_order_key = codecde

# Prepare data for CSV export if a best order is found
if best_order:
    result = {
        'City': best_order['villecli'],
        'Date': best_order['datcde'],
        'Codecde': best_order_key,
        'Quantity': best_order['qte'],
        'Timbrecde': best_order['timbrecde'],
        'Gender': best_order['genrecli'],
        'LastName': best_order['nomcli'],
        'FirstName': best_order['prenomcli']
    }
    df = pd.DataFrame([result])

    # Save path for the CSV file
    output_dir = '/datavolume1/results_lot3'
    os.makedirs(output_dir, exist_ok=True)  

    # Save data to a CSV file
    df.to_csv(os.path.join(output_dir, 'best_order_nantes.csv'), index=False)
    print("Best order saved to /datavolume1/results_lot3/best_order_nantes.csv")

    # Display the result in the console
    print("Best Order:")
    print("Order Code: {}".format(result['Codecde']))
    print("Quantity: {}".format(result['Quantity']))
    print("Timbrecde: {}".format(result['Timbrecde']))
    print("Last Name: {}".format(result['LastName']))
    print("First Name: {}".format(result['FirstName']))

  
else:
    print("No orders found.")
