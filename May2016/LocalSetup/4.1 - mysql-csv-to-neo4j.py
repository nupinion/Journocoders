
# coding: utf-8

# MySQL Syntax to create the CSV's
# 
# ```bash
# SELECT *
# FROM employeelist
# INTO OUTFILE '/tmp/employeelist.csv' 
# FIELDS ENCLOSED BY '"' 
# TERMINATED BY ',' 
# ESCAPED BY '"' 
# LINES TERMINATED BY '\n';
# ```
# 
# ```bash
# SELECT *
# FROM message
# INTO OUTFILE '/tmp/message.csv' 
# FIELDS ENCLOSED BY '"' 
# TERMINATED BY ',' 
# ESCAPED BY '"' 
# LINES TERMINATED BY '\n';
# ```
# 
# 
# ```bash
# SELECT *
# FROM recipientinfo
# INTO OUTFILE '/tmp/recipientinfo.csv' 
# FIELDS ENCLOSED BY '"' 
# TERMINATED BY ',' 
# ESCAPED BY '"' 
# LINES TERMINATED BY '\n';
# ```

# In[1]:

import json
import os
import time


# In[2]:

from neo4j.v1 import GraphDatabase, basic_auth


# In[3]:

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "hellouniverse"))


# In[4]:

session = driver.session()


# In[13]:

# Delete everything.
print session.run("MATCH (n)-[r]->() DELETE n,r")
print session.run("MATCH (n) DELETE n")


# ---
# ### Employees

# In[14]:

f = open('/home/ubuntu/DATA/employeelist.csv','r')

# Loop over all employees and add them as nodes.
t0 = time.time()
for line in f.readlines()[1:]:
    
    employee = line.replace('"','').split(',')
    
    eid = employee[0]
    efname = employee[1]
    elname = employee[2]
    estatus = employee[-2]
    einenron = "True"
    
    session.run("CREATE (person:Person {eid:"+eid+", first_name:'"+efname+"', last_name:'"+elname+"', status:'"+estatus+"', enron:'"+einenron+"'}) RETURN person").consume()
        
    #create email nodes
    for email in employee[3:7]: 
        if email != "":
            session.run("MATCH (person:Person) WHERE person.eid="+eid+" CREATE (person)-[r:has_address]->(email:EmailAddress {address:'"+email+"'})").consume()


print 'DONE! Time elapsed: {} seconds'.format(time.time()-t0)
f.close()


# ---
# ### Message

# In[18]:

f = open('/home/ubuntu/DATA/message.csv','r')

# Loop over all employees and add them as nodes.
t0 = time.time()
for e,line in enumerate(f.readlines()):
    
    message = line.replace('"','').split(',')
    
    # See if the sender exists...
    matches = session.run("MATCH (n:EmailAddress) WHERE n.address='"+message[1]+"' RETURN n.address")
    numMatches = len([ m for m in matches ])
    # If the sender does not exist, create the sender and the message together.
    if numMatches == 0:
        session.run("CREATE (n:EmailAddress {address:'"+message[1]+"'})-[r:Sent]->(e:Email {mid:"+message[0]+", subject:'"+message[4]+"', date:'"+message[2]+"'})").consume()
    else:
        # Create a node for the message object.
        session.run("MATCH (n:EmailAddress) WHERE n.address='"+message[1]+"' CREATE (n)-[r:Sent]->(email:Email {mid:"+message[0]+", subject:'"+message[4]+"', date:'"+message[2]+"'})").consume()
    
    if e % 1000 == 0:
        print e, '.',
    
    
print '\n\nDONE! Time elapsed: {} seconds'.format(time.time()-t0)
f.close()


# ---
# ### RecipientInfo

# In[20]:

f = open('/home/ubuntu/DATA/recipientinfo.csv','r')

# Loop over all employees and add them as nodes.
t0 = time.time()
for e,line in enumerate(f.readlines()):
    
    message = line.replace('"','').split(',')
    mid = message[1]
    rtype = message[2]
    rvalue = message[3]
    
    # See if the receiver exists...
    matches = session.run("MATCH (n:EmailAddress) WHERE n.address='" + rvalue + "' RETURN n.address")
    numMatches = len([ m for m in matches ])
    # If the receiver does not exist, create the sender and the message together.
    if numMatches == 0:
        session.run("MATCH (m:Email) WHERE m.mid="+mid+" CREATE (m)-[r:"+rtype+"]->(e:EmailAddress {address:'"+rvalue+"'})").consume()
    else:
        # Create a node for the message object.
        session.run("MATCH (m:Email), (e:EmailAddress) WHERE m.mid='"+mid+"' AND e.address='"+rvalue+"' CREATE (m)-[r:"+rtype+"]->(e)").consume()
    
    if e % 1000 == 0:
        print e, '.',
    
    
print '\n\nDONE! Time elapsed: {} seconds'.format(time.time()-t0)
f.close()


# In[ ]:



