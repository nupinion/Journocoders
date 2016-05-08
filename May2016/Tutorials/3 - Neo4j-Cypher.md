## Introduction

Neo4j is a graph database -- the filesystem in which the data is kept, includes graph information. This means that in the files there are nodes and relationships/edges. So, we could denote information with something like: `(sender)-[sends]->(email)<-[receives]-(recipient)`. 

This facilitates querying the filesystem with graph questions like: "Which people email each other?" and "Who sends emails between their own accounts?".

Neo4j is the name of the database. The language used to query it is called Cypher. 

To access Neo4j, we will interact with its web interface. The interface allows us to both visualise the graph, and to query it with cypher.

In your browser, go to <a href="xxxx:7474">xxxx:7474</a>. You're ready to start exploring!

### Simple Queries

Let's take a quick look at the graph:

```
match (n)-[r]->(m)-[u]->(p) return n,r,m,u,p limit 20;
```

How many nodes are in our graph?

```
match (n) return count(n);
```

What types of nodes are they?

```
match (n) return distinct labels(n), count(n);
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

```
match (ea1:EmailAddress)-[s:sent]->(e:Email) return ea1 limit 10;
```

Also find email addresses that receive emails:

```
match (ea1:EmailAddress)-[s:sent]->(e:Email)<-[r:received]-(ea2:EmailAddress) return ea1,ea2 limit 10;
```

Find the person that these email addresses belong to:

```
match (p1:Person)-[a1:has_address]->(ea1:EmailAddress)-[s:sent]->(e:Email)<-[r:received]-(ea2:EmailAddress)<-[a2:has_address]-(p2:Person) return p1,p2 limit 10;
```

Now, limit the query so that `p1 = p2 = p`, i.e. a person emails themself:

```
match (p:Person)-[a1:has_address]->(ea1:EmailAddress)-[s:sent]->(e:Email)<-[r:received]-(ea2:EmailAddress)<-[a2:has_address]-(p) return p limit 10;
```

Simplified:

```
match (p:Person)-[]->()-[s:sent]->(e:Email)<-[r:received]-()<-[]-(p) return p limit 10;
```

Congratulations! You've cracked it!