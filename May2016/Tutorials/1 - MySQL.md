# MySQL Tutorial

Duration: 15min.

### Motivation

Relational databases, like MySQL, allow us to store "tables" of information, including the relationships between tables. For the enron corpus, you can get full information on the tables <a href="http://www.ahschulz.de/enron-email-data/">here</a>. 

The fact that we can connect tables, allows us to quickly answer questions like:


* Who has sent most emails?
* Emails with most recipients
* Dates with most emails?
* Unique email addresses?

We'll take a closer look at how to answer these questions using SQL -- the query language for MySQL.

### Accessing the data

To access MySQL, we will use the web interface <b>phpMyAdmin</b>. That allows us to write queries and interact with the data directly from the browser, without needing to access the server via the terminal. 

In your browsers, navigate to: http://journocoders.nupinion.com/phpmyadmin/

You can login with the following credentials:<br>
username: <strong>journocoders<br></strong>
password: <strong>hellouniverse</strong>

Once you have logged in, navigate to the <b>SQL</b> tab. This is where we can write our queries (top), and view the output (bottom).

## Tutorial

What databases are on the system?

```bash
SHOW DATABASES;
```

Click on `Show query box` to be able to write more queries. We can see Enron is a database, so let's select it:

```
USE enron;
```

What is in the Enron database? Let's see what tables are there:

```bash
USE enron;
SHOW TABLES;
```

The output should look like this:
```
+-----------------+
| Tables_in_enron |
+-----------------+
| employeelist    |
| message         |
| recipientinfo   |
| referenceinfo   |
+-----------------+
4 rows in set (0.00 sec)
```


### Exploration

Let's first focus at the employeelist. What are the columns in that table?

```bash
USE enron;
SHOW COLUMNS FROM employeelist;
```

How many employees are there in this table?

```bash
USE enron;
SELECT COUNT(*) FROM employeelist;
```

Let's look at the first 5 employees:

```bash
USE enron;
SELECT * FROM employeelist LIMIT 0,5;
```

What about the message table? That should hold information on emails. Let's look at the column names:

```bash
USE enron;
SHOW COLUMNS FROM message;
```

How many emails are there?

```bash
USE enron;
SELECT COUNT(*) FROM message;
```

Lets answer a specific question. **Who has sent the most emails?** 

Luckily we have a column with the `sender` email address in the message table. So we can select all information in that table, return all unique senders and count how many emails were sent by them.

We will use multiple things at once here:
* `GROUP BY` to aggregate information together
* `ORDER BY` to sort

Read out the query to see that it makes sense in English. Then paste it in the SQL tab:

```bash
USE enron;
SELECT sender, COUNT(mid) AS numberOfEmails
FROM message
GROUP BY sender
ORDER BY numberOfEmails DESC
LIMIT 0,10;
```

This will give us the top 10 email addresses that have sent most emails. We could have been finished here, except it's possible that there are people who use different addresses. If this has happened, then we need to merge their counts. 

Lets take a look at the employee-information for one of the email addresses above.

```bash
USE enron;
SELECT *
FROM employeelist
WHERE email_id='jeff.dasovich@enron.com';
```

This gives us his employee-information. So we know two important things: he has three email addresses and his employee-id is 73. We can extend the previous query to make sure we account for all of his email addresses:

```bash
USE enron;
SELECT sender, COUNT(mid) AS numberOfEmails
FROM message
WHERE RIGHT(sender,18)='dasovich@enron.com'
GROUP BY sender
ORDER BY numberOfEmails DESC;
```

As it turns out, accounting for multiple email addresses did not have any impact on Mr Dasovich's email count.

Try a few of the other addresses to see whether it makes a difference!

If you're keen to practice SQL a little more, feel free to continue exploring below. Otherwise switch to a different type of database!

### Exploration continued

Now lets see how often our persona is on the receiving end of emails:

```bash
USE enron;
SELECT rtype, rvalue, COUNT(rid) AS numberOfEmails
FROM recipientinfo
WHERE RIGHT(rvalue,18)='dasovich@enron.com'
GROUP BY rvalue, rtype;
```

Linking up senders and recipients, to see who jeff.dasovich@enron.com is emailing and how many emails he's sending them:

```bash
USE enron;
SELECT sender, rvalue, COUNT(rid) AS numberOfEmails
FROM message
RIGHT OUTER JOIN recipientinfo ON recipientinfo.mid=message.mid 
WHERE sender='jeff.dasovich@enron.com'
GROUP BY rvalue
ORDER BY numberOfEmails DESC
LIMIT 0,10;
```

We can even split it out by type:

```bash
USE enron;
SELECT sender, rvalue, rtype, COUNT(rid) numberOfEmails
FROM message
RIGHT OUTER JOIN recipientinfo ON recipientinfo.mid=message.mid 
WHERE sender='jeff.dasovich@enron.com'
GROUP BY rvalue, rtype
ORDER BY numberOfEmails DESC
LIMIT 0,20;
```

Spice up your queries even more, by adding date restrictions. Look at all emails between 20/01/2000 and 21/01/2000:

```bash
USE enron;
SELECT * 
FROM message 
WHERE date BETWEEN '2000-01-20 00:00:00' AND '2000-01-21 23:59:00' 
ORDER BY date DESC;
```
