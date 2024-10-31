# Projet BigData Groupe 2 



## Collaborateurs
  - Faiza MNASRI
  - Virginie GIACOMETTI
  - AlaeEN NASYRY
  - Alexis GUIZARD 

### Description :
```
Lot0 : Comprendre et de nettoyer les données fournies par le client.

```

```
Lot1 : Création des jobs :
  - Filtrer les données selon les critères suivants : 
      - Entre 2006 et 2010
      - Uniquement les départements 53, 61 et 28

  - Ressortir dans un tableau des 100 meilleures commandes avec
la ville, la somme des quantités des articles et la valeur de « timbrecde » (la notion
de meilleures commandes : la somme des quantités la plus grande ainsi que le plus
grand nombre de « timbrecde » )

  - Exporter le résultat dans un fichier Excel.
```

```
Lot2 : Création des jobs :
  - Filtrer les données selon les critères suivants : 
      - Entre 2011 et 2016
      - Uniquement les départements 22, 49 et 53

  - Ressortir de façon aléatoire de 5% des 100 meilleures
commandes avec la ville, la somme des quantités des articles sans « timbrecli » (le
timbrecli non renseigné ou à 0) avec la moyenne des quantités de chaque
commande
Avoir un PDF avec un graphe (PIE) (par Ville)

  - Exporter le résultat dans un fichier Excel.
```

```
Lot3 
1. Mettre en place une base NoSQL HBASE pour stocker le contenu du fichier CSV
2. Interroger la base de données NoSQL HBASE avec des scripts python.
  - La meilleure commande de Nantes de l’année 2020.
  - Le nombre total de commandes effectuées entre 2010 et 2015, réparties par année
  - Le nom, le prénom, le nombre de commande et la somme des quantités d’objets du
client qui a eu le plus de frais de timbrecde

3. Créer un programme python (avec Panda) pour créer des graphes en pdf et des tableaux
Excel et csv de votre importation dans HBase :
  - Question 1 partie 1 du lot 3 en csv
  - Question 2 partie 1 du lot 3 en barplot matplotib exporté en pdf
  - Question 3 partie 1 du lot 3 en excel
```

```
Lot4
1. Mettre en œuvre un moteur de recherche avec ELK pour interroger HBase.
2. Pour répondre au Lot 1 et Lot 2 au niveau des résultats avec les graphes
3. Mise en place d’un Dashboard interactif
```


#### Cloner le dépôt :

```bash
git clone https://github.com/lana-12/projetbigdata_gr2.git
```

#### Créer et activer un environnement virtuel :

```python

python -m venv .venv

```

Activation :

Sur Windows :

```bash

.\.venv\Scripts\activate

```

Sur macOS/Linux :
```bash

source .venv/bin/activate

```

#### Désactivation :
```bash

desactivate

```

#### Installer les dépendances :

Activer l environnement
```bash
pip install -r ./requirements.txt

```
#### Exécuter le lot0

Nettoyer le fichier data
```bash
cd lot0
python cleaned_data.py
```


#### Mettre en place l'espace de travail dans la VM + Hadoop

1. Créer un dossier /projetbigdata qui contient 
    - cleaned_data.csv
    - mapperlot1.py
    - reducerlot1.py
    - mapperlot2.py
    - reducerlot2.py
    - script_hbase.py
    - script_query1.py
    - script_query2.py
    - script_query3.py


2. Lancer la vm 
```bash
./start_docker_digi.sh
./lance_srv_slaves.sh
```

3. Téléverser ce dossier dans le dossier /root de la vm avec filezila

4. Déplacer le dossier dans Hadoop
```bash
docker cp projetbigdata hadoop-master:/root/
```

5. Lancer Hadoop
```bash
./bash_hadoop_master.sh
./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift
```

6. Mettre le fichier csv dans HDFS
```bash
hdfs dfs -mkdir -p input
cd projetbigdata
hdfs dfs -put cleaned_data.csv input
```


#### Exécuter les lots

Lot1 => voir /lot1/lot1.md
Lot2 => voir /lot2/lot2.md
Lot3 => voir /lot3/lot3.md
Lot4 => voir /lot4/lot4.md


#### Initialisation Elasticsearch

Plusieurs manières 

1. Cloner un repo Git 
```bash
git clone https://github.com/deviantony/docker-elk.git
docker compose build
docker compose up
```

2. Avec curl 
Avoir Docker démarré
```bash
curl -fsSL https://elastic.co/start-local | sh

```

3. Télécharger Elasticsearch et kibana
Ouvrir un terminal en tant que Administrateur
```bash
./bin/elasticsearch
./bin/kibana

bin/elasticsearch-reset-password -u elastic

```


### Accès à Elasticsearch

http://localhost:5601/
http://127.0.0.1:9200/



### Structure du projet  A REFAIRE

```

pythonprojetbigdata_gr2/
│
├── .venv/                  # Environnement virtuel
│
├── data/                   # Données en csv
│   ├── dataw_fro03.csv     # Fichier initial
│   ├── cleaned_data.csv    # Fichier nettoyé
│      
├── lot0/                   
│   ├── cleaned_data.csv.py # Code pour nettoyer le fichier de données
│      
├── lot1/                    
│   ├── mapperlot1.py       
│   ├── reducerlot1.py      
│   ├── lot1.md/            # Commande è exécuter
|
├── lot2/                    
│   ├── mapperlot2.py       
│   ├── reducerlot2.py      
│   ├── lot2.md/            # Commande è exécuter
│      
|
├── lot3/                    
│   ├── script_hbase.py     # Création de la table       
│   ├── script_query1.py      
│   ├── script_query2.py            
│   ├── script_query3.py            
│   ├── lot3.md             # Commande è exécuter    
|        
├── lot4/                    
│   ├── script_hbase.py     # Connexion à Elasticsearch      
│   ├── lot4.md             # Commande è exécuter            
│      
│
├── .gitignore              # Fichiers et dossiers à ignorer par Git
│
├── README.md               # Documentation du projet
│
├── requirements.txt        # Dépendances du projet
```




