# MySQL Tutorial

Duration: 15min.

* Who has sent most emails?
* Emails with most recipients
* Dates with most emails?

* Unique emailaddresses?


```bash
mysql> SHOW DATABASES;
mysql> USE enron;
```


```bash
mysql> SHOW TABLES;
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


```bash
SHOW COLUMNS FROM employeelist;
```


```bash
SELECT COUNT(*) FROM employeelist;
```

```bash
SELECT * FROM employeelist LIMIT 0,5;
```

```bash
SHOW COLUMNS FROM message;
```

```bash
SELECT COUNT(*) FROM message;
```

Lets answer a specific question. **Who has sent the most emails?** Luckily we have a column with the `sender` email address in the message table. So we can select all information in that table, return all unique senders and count how many emails were sent by them.

```bash
SELECT sender, COUNT(mid) AS numberOfEmails
FROM message
GROUP BY sender
ORDER BY numberOfEmails DESC
LIMIT 0,10;
```

This will give us the top 10 email-addresses that have sent most emails. This may be a great way to start from. Lets take a look at the employee-information for one of these email addresses.

```bash
SELECT *
FROM employeelist
WHERE email_id='jeff.dasovich@enron.com';
```

This gives us his employee-information. So we know two important things: he has three email addresses and his employee-id is 73. We can extend the previous query to make sure we account for all email addresses, but it will not have any impact:

```bash
SELECT sender, COUNT(mid) AS numberOfEmails
FROM message
WHERE RIGHT(sender,18)='dasovich@enron.com'
GROUP BY sender
ORDER BY numberOfEmails DESC;
```

Now lets see how often he is on the receiving end of emails

```bash
SELECT rtype, rvalue, COUNT(rid) AS numberOfEmails
FROM recipientinfo
WHERE RIGHT(rvalue,18)='dasovich@enron.com'
GROUP BY rvalue, rtype;
```

Linking up senders and receipients.

```bash
SELECT sender, rvalue, COUNT(rid) numberOfEmails
FROM message
RIGHT OUTER JOIN recipientinfo ON recipientinfo.mid=message.mid 
WHERE sender='jeff.dasovich@enron.com'
GROUP BY rvalue
ORDER BY numberOfEmails DESC
LIMIT 0,10;
```

We can even split it out by type.

```bash
SELECT sender, rvalue, rtype, COUNT(rid) numberOfEmails
FROM message
RIGHT OUTER JOIN recipientinfo ON recipientinfo.mid=message.mid 
WHERE sender='jeff.dasovich@enron.com'
GROUP BY rvalue, rtype
ORDER BY numberOfEmails DESC
LIMIT 0,20;
```

Other queries:

```bash
SELECT * 
FROM message 
WHERE date BETWEEN '2000-01-20 00:00:00' AND '2000-01-21 23:59:00' 
ORDER BY date DESC;
```
