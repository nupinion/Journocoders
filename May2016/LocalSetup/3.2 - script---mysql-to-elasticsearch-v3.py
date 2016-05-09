import json
import os
import time

import pandas as pd

import MySQLdb


# =======================================================================


# Clean up any previous files.
os.system("rm dump.jsonl")


# Open database connection
db = MySQLdb.connect("localhost","journocoders","hellouniverse","enron" )

# prepare a cursor object using cursor() method
cursor = db.cursor()


# Create a pandas dataframe for the EMPLOYEES.
cursor.execute("SHOW COLUMNS FROM employeelist")
employee_cols = [ i[0] for i in cursor.fetchall() ] 
cursor.execute("SELECT * FROM employeelist")
employees = cursor.fetchall()
employees_array = [ e for e in employees ]
employees_df = pd.DataFrame.from_records(data=employees_array, index=employee_cols[0], columns=employee_cols)
employees = employees_array = None


# Create a pandas dataframe for the RECIPIENTINFO.
cursor.execute("SHOW COLUMNS FROM recipientinfo")
recipientinfo_cols = [ i[0] for i in cursor.fetchall() ]
cursor.execute("SELECT * FROM recipientinfo")
recipients = cursor.fetchall()
recipients_array = [ r for r in recipients ]
recipients_df = pd.DataFrame.from_records(data=recipients_array, index=recipientinfo_cols[0], columns=recipientinfo_cols)
recipients = recipients_array = None

 
# Grab all emails in memory.
cursor.execute("SHOW COLUMNS FROM message")
message_cols = [ i[0] for i in cursor.fetchall() ] 
cursor.execute("SELECT * FROM message")
messages = cursor.fetchall()


print '*** DONE LOADING DATA FROM MYSQL...\n\n'


# Get starting time.
t0 = time.time()


for e,curr_message in enumerate(messages):
    #
    mid = curr_message[0]
    #
    line1 = '{ "create": { "_id": ' + str(mid) + '}}'
    line2 = dict()
    #
    for dd in range(0,len(curr_message)):
        if message_cols[dd] == "date":
            line2[message_cols[dd]] = unicode(curr_message[dd])
        else:
            line2[message_cols[dd]] = curr_message[dd]
    #
    # Get the recipients for the current email-message.
    curr_recipients = recipients_df[recipients_df.mid == mid]
    all_recipients = []
    # For each of the recipients found
    for r in curr_recipients.index:
        #
        this_address = curr_recipients.ix[r].rvalue
        this_recipient = dict()
        this_recipient["email"] = this_address
        this_recipient["type"] = curr_recipients.ix[r].rtype
        #
        # Get their employee information if available.
        this_employee = employees_df[(employees_df.Email_id==this_address)|(employees_df.Email2==this_address)|(employees_df.Email3==this_address)|(employees_df.EMail4==this_address)]
        if this_employee.shape[0] > 0:
            eid = list(this_employee.index)[0]
            this_recipient["internal"] = "True"
            this_recipient["firstName"] = this_employee.loc[eid,'firstName']
            this_recipient["lastName"] = this_employee.loc[eid,'lastName']
            this_recipient["status"] = this_employee.loc[eid,'status']
        else:
            this_recipient["internal"] = "False"
            this_recipient["firstName"] = ""
            this_recipient["lastName"] = ""
            this_recipient["status"] = ""
        # Done... now add the the list of recipients...
        all_recipients.append(this_recipient)
    #
    line2["recipients"] = all_recipients
    line2["number_recipients"] = curr_recipients.shape[0]
    #
    #append to jsonl file
    with open("dump.jsonl", "a") as myfile:
        myfile.write(line1 + "\n")
        myfile.write(json.dumps(line2) + "\n")

    if (e+1) % 5000 == 0:
        os.system('curl -s -XPOST http://127.0.0.1:9200/enron/emails/_bulk --data-binary "@dump.jsonl"')
        os.system("rm dump.jsonl")
        print 10 * '.\n'
        print '{}({}sec)'.format(str(e+1),time.time()-t0)
        t0 = time.time()


os.system('curl -s -XPOST http://127.0.0.1:9200/enron/emails/_bulk --data-binary "@dump.jsonl"')
os.system("rm dump.jsonl")

# disconnect from server
db.close()


print 'DONE!'
