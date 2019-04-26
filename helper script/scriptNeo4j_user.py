from py2neo import Graph,Node,Relationship
import csv
import sys
from collections import OrderedDict

user = sys.argv[1]

neo4jAddress = 'bolt://3.85.121.66:7687'
userName = 'neo4j'
passWord = 'I won\'t tell you :-)'
csv_path = "/Users/wuzhenglin/movies.csv"

print "Connect to AWS Neo4j " + neo4jAddress + " ...\n"

graph = Graph(neo4jAddress,username=userName,password=passWord)
cypher_phrase1 = "MATCH (u1{userId:'" + user + "'})-[r1:Rating]->(m1:Movie)<-[]-()-[]->(:Movie)<-[r2:Rating]-(u2:User) WITH  u1, max(r1.rating) as rmax1, max(r2.rating) as rmax2 MATCH (u1)-[r1:Rating]->(m1:Movie)<-[]-()-[]->(:Movie)<-[r2:Rating]-(u2:User) WHERE r1.rating = rmax1 AND r2.rating = rmax2 AND u2 <> u1 WITH u1, u2, count(*) as count ORDER BY count DESC Limit 10 RETURN collect(u2.userId) as Neighbours, count"
matchResult1 = graph.run(cypher_phrase1)
matchResult1 = list(matchResult1)
neighbors = []
count1_list = []
w_map = {}
w_sum = 0

for i in range(len(matchResult1)):
    neighbors.append(matchResult1[i][0])
    count1_list.append(matchResult1[i][1])
    w_map[str(neighbors[i][0])] = matchResult1[i][1]
    w_sum += int(matchResult1[i][1])

neighbors_str = ""
for i in range(len(neighbors)):
    neighbor_str = str(neighbors[i][0])
    neighbors_str += "\"" + neighbor_str + "\"" + ","
neighbors_str = "[" + neighbors_str[0:len(neighbors_str) - 1] + "]"

cypher_phrase2 = "WITH " + neighbors_str + " as Neighbours MATCH (u:User) where u.userId IN Neighbours WITH collect(u) as nodes UNWIND nodes as n UNWIND nodes as m WITH * WHERE id(n) < id(m) MATCH path = (n)-[r2:Rating]->(m2:Movie)<-[r3:Rating]-(m) WITH m2, count(m2) as count WHERE count = 10 RETURN collect(m2.movieId) as CommonM"
matchResult2 = graph.run(cypher_phrase2)
matchResult2 = list(matchResult2)
commonMoives = matchResult2[0][0]

commonMoives_str = ""
for i in range(len(commonMoives)):
    moive_str = str(commonMoives[i])
    commonMoives_str += "\"" + moive_str + "\"" + ","
commonMoives_str = "[" + commonMoives_str[0:len(commonMoives_str) - 1] + "]"

cypher_phrase3 = "WITH " + neighbors_str + " as Neighbours," + commonMoives_str + " as CommonM MATCH (u:User) WHERE u.userId IN Neighbours MATCH (p:Movie) WHERE p.movieId IN CommonM WITH collect(u) as nodes, collect(p) as modes UNWIND nodes as n UNWIND modes as m MATCH path = (n)-[r2:Rating]->(m) RETURN n.userId, r2.rating, m.movieId"
matchResult3 = graph.run(cypher_phrase3)
matchResult3 = list(matchResult3)

userid3 = []
rating3 = []
moiveMap = {}

for i in range(len(matchResult3)):
    u = str(matchResult3[i][0])
    r = int(matchResult3[i][1])
    m = str(matchResult3[i][2])

    if m not in moiveMap:
       appMap = {}
       appMap[u] = r
       moiveMap[m] = appMap
    else:
        oldMap = moiveMap[m]
        oldMap[u] = r
        moiveMap[m] = oldMap

cypher_phrase4 = "WITH " + neighbors_str + " as Neighbours MATCH (u:User) WHERE u.userId IN Neighbours RETURN u.AveRating"
matchResult4 = graph.run(cypher_phrase4)
matchResult4 = list(matchResult4)
rv = []
rv2_map = {}
for i in range(len(matchResult4)):
    rv.append(matchResult4[i][0])
    rv2_map[str(neighbors[i][0])] = matchResult4[i][0]

# do the calculation
moive_rate = {}
for each_moive in moiveMap:
    rv_map = moiveMap[each_moive]
    sum = 0
    for each_user in rv_map:
        rvi = rv_map[each_user]
        rv2 = rv2_map[each_user]
        w3 = w_map[each_user]
        upper = (rvi - rv2) * w3
        sum += upper
    
    moive_rate[each_moive] = sum

result_list = []

csv_path = "/Users/wuzhenglin/movies.csv"
csv_file = csv.reader(open(csv_path, "r"))
moiveDic = {}
for item in csv_file:
    moiveDic[item[0]] = item[1]


for m in moive_rate:
    moive_rate[m] = moive_rate[m] / w_sum
    if moive_rate[m] > 0:
        result_list.append(moiveDic[m])


for i in range(len(result_list)):
    print i + 1, result_list[i]


    



    


    
         


         












