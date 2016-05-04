# MySQL Tutorial

Duration: 15min.


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
mysql> SHOW COLUMNS FROM employeelist;
```


```bash
mysql> SELECT COUNT(*) FROM employeelist;
```

```bash
mysql> SELECT * FROM employeelist LIMIT 0,5;
```



```bash
mysql> SHOW COLUMNS FROM message;
```

```bash
mysql> SELECT COUNT(*) FROM message;
```


