from py2neo import Graph

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "your_password"))

# Define and run each query

# Task 1(a)
query_1a = """
MATCH (d:Person)-[:DIRECTED]->(:Movie {title: "Inception"})<-[:ACTED_IN]-(a:Person)
RETURN DISTINCT a.name AS ActorName
"""
result_1a = graph.run(query_1a).data()
print("Task 1(a) - Actors who worked with the director of 'Inception':")
for record in result_1a:
    print(record['ActorName'])
print("\n")

# Task 1(b)
query_1b = """
MATCH (d:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(a:Person)
WHERE (d)-[:DIRECTED]->(:Movie {title: "Inception"})
RETURN m.title AS title, collect(a.name) AS List_of_actors
"""
result_1b = graph.run(query_1b).data()
print("Task 1(b) - Movies directed by 'Inception' director and their actors:")
for record in result_1b:
    print(f"Title: {record['title']}")
    print("List of actors:", record['List_of_actors'])
print("\n")

# Task 1(c)
query_1c = """
MATCH (d:Person)-[:DIRECTED]->(m:Movie)
WHERE d.name =~ '^[M-Y].*'
RETURN d.name AS Directors_Name, COUNT(m) AS Number_of_movies
"""
result_1c = graph.run(query_1c).data()
print("Task 1(c) - Directors with first name between M and Y and their movie counts:")
for record in result_1c:
    print(f"Director: {record['Directors_Name']}, Number of movies: {record['Number_of_movies']}")
print("\n")

# Task 1(d)
query_1d = """
MATCH (m:Movie)
WITH m, m.rating AS rate, COUNT { (m)<-[:RATED]-() } AS numRatings
RETURN m.title AS title, min(rate) AS minRating, avg(rate) AS avgRating, max(rate) AS maxRating, numRatings
ORDER BY avgRating DESC
LIMIT 5
"""
result_1d = graph.run(query_1d).data()
print("Task 1(d) - Top 5 recommended movies:")
for record in result_1d:
    print(f"Title: {record['title']}, Min Rating: {record['minRating']}, Avg Rating: {record['avgRating']}, Max Rating: {record['maxRating']}, Number of Ratings: {record['numRatings']}")
print("\n")

# Task 1(e)
query_1e = """
MATCH (j:Person {name: "James"}), (t:Person {name: "Thomas"})
CREATE (j)-[:FOLLOWS {KNOWS: "Yes"}]->(t)
"""
graph.run(query_1e)
print("Task 1(e) - Created FOLLOWS relationship between 'James' and 'Thomas'.")
print("\n")

# Task 1(f)
query_1f_create_user = """
MERGE (u:Person {name: "Yousef"})
"""
query_1f_rate_movies = """
MATCH (u:Person {name: "Yousef"}), (m:Movie {title: "Inception"})
MERGE (u)-[:RATED {rating: 5}]->(m)
"""
query_1f_follow = """
MATCH (t:Person {name: "Thomas"}), (u:Person {name: "Yousef"})
MERGE (t)-[:FOLLOWS]->(u)
"""
graph.run(query_1f_create_user)
graph.run(query_1f_rate_movies)  # Repeat this for each movie you want to rate
graph.run(query_1f_follow)
print("Task 1(f) - Created user 'Yousef', rated movies, and created FOLLOWS relationship with 'Thomas'.")
print("\n")

# Verify Yousef's ratings
query_verify_yousef_ratings = """
MATCH (u:Person {name: "Yousef"})-[r:RATED]->(m:Movie)
RETURN u.name AS User, m.title AS Movie, r.rating AS Rating
"""
result_verify_yousef_ratings = graph.run(query_verify_yousef_ratings).data()
print("Yousef's Ratings:")
for record in result_verify_yousef_ratings:
    print(f"User: {record['User']}, Movie: {record['Movie']}, Rating: {record['Rating']}")
print("\n")

# Verify Thomas follows Yousef
query_verify_thomas_follows_yousef = """
MATCH (t:Person {name: "Thomas"})-[:FOLLOWS]->(u:Person {name: "Yousef"})
RETURN t.name AS Follower, u.name AS Followed
"""
result_verify_thomas_follows_yousef = graph.run(query_verify_thomas_follows_yousef).data()
print("Thomas Follows Yousef:")
for record in result_verify_thomas_follows_yousef:
    print(f"Follower: {record['Follower']}, Followed: {record['Followed']}")
print("\n")

# Task 1(g)
query_1g = """
MATCH (t:Person {name: "Thomas"})-[:FOLLOWS]->(friend:Person)-[r:RATED]->(m:Movie)
RETURN m.title AS MOVIES, friend.name AS Followed_user, r.rating AS rating
"""
result_1g = graph.run(query_1g).data()
print("Task 1(g) - Movies rated by friends of 'Thomas':")
for record in result_1g:
    if record['Followed_user'] == "James" or record['Followed_user'] == "Yousef":
        print(f"Movie: {record['MOVIES']}, Followed user: {record['Followed_user']}, Rating: {record['rating']}")
print("\n")
