from collections import defaultdict
import os
import happybase
import matplotlib.pyplot as plt

"""
Script de comptage des commandes par année dans la table HBase 'fromagerie' et génération d'un graphique PDF.

Ce script se connecte à HBase, récupère toutes les commandes de la table 'fromagerie' et compte le nombre de commandes
par année entre 2010 et 2015. Les résultats sont ensuite affichés dans la console, et un graphique à barres représentant
le nombre total de commandes par année est généré et enregistré dans un fichier PDF.

Fonctionnalités:
- Connexion à la table 'fromagerie' de HBase.
- Filtrage et comptage des commandes par année entre 2010 et 2015.
- Affichage du nombre de commandes par année dans la console.
- Génération d'un graphique à barres représentant le nombre total de commandes par année.
- Sauvegarde du graphique dans un fichier PDF dans le répertoire spécifié.

Configuration:
- Hôte: `127.0.0.1`
- Port: `9090`
- Fichier PDF de sortie: `/datavolume1/results_lot3/orders_by_year.pdf`

Structure des données dans HBase:
- La colonne `data_fro:datcde` contient les dates des commandes au format `AAAA-MM-JJ`.

"""


# Connect to HBase
connection = happybase.Connection('127.0.0.1', port=9090)
table = connection.table('fromagerie')

def orders_count_by_year():
    # Dictionary to store the number of orders per year
    orders_per_year = {year: 0 for year in range(2010, 2016)}

    for key, data in table.scan():
        date_str = data[b'data_fro:datcde'].decode()
        year = int(date_str.split('-')[0])  

        if 2010 <= year <= 2015:
            orders_per_year[year] += 1

    return orders_per_year

orders_by_year = orders_count_by_year()

# Display results in ascending order
print("\nTotal number of orders between 2010 and 2015:")
for year in sorted(orders_by_year.keys()):
    print("{}: {} orders".format(year, orders_by_year[year]))

# Output directory
output_dir = '/datavolume1/results_lot3'
os.makedirs(output_dir, exist_ok=True)  

# Create a bar plot
years = list(orders_by_year.keys())
counts = list(orders_by_year.values())

plt.figure(figsize=(10, 6))
plt.bar(years, counts, color='blue')
plt.xlabel('Year')
plt.ylabel('Number of Orders')
plt.title('Total Number of Orders by Year (2010-2015)')
plt.xticks(years)  
plt.grid(axis='y')

# Save the plot as a PDF in the specified output directory
pdf_path = os.path.join(output_dir, 'orders_by_year.pdf')  
plt.savefig(pdf_path)  
plt.close() 

print("PDF saved at: " + pdf_path)  
