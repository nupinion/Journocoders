## Introduction

Elasticsearch is a fantastic document store for searching text. We can carry out flexible text queries -- even fuzzy matches -- across all data points.

To access Elasticsearch, we will interact with <a href="https://www.elastic.co/products/kibana">Kibana</a>. Kibana is an interface for testing queries pre-production.

In your browser, go to <a href="xxxx:5601/app/sense">xxxx:5601/app/sense</a>. Then click on <button style="background:blue; color:white;">Start exploring</button>

### Simple Queries

In the left side of the console, paste `GET _cat/indices`. If you click on that line a play button should appear. Click on the play button to execute. This shows you details of what documents and how many are in the database. 

From a new line, check what the documents look like. Do a general search like this:

```
GET _search
{
  "query": {
    "match_all": {}
  }
}

```

By default, Elasticsearch will only return the first 10 documents. To return some more, do:

```
GET _search
{
  "from" : 20, "size" : 30,
  "query": {
    "match_all": {}
  }
}
```

Let's limit the search. Imagine we want to find employees that within a time period, were thinking of getting a new job, that were sent in the last two months.


Search for "looking for a new job" in the body of the email

```
GET _search
{
  "size":10000,
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
  "size":10000,
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
  "size":10000,
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
  "size":10000,
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


Limit according to date, and return the sender:

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
      }
    
    }
  },
  "size":2000,
  "fields":["sender"]
} 
```


