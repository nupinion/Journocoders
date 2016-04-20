import MySQLdb
import json
import os

# Open database connection
db = MySQLdb.connect("localhost","root","journocoders","mysql" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("select distinct(mid) from message")

# Fetch a single row using fetchone() method.
# data = cursor.fetchone()
#data = cursor.fetchall()
message_ids = [int(i[0]) for i in cursor.fetchall()] 

cursor.execute("show columns from message")
message_cols = [i[0] for i in cursor.fetchall()] 
cursor.execute("show columns from employeelist")
employee_cols = [i[0] for i in cursor.fetchall()] 

mcount = 0;
os.system("rm dump.jsonl")
for mid in message_ids:
	mcount += 1
	line1 = '{ "create":  {"_id":' + str(mid) + '}}'
	cursor.execute("select * from message where mid = '" + str(mid) +"'")
	curr_message = cursor.fetchall()[0];
	line2 = dict();
	for dd in range(0,len(curr_message)):
		if message_cols[dd] == "date":
			line2[message_cols[dd]] = unicode(curr_message[dd])
		else:
			line2[message_cols[dd]] = curr_message[dd]
	#connect to recipient
	cursor.execute('select rvalue,rtype from recipientinfo where recipientinfo.mid = '+ str(mid) +';')
	recipients = [[i[0],i[1]] for i in cursor.fetchall()] 
	print "the recipients"
	all_recipients = []
	for curr_recipient in recipients:
		tmp = dict()
		recipient = curr_recipient[0]
		tmp["email"] = recipient
		tmp["type"] = curr_recipient[1]
		cursor.execute('select * from employeelist where (employeelist.Email_id = "'+ recipient +'") OR (employeelist.Email2 = "'+ recipient +'") OR (employeelist.Email3 = "'+ recipient +'") OR (employeelist.Email4 = "'+ recipient +'");')
		employee_info = cursor.fetchall()
		if len(employee_info) > 0:
			tmp["internal"] = "True"
			tmp["firstName"] = employee_info[0][1]
			tmp["lastName"] = employee_info[0][2]
			tmp["status"] = employee_info[0][8]
		else:
			tmp["internal"] = "False"
			tmp["firstName"] = ""
			tmp["lastName"] = ""
			tmp["status"] = ""
		all_recipients.append(tmp)
	line2["recipients"] = all_recipients
	line2["number_recipients"] = len(all_recipients)
	#append to jsonl file
	with open("dump.jsonl", "a") as myfile:
		myfile.write(line1 + "\n")
		myfile.write(json.dumps(line2) + "\n")
	if mcount % 50000 == 0:
		'curl -s -XPOST http://127.0.0.1:9200/enron/emails/_bulk --data-binary "@dump.jsonl"'
		os.system("rm dump.jsonl")
		#read to es via bulk load
		#delete dump.jsonl
		# break
	#check for %%50000 for bulk load to es
	#and empty jsonl



print "Database version : %s " % data




{ "index":  {}}
{ "webTitle": "Denise", "description": "Xifara"}

# disconnect from server
db.close()