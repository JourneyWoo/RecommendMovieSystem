from py2neo import Graph,Node,Relationship
import csv
import sys

user = sys.argv[1]
showCount = sys.argv[2]

neo4jAddress = 'bolt://3.85.121.66:7687'
userName = 'neo4j'
passWord = 'I won\'t tell you :-)'
csv_path = "/Users/wuzhenglin/movies.csv"

print "Connect to AWS Neo4j " + neo4jAddress + " ...\n"

graph = Graph(neo4jAddress,username=userName,password=passWord)
cypher_phrase = "MATCH (u1:User{userId:'" + user + "'})-[r:Rating]->(:Movie) WITH  u1, max(r.rating) as rmax MATCH (u1)-[r:Rating]->(m1:Movie)<-[]-()-[]->(m2:Movie) WHERE r.rating = rmax AND m2 <> m1 WITH m2, count(*) as count ORDER BY count DESC Return m2.movieId, count"
matchResult = graph.run(cypher_phrase)
matchResult = list(matchResult)

recommendId_list = []
recommendTitle_list = []
for i in range(len(matchResult)):
    recommendId_list.append(matchResult[i][0])

csv_file = csv.reader(open(csv_path, "r"))
moiveDic = {}
for item in csv_file:
    moiveDic[item[0]] = item[1]

for id in recommendId_list:
    recommendTitle_list.append(moiveDic[id])

if int(showCount) > len(recommendId_list):
    print "Sorry, the length of recommonded moive-list for you is", len(recommendId_list)
else:
    for i in range(int(showCount)):
        print i + 1, recommendTitle_list[i]






