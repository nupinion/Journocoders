from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime

es = Elasticsearch()

print es.search(index="enron",doc_type="emails")["hits"]["total"]

search_terms = "holidays"

def es_search(search_terms):
	search_results = es.search(
	    index="enron",
	    doc_type="emails",
	    body={
	      "sort": [
	      	"_score"
	      ],
	      "query": {
	        "bool": {
	          "should": [],
	          "must": [
	              { "query_string" : 
	                {
	                  "fields" : ["subject","body"],
	                  "query" : ' AND '.join(search_terms)
	                }
	              }
	            ],
	        }
	      },
	      "from": 0,
	      "size": 10000,
	      "fields": [ "subject", "body"]
	    }
	)
	print search_results['hits']['total']
	#extract output
	output = []
	for x in range(0,search_results['hits']['total']):
		tmp = dict()
		tmp["score"] = search_results["hits"]["hits"][x]["_score"]
		tmp["body"] = search_results["hits"]["hits"][x]["fields"]["body"][0]
		tmp["subject"] = search_results["hits"]["hits"][x]["fields"]["subject"][0]
		output.append(tmp)
	# return 
	return output;
