
# Neo4J Installation


### Install/Update Java

Update java:

```bash
$ sudo add-apt-repository ppa:webupd8team/java
$ sudo apt-get update
$ sudo apt-get install oracle-java8-installer
$ java -version
```

Download Neo4J

```bash
wget http://neo4j.com/artifact.php?name=neo4j-community-3.0.1-unix.tar.gz

tar -xf artifact.php\?name\=neo4j-community-3.0.1-unix.tar.gz

$NEO4J_HOME/bin/neo4j console
```

From neo4j dir:

~~~
$ cd bin/
$ ./neo4j start
# Enter shell for cypher
$ ./neo4j-shell
~~~

To open up remote access to the webserver we need to uncomment the following line in `<NEODIR>/conf/neo4j.conf`

```bash
dbms.connector.http.address=0.0.0.0:7474
```

Now we can access it on: http://<IP-ADDRESS>:7474/


### Authorization Issues in Python

To call neo4j from python, we run into authorization issues. For exampe, look here:
https://stackoverflow.com/questions/32840922/authentication-on-neo4j-with-python

For simplicity for this course, we will turn off authorization:

(from neo dir)
~~~
$ pico conf/neo4j.conf
~~~

uncomment the line `#dbms.security.auth_enabled=false`.

Upon starting neo4j, sometimes it is required to wait a moment before being able to call the service from python. Attempt using cypher from the shell to ensure it running properly. 