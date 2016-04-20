

## Elasticsearch


~~~
curl -XDELETE http://127.0.0.1:9200/enron

curl -XPOST http://127.0.0.1:9200/enron -d '{
    "mappings" : {
        "emails": {
            "properties": {
                "body": {
                    "type": "multi_field",
                    "fields": {
                        "body": { 
                            "type":         "string",
                            "analyzer":     "standard"
                        },
                        "english": { 
                            "type":         "string",
                            "analyzer":     "english"
                        },
                        "stemming": { 
                            "type" : "string",
		                    "analyzer" : "snowball"
                        }
                    }
                },
                "subject": {
                    "type": "multi_field",
                    "fields": {
                        "Description": { 
                            "type":         "string",
                            "analyzer":     "standard"
                        },
                        "english": { 
                            "type":         "string",
                            "analyzer":     "english"
                        },
                        "stemming": { 
                            "type" : "string",
                            "analyzer" : "snowball"
                        }
                    }
                },
                "date": {
                  "type":   "date",
                  "format": "yyyy-MM-dd HH:mm:ss"
                }
            }
        }
    }
}'
~~~
