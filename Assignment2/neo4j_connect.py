from neo4j import GraphDatabase

# Neo4j connection URI and credentials
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

# Create a driver instance
driver = GraphDatabase.driver(uri, auth=(user, password))

def test_connection():
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) AS node_count")
        record = result.single()
        print(f"Node count: {record['node_count']}")

# Test the connection
test_connection()

# Close the driver
driver.close()
