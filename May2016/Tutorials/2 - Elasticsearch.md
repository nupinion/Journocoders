## Introduction

Elasticsearch is a fantastic document store for searching text. We can carry out flexible text queries -- even fuzzy matches -- across all data points.

To access Elasticsearch, we will interact with <a href="https://www.elastic.co/products/kibana">Kibana</a>. Kibana is an interface for testing queries pre-production.

In your browser, go to <a href="http://54.171.70.156:5601/app/sense">http://54.171.70.156:5601/app/sense</a>. Then click on <button style="background:grey; color:white;">Get to work</button>

### Simple Queries

You might have the following query already pasted on the left:

```
GET _search
{
  "query": {
    "match_all": {}
  }
}

```

If you click on that first line a play button should appear. Click on the play button to execute. 

By default, Elasticsearch will only return the first 10 documents. In a new line, paste `GET _cat/indices`. This shows you details of what documents and how many are in the database. 

To return some more documents from the first query, do:

```
GET _search
{
  "from" : 20, "size" : 30,
  "query": {
    "match_all": {}
  }
}
```

Let's limit the search. Imagine we want to find employees that within a time period (say the last two months), were thinking of getting a new job.

Search for "looking for a new job" in the body of the email

```
GET _search
{
  "size":10,
  "query":{
          "query_string" : {
	          "fields" : ["body"],
	          "query" : "looking for a new job"
        }
  }
}
```

How many results did you get? Do they mention all the keywords? In Elasticsearch, if we don't specify that all keywords should be present, it will return a "hit" if only just one of them is present. Try instead:

```
GET _search
{
  "size":10,
  "query":{
          "query_string" : {
	          "fields" : ["body"],
	          "query" : "looking AND for AND a AND new AND job"
        }
  }
}
```

Now we get significantly less! Perhaps we should also search the subject of the email, and drop a few "stop words". Try:

```
GET _search
{
  "size":10,
  "query":{
          "query_string" : {
	          "fields" : ["body","subject"],
	          "query" : "look AND new AND job"
        }
  }
}
```

The real power of using Elasticsearch comes from its flexibility. One of the most popular uses is Elasticsearch's default ability to stem words. Try out the following query:


```
GET _search
{
  "size":10,
  "query":{
          "query_string" : {
	          "fields" : ["body.stemming","subject.stemming"],
	          "query" : "look* AND new AND job"
        }
  },
  "fields":["body","subject"]
}
```

Do you see what this has done?


Finally, let's write a more complicated query, by adding some filters! Limit according to date, ensure only enron addresses are the sender and return the sender:

```
GET _search
{
  "query": {

    "filtered":{
    
      "filter":{
        "range":{
          "date": {
            "gte":"2001-01-01 00:00:00",
            "lte":"2002-12-31 23:59:59"
          }
        }
      },
    
      "query": {
 
        "query_string" : {
          "fields" : ["body.stemming","subject.stemming"],
          "query" : "look* AND job"
        }
      },
      "query": {
 
        "query_string" : {
          "fields" : ["sender"],
          "query" : "@enron"
        }
      }
    
    }
  },
  "size":20,
  "fields":["sender"]
} 
```

Well done! Feel free to experiment!
