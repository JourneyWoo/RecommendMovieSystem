# Movie Recommender System Based on Neo4j and AWS

## Quick Begin

/helperscript/scriptNeo4j_user.py: get the recommended movie list (based on the first algorithm)

    python scriptNeo4j_moive.py [userID] [theNumberOfMovies]

/helperscript/scriptNeo4j_moive.py: get the recommended movie list (based on the second algorithm)

    python scriptNeo4j_moive.py [userID]
    

/toolscript/auto_backup.sh: do the backup of Neo4j DB periodically

/toolscript/stress_test.sh: do the stress test of this Database

/CypherQueryLanguage.txt: the CQL to handle data in Neo4j


## Basic Settings

**Data**: [MovieLen](https://grouplens.org/datasets/movielens/)

**Database**: [Neo4j](https://neo4j.com/)

**Cloud Server**: AWS

## Recommender Algorithms

- Content-based

Main Idea: Counting the paths between the liked movies of one specific user and other movies as similarity. Recommend top 10 movies.
Pros: This method intensively focus on the preference of this user. It is possible to recommend niche movies. This method suits Neo4j very well.
Cons: It is hard for this method to deal with cold starts(new users/movies).

![EuKXDA.md.png](https://s2.ax1x.com/2019/04/27/EuKXDA.md.png)

- User-User Collaborative Filter

Main Idea: Similar users⇒ Popular movies in this neighbourhood ⇒ Predict the ratings.

![EuKjHI.th.png](https://s2.ax1x.com/2019/04/27/EuKjHI.th.png)

Pros: This method tends to recommend safe choices(popular movies).
Cons: Boring recommendation and it requires more mathematic computation which may not be Neo4j’s strong suit. Python is used here.

![EuKzUP.md.png](https://s2.ax1x.com/2019/04/27/EuKzUP.md.png)

## AWS Settings

AWS IPV4 Address: 3.85.121.66
HTTP x.y.z.0/24 7474
HTTPS  x.y.z.0/24 7473
BOLT x.y.z.0/24 7687

## Neo4j Remote Database Settings

Connect URL: neo4j@bolt://3.85.121.66:7687
Username: xyz
Password: xyz

## Neo4j Structure

![EuMPgg.md.png](https://s2.ax1x.com/2019/04/27/EuMPgg.md.png)
