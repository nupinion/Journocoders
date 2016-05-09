from py2neo import Graph, Path
import MySQLdb
import json
import os

# Open Neo4j connection
graph = Graph()

# Open database connection
db = MySQLdb.connect("localhost","root","journocoders","mysql" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

####################################################################################
# Create people nodes (and their email nodes)

# execute SQL query using execute() method.
cursor.execute("select * from employeelist")
# employees = cursor.fetchall()
employees = [list(i) for i in cursor.fetchall()] 


#### DELETE EVERYTHING
graph.cypher.execute("MATCH (n)-[r]->() DELETE n,r")
graph.cypher.execute("MATCH (n) DELETE n")


#### ADD EMPLOYEE INFO
for employee in employees:
	eid = int(employee[0])
	efname = employee[1]
	elname = employee[2]
	estatus = employee[-2]
	einenron = True
	tx = graph.cypher.begin()
	tx.append("CREATE (person:Person {eid:{eid}, first_name:{first_name}, last_name:{last_name}, status:{status}, enron:{enron}}) RETURN person", 
		eid=eid ,first_name=efname, last_name=elname, status=estatus, enron=einenron)
	tx.commit()
	#create email nodes
	for email in employee[3:7]:
		if email != "":
			tx = graph.cypher.begin()
			tx.append("MATCH (person:Person) WHERE person.eid={eid} CREATE  (person)-[r:has_address]->(email:EmailAddress {address:{address}})",
				eid=eid, address=email)
			tx.commit()


####################################################################################
# Now consider emails....
# execute SQL query using execute() method.
cursor.execute("select distinct(mid) from message")
message_ids = [int(i[0]) for i in cursor.fetchall()] 

cursor.execute("show columns from message")
message_cols = [i[0] for i in cursor.fetchall()] 

mcount = 0;
# Iterate over emails
for mid in message_ids:
	mcount += 1
	print str(mcount) + " of " + str(len(message_ids))
	########################################################################
	cursor.execute("select * from message where mid = '" + str(mid) +"'")
	curr_message = cursor.fetchall()[0];
	line2 = dict();
	for dd in range(0,len(curr_message)):
		if message_cols[dd] == "date":
			line2[message_cols[dd]] = unicode(curr_message[dd])
		else:
			line2[message_cols[dd]] = curr_message[dd]
	########################
	########################
	#Create Node for Email Object
	tx = graph.cypher.begin()
	tx.append("CREATE (email:Email {mid:{mid}, subject:{subject}, body:{body}})",
		mid = mid, subject = line2["subject"], body = line2["body"])
	tx.commit()
	########################
	########################
	#Create Edge from Sender
	########################
	########################
	sender_email = line2["sender"]
	results = graph.cypher.execute("MATCH (n:EmailAddress) WHERE n.address={address} RETURN n.address",address=sender_email)
	if len(results) > 0:
		#create edge
		res = graph.cypher.execute("MATCH (email:Email {mid:{mid}}), (sender:EmailAddress {address:{address}}) CREATE UNIQUE (sender)-[r:sent]->(email)",
			mid=mid, address=sender_email)
		res = graph.cypher.execute("MATCH (email:Email {mid:{mid}}), (sender:EmailAddress {address:{address}}) CREATE UNIQUE (sender)<-[r:From]-(email)",
			mid=mid, address=sender_email)
	else:
		#create node and edge
		res = graph.cypher.execute("MATCH (email:Email {mid:{mid}}) CREATE UNIQUE (sender {address:{address}})-[r:sent]->(email)",
			mid=mid, address=sender_email)
		res = graph.cypher.execute("MATCH (email:Email {mid:{mid}}) CREATE UNIQUE (sender:EmailAddress {address:{address}})<-[r:From]-(email)",
			mid=mid, address=sender_email)
	########################
	########################
	#connect to recipient
	########################
	########################
	cursor.execute('select rvalue, rtype from recipientinfo where recipientinfo.mid = '+ str(mid) +';')
	recipients = [[i[0],i[1]] for i in cursor.fetchall()] 
	all_recipients = []
	for curr_recipient in recipients:
		tmp = dict()
		recipient = curr_recipient[0]
		tmp["email"] = recipient
		tmp["type"] = curr_recipient[1]
		####
		####
		results = graph.cypher.execute("MATCH (n:EmailAddress) WHERE n.address={address} RETURN n.address",
			address=recipient)
		if len(results) > 0:
			#create edge
			res = graph.cypher.execute("MATCH (email:Email {mid:{mid}}), (recipient:EmailAddress {address:{address}}) CREATE UNIQUE (recipient)-[r:received {type:{type}}]->(email)",
				mid=mid, address=recipient, type=tmp["type"])
			res = graph.cypher.execute("MATCH (email:Email {mid:{mid}}), (recipient:EmailAddress {address:{address}}) CREATE UNIQUE (recipient)<-[r:To {type:{type}}]-(email)",
				mid=mid, address=recipient, type=tmp["type"])
		else:
			#create node and edge
			res = graph.cypher.execute("MATCH (email:Email {mid:{mid}}) CREATE UNIQUE (recipient:EmailAddress {address:{address}})-[r:received {type:{type}}]->(email)",
				mid=mid, address=recipient, type=tmp["type"])
			res = graph.cypher.execute("MATCH (email:Email {mid:{mid}}) CREATE UNIQUE (recipient:EmailAddress {address:{address}})<-[r:To {type:{type}}]-(email)",
				mid=mid, address=recipient, type=tmp["type"])
	# break
	################################################
	################################################
	# End node/edge creation for current email

# disconnect from server
db.close()