# Projet BigData Groupe 2 



## Collaborateurs
  - Faiza MNASRI
  - Virginie GIACOMETTI
  - AlaeEN NASYRY
  - Alexis GUIZARD 

### Description :


### Initialisation :

#### 1. Cloner le dépôt :

```bash
git clone https://github.com/aennasyry/pythonApiGestionColisGr2.git
```

#### 2. Créer et activer un environnement virtuel :

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

#### 3. Désactivation :
```bash

desactivate

```

#### 4.Installer les dépendances :


Activer l environnement
```bash
pip install -r ./requirements.txt

```


### Initialisation Elasticsearch

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
│
├── config.py               # Configuration de l'application ;Contient les paramètres de configuration de la base des données
│  
│
├── src/                    # Code source de l'application
│   ├── main.py             # Point d'entrée de l'application
│   ├── models/             # Modèles de Base de données:Contient les modèles SQLAlchemy
│   │   
│   ├── routers/            # Routes de l'application: Contient les routes FastAPI
│   │   
│   ├── schemas/            # Schémas de données (Pydantic): Contient les schémas de validation
│   │   
│   └── services/           # Services et logique métier
│      
│
├── .gitignore              # Fichiers et dossiers à ignorer par Git
│
├── README.md               # Documentation du projet
│
├── requirements.txt        # Dépendances du projet
```




