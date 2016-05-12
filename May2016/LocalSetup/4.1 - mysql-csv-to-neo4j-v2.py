import json
import os
import time

import pandas as pd

from neo4j.v1 import GraphDatabase, basic_auth

import MySQLdb


driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "hellouniverse"))
session = driver.session()


# Delete everything.
_ = session.run("MATCH (n)-[r]->() DELETE n,r")
_ = session.run("MATCH (n) DELETE n")


# Open database connection
db = MySQLdb.connect("localhost","journocoders","hellouniverse","enron" )
# prepare a cursor object using cursor() method
cursor = db.cursor()

print 'DONE CONNECTING TO MYSQL'










# ---------------------------------------------
# EMPLOYEES
# ---------------------------------------------

# Create a pandas dataframe for the EMPLOYEES.
cursor.execute("SHOW COLUMNS FROM employeelist")
employee_cols = [ i[0] for i in cursor.fetchall() ] 
cursor.execute("SELECT * FROM employeelist")
employees = cursor.fetchall()
employees_array = [ e for e in employees ]
employees_df = pd.DataFrame.from_records(data=employees_array, index=None, columns=employee_cols)
employees = employees_array = None
print employees_df.head()


# Loop over all employees and add them as nodes.
t0 = time.time()
for i in employees_df.index:
    #
    eid = str(employees_df.ix[i].eid)
    efname = str(employees_df.ix[i].firstName)
    elname = str(employees_df.ix[i].lastName)
    estatus = str(employees_df.ix[i].status)
    einenron = "True"
    # Add the node to Neo4J
    _ = session.run("CREATE (person:Person { eid:"+eid+", first_name:'"+efname+"', last_name:'"+elname+"', status:'"+estatus+"', enron:'"+einenron+"' }) RETURN person").consume()
    # create email nodes
    for col in ['Email_id','Email2','Email3','EMail4']: 
        eaddress = employees_df.ix[i][col]
        if eaddress != "":
            _ = session.run("MATCH (person:Person) WHERE person.eid=" + eid + " CREATE (person)-[r:has_address]->(email:EmailAddress { address: '" + eaddress + "' })").consume()

#
print '\nDONE! Time elapsed: {} seconds\n\n'.format(time.time()-t0)










# ---------------------------------------------
# MESSAGES
# ---------------------------------------------

# Grab all emails in memory.
cursor.execute("SHOW COLUMNS FROM message")
message_cols = [ i[0] for i in cursor.fetchall() ] 
cursor.execute("SELECT * FROM message ORDER BY mid ASC")
messages = cursor.fetchall()


t0 = time.time()
for e,curr_message in enumerate(messages[10000:15000]):
    if curr_message[0] >= 0:
        #
        message = [ str(col).replace('\\','') for col in curr_message ]
        #
        matches = session.run("MATCH (n:EmailAddress) WHERE n.address='" + message[1] + "' RETURN n.address")
        numMatches = len([ m for m in matches ])
        # If the sender does not exist, create the sender and the message together.
        if numMatches == 0:
            _ = session.run("CREATE (n:EmailAddress { address: '" + message[1] + "' })-[r:Sent]->(e:Email { mid:" + message[0] + ", subject:'" + message[4] + "', date:'" + message[2] + "' })").consume()
            # _ = session.run("CREATE (n:EmailAddress { address: '" + message[1] + "' })<-[r:From]-(e:Email { mid:" + message[0] + ", subject:'" + message[4] + "', date:'" + message[2] + "' })").consume()
        else:
            # Create a node for the message object.
            _ = session.run("MATCH (n:EmailAddress) WHERE n.address='" + message[1] + "' CREATE (n)-[r:Sent]->(email:Email { mid:"+message[0]+", subject:'"+message[4]+"', date:'"+message[2]+"' })").consume()
            # _ = session.run("MATCH (n:EmailAddress) WHERE n.address='" + message[1] + "' CREATE (n)<-[r:From]-(email:Email { mid:"+message[0]+", subject:'"+message[4]+"', date:'"+message[2]+"' })").consume()
        if (e+1) % 1000 == 0:
            t1 = time.time()
            mins = (t1-t0) // 60
            secs = (t1-t0) % 60
            print 'Added {} nodes ({} minutes and {} seconds).'.format(e+1, mins, secs)
            print '\tLast added mid was {}\n'.format(message[0])
#
#   
print '\nDONE! Time elapsed: {} seconds\n\n'.format(time.time()-t0)













# ---------------------------------------------
# RECIPIENTS
# ---------------------------------------------

# Create a pandas dataframe for the RECIPIENTINFO.
cursor.execute("SHOW COLUMNS FROM recipientinfo")
recipientinfo_cols = [ i[0] for i in cursor.fetchall() ]
cursor.execute("SELECT * FROM recipientinfo ORDER BY mid ASC")
recipients = cursor.fetchall()
recipients_array = [ r for r in recipients ]
recipients_df = pd.DataFrame.from_records(data=recipients_array, index=recipientinfo_cols[0], columns=recipientinfo_cols)
recipients = recipients_array = None
print recipients_df.head()

# Loop over all employees and add them as nodes.
t0 = time.time()
for e,i in enumerate(recipients_df.index):
    #
    if recipients_df.ix[i].mid < 12413:
        #
        mid = str(recipients_df.ix[i].mid)
        rtype = str(recipients_df.ix[i].rtype)
        rvalue = str(recipients_df.ix[i].rvalue)
        
        # See if the receiver exists...
        matches = session.run("MATCH (n:EmailAddress) WHERE n.address='" + rvalue + "' RETURN n.address")
        numMatches = len([ m for m in matches ])
        # If the receiver does not exist, create the sender and the message together.
        if numMatches == 0:
            _ = session.run("MATCH (m:Email) WHERE m.mid=" + mid + " CREATE (m)<-[r:Received {type:'" + rtype + "'}]-(e:EmailAddress {address:'" + rvalue + "'})").consume()
            # _ = session.run("MATCH (m:Email) WHERE m.mid=" + mid + " CREATE (m)-[r:To {type:'" + rtype + "'}]->(e:EmailAddress {address:'" + rvalue + "'})").consume()
        else:
            # Create a node for the message object.
            _ = session.run("MATCH (m:Email), (e:EmailAddress) WHERE m.mid=" + mid + " AND e.address='" + rvalue + "' CREATE (m)<-[r:Received {type:'" + rtype + "'}]-(e)").consume()
            # _ = session.run("MATCH (m:Email), (e:EmailAddress) WHERE m.mid=" + mid + " AND e.address='" + rvalue + "' CREATE (m)-[r:To {type:'" + rtype + "'}]->(e)").consume()
        # Show results...
        if (e+1) % 500 == 0:
            t1 = time.time()
            mins = (t1-t0) // 60
            secs = (t1-t0) % 60
            print 'Added {} recipients ({} minutes and {} seconds).'.format(e+1, mins, secs)
            print '\tLast added mid was {}\n'.format(mid)
    
    
print '\nDONE! Time elapsed: {} seconds'.format(time.time()-t0)


