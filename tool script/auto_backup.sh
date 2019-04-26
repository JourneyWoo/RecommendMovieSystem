time=date '+%y-%m-%d %H:%M:%S'
file=date '+%y-%m-%d'
echo $time
echo $file
echo ‘Begin the backup...’
/neo4jfolder/neo4j-community-3.5.4/bin/neo4j-admin  dump --database=graph.db --to=/neo4jfolder/neo4j-community-3.5.4/backup
echo ‘Finish the backup’