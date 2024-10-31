# Projet BigData Groupe 2 



## Collaborateurs
  - Faiza MNASRI
  - Virginie GIACOMETTI
  - AlaeEN NASYRY
  - Alexis GUIZARD 

### Description :


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

2. Lancer la vm 
```bash
./start_docker_digi.sh
./lance_srv_slaves.sh
```

3. Téléverser ce dossier dans le dossier /root de la vm

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
Voir Les dossiers correspondants


#### Initialisation Elasticsearch

Plusieurs manières 

1. Cloner un repo 
```bash
git clone https://github.com/deviantony/docker-elk.git
docker compose build
docker compose up
```

2. Avec curl 
```bash


```

3. Télécharger Elasticsearch et kibana
```bash


```



### Accès à Elasticsearch

http://localhost:5601/
http://127.0.0.1:9200/



### Structure du projet  A REFAIRE

```

pythonApiGestionColisGr2/
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
│      
│
├── .gitignore              # Fichiers et dossiers à ignorer par Git
│
├── README.md               # Documentation du projet
│
├── requirements.txt        # Dépendances du projet
```




