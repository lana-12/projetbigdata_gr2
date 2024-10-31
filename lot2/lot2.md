# Exécuter le lot2

Assurez-vous d'avoir : voir => Mettre en place l'espace de travail dans la VM + Hadoop dans le fichier README.md

1. Lancer les services Hadoop + HBase
2. Créer le répertoire input et transférer le fichier de cleaned_data.csv


## Supprimer le répertoire de sortie existant dans HDFS :
hdfs dfs -rm -r outputjob02

## Exécuter le job Hadoop Streaming
hadoop jar hadoop-streaming-2.7.2.jar -file mapperlot2.py -mapper "python3 mapperlot2.py" -file reducerlot2.py -reducer "python3 reducerlot2.py" -input input -output outputjob02




