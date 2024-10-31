# Exécuter le lot2

## Copier le fichier JAR Hadoop Streaming dans le répertoire courant 
cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .

## Démarre services Hadoop
./start-hadoop.sh

## Démarre le service HBase
start-hbase.sh
hbase-daemon.sh start thrift

## Créer un répertoire dans HDFS pour les données d'entrée
hdfs dfs -mkdir -p input

## Supprimer le fichier cleaned_data.csv dans HDFS
hdfs dfs -rm input/cleaned_data.csv

## Télécharger le fichier cleaned_data.csv vers HDFS
hdfs dfs -put cleaned_data.csv input

## Supprimer le répertoire de sortie existant dans HDFS :
hdfs dfs -rm -r outputjob02

## Exécuter le job Hadoop Streaming
hadoop jar hadoop-streaming-2.7.2.jar -file mapperlot2.py -mapper "python3 mapperlot2.py" -file reducerlot2.py -reducer "python3 reducerlot2.py" -input input/csv -output outputjob02




