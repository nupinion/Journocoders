# Neo4J Tutorial

Neo4j is a graph database: the filesystem in which the data is kept, includes graph information. This means that in the files there are nodes and relationships/edges. So, we could denote information with something like: `(sender)-[sends]->(email)<-[receives]-(recipient)`. 

This facilitates querying the filesystem with graph questions like: "Which people email each other?" and "Who sends emails between their own accounts?".

Neo4j is the name of the database. The language used to query it is called Cypher. 

To access Neo4j, we will interact with its web interface. The interface allows us to both visualise the graph, and to query it with cypher.

In your browser, go to <a href="http://journocoders.nupinion.com:7474/browser/">http://journocoders.nupinion.com:7474/browser/</a>. You're ready to start exploring!

### Simple Queries

Let's take a quick look at the graph:

```bash
MATCH (n)-[r]->(m)-[u]->(p) RETURN n,r,m,u,p LIMIT 20;
```

How many nodes are in our graph?

```bash
MATCH (n) RETURN COUNT(n);
```

What types of nodes are they?

```bash
MATCH (n) RETURN DISTINCT LABELS(n), COUNT(n);
```

```bash
MATCH ()-[r]->() RETURN DISTINCT TYPE(r), COUNT(r);
```

So, there are people, email addresses and emails in our graph. 

Let's try and answer the question: "Which Enron employee emails themself the most?". We'll break the question into the following steps:
<ol>
  <li>Find email addresses that send emails</li>
  <li>Find email addresses that receive emails</li>
  <li>Identify the person that the above email addresses belong to</li>
  <li>Limit the query so that this person is always the same</li>
  <li>Count the number of emails and sort</li>
</ol>

OK, here we go:

Find email addresses that send emails:

```bash
MATCH (ea:EmailAddress)-[s:Sent]->(e:Email) RETURN ea, s, e LIMIT 20;
```

Also find email addresses that receive emails:

```bash
MATCH (ea1:EmailAddress)-[s:Sent]->(e:Email)<-[r:Received]-(ea2:EmailAddress) RETURN ea1, s, r, ea2 LIMIT 20;
```

Find the person that these email addresses belong to:

```bash
MATCH (p1:Person)-[a1:has_address]->(ea1:EmailAddress)-[s:Sent]->(e:Email)<-[r:Received]-(ea2:EmailAddress)<-[a2:has_address]-(p2:Person) RETURN p1,a1,ea1,s,e,r,ea2,a2,p2 LIMIT 20;
```

Since we are dealing with fraud it makes sense to look at suspicious behaviour. So how about we look at people who actually email themselves (perhaps on a different email address). To do this, limit the query so that `p1 = p2 = p`, i.e. a person emails themself:

```bash
MATCH (p:Person)-[a1:has_address]->(ea1:EmailAddress)-[s:Sent]->(e:Email)<-[r:Received]-(ea2:EmailAddress)<-[a2:has_address]-(p) RETURN p,a1,ea1,s,e,r,ea2,a2 LIMIT 20;
```

Simplified:

```bash
MATCH (p:Person)-[]->()-[s:Sent]->(e:Email)<-[r:Received]-()<-[]-(p) RETURN p LIMIT 20;
```

Congratulations! You've cracked it!


Which pair of individuals email each other the most? Break down the following query.... :)

```bash
MATCH (ea1:EmailAddress)-[s1:Sent]->(e1:Email)<-[r1:Received]-(ea2:EmailAddress)-[s2:Sent]->(e2:Email)<-[r2:Received]-(ea1) WITH ea1.address + " - " + ea2.address AS concat_string RETURN DISTINCT concat_string, COUNT(concat_string) AS ct order BY ct DESC LIMIT 30;
```

