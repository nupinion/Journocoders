from py2neo import Graph, Path
graph = Graph()

MATCH (n)-[r]->() DELETE n,r;
MATCH (n) DELETE n;


MATCH (n:Person) RETURN n;
MATCH (n:Email) RETURN n;

//all nodes need at least one relationship?
MATCH (person:Person)-[r]->(email)
WHERE r is null
RETURN person; 

//all nodes need at least one relationship?
MATCH (email:Email)-[r]->(person)
WHERE r is null
RETURN email; 