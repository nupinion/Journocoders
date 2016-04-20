
## Setting up Neo4j

* Download from: http://neo4j.com/download/other-releases/
* Select individual version for linux/osx
* Transfer to server and follow installation instructions

Update java:

~~~
$ sudo add-apt-repository ppa:webupd8team/java
$ sudo apt-get update
$ sudo apt-get install oracle-java8-installer
$ java -version
~~~

From neo4j dir:

~~~
$ cd bin/
$ ./neo4j start
# Enter shell for cypher
$ ./neo4j-shell
~~~