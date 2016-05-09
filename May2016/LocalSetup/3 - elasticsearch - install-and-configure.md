# ElasticSearch Installation

First some notes on installing ElasticSearch (2.1.1), Kibana (4.3.1), and Sense.

Great read-through: https://www.elastic.co/guide/en/elasticsearch/guide/current/getting-started.html


### Install Java

Install Java

~~~bash
$ sudo apt-add-repository ppa:webupd8team/java
$ sudo apt-get update
$ sudo apt-get install oracle-java7-installer

$ java -version
~~~



### Installing ElasticSearch (2.1.1)

First download and unpack ElasticSearch:

~~~bash
$ wget https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-2.1.1.tar.gz

$ tar -xvzf elasticsearch-2.1.1.tar.gz

$ rm elasticsearch-2.1.1.tar.gz

$ mv elasticsearch-2.1.1/ elastic-elasticsearch-2.1.1/

$ cd elastic-elasticsearch-2.1.1
~~~

~~~bash
$ cd ~/elastic-elasticsearch-2.1.1/

$ sudo bin/plugin install license
-> Installing license...
Plugins directory [/home/vagrant/elasticsearch-2.1.1/plugins] does not exist. Creating...
Trying https://download.elastic.co/elasticsearch/release/org/elasticsearch/plugin/license/2.1.1/license-2.1.1.zip ...
Downloading .......DONE
Verifying https://download.elastic.co/elasticsearch/release/org/elasticsearch/plugin/license/2.1.1/license-2.1.1.zip checksums if available ...
Downloading .DONE
Installed license into /home/vagrant/elastic-elasticsearch-2.1.1/plugins/license
~~~

Install Kibana, the visualisation toolkit and something we will need to run the UI for elasticsearch (i.e., Sense).

~~~bash
$ wget https://download.elastic.co/kibana/kibana/kibana-4.3.1-linux-x64.tar.gz

$ tar -xvzf kibana-4.3.1-linux-x64.tar.gz

$ rm kibana-4.3.1-linux-x64.tar.gz

$ mv kibana-4.3.1-linux-x64/ elastic-kibana-4.3.1/

$ cd elastic-kibana-4.3.1/
~~~

~~~bash
$ ./bin/kibana plugin --install elastic/sense
Installing sense
Attempting to extract from https://download.elastic.co/elastic/sense/sense-latest.tar.gz
Downloading 318236 bytes....................
Extraction complete
Optimizing and caching browser bundles...
~~~

To summarise. We have installed **ElasticSearch**, **Kibana** and the **Sense** UI plugin.

-
### Starting the Service(s)

To start ElasticSearch we can run:

~~~
# Use the flag -d for background deamon.
$ ./elastic-elasticsearch-2.1.1/bin/elasticsearch -d 
~~~

To see what the process id is:

~~~bash
$ ps aux | grep elastic
vagrant   2134 60.5  8.6 1886424 177556 pts/0  Sl   15:57   0:04 /usr/bin/java -Xms256m -Xmx1g -Djava.awt.headless=true -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly -XX:+HeapDumpOnOutOfMemoryError -XX:+DisableExplicitGC -Dfile.encoding=UTF-8 -Djna.nosys=true -Des.path.home=/home/vagrant/elasticsearch-2.1.1 -cp /home/vagrant/elasticsearch-2.1.1/lib/elasticsearch-2.1.1.jar:/home/vagrant/elasticsearch-2.1.1/lib/* org.elasticsearch.bootstrap.Elasticsearch start -d
vagrant   2187  0.0  0.0  10432   668 pts/0    S+   15:57   0:00 grep elastic
~~~

To start Kibana we can run:

~~~bash
# To start Kibana, supress output and put it in a background process
$ nohup ./elastic-kibana-4.3.1/bin/kibana &
~~~

The URL's we can use now are

* Sense on Kibana - http://127.0.0.1:5601/app/sense

