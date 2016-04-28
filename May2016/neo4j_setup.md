
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

##### Authorization

To call neo4j from python, we run into authorization issues. For exampe, look here:
https://stackoverflow.com/questions/32840922/authentication-on-neo4j-with-python

For simplicity for this course, we will turn off authorization:

(from neo dir)
~~~
$ pico conf/neo4j.conf
~~~

uncomment the line `#dbms.security.auth_enabled=false`.


Upon starting neo4j, sometimes it is required to wait a moment before being able to call the service from python. Attempt using cypher from the shell to ensure it running properly. 