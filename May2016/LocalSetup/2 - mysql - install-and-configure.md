# MySQL Installation and Configuration

To install MySQL you can follow the following blog

* https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-14-04

or, for the default installation, use the following four commands:

```bash
$ sudo apt-get update
$ sudo apt-get install mysql-server
$ sudo mysql_secure_installation
$ sudo mysql_install_db
```

You can see if the database is running by checking its status:

```bash
$ sudo service mysql status
mysql start/running, process XXXX
```


To check if everything work we can login to the database using:

```bash
$ mysql -u root -p
```

Once logged in we can run the following command to see all the databases:

```bash
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
3 rows in set (0.00 sec)
```

Lets create a new database to hold all the Enron data:

```bash
mysql> CREATE DATABASE enron;
```

```bash
mysql> CREATE USER 'journocoders'@'localhost' IDENTIFIED BY 'hellouniverse';
mysql> GRANT SELECT ON enron.* TO 'journocoders'@'localhost';
mysql> FLUSH PRIVILEGES;
```

This should do it! Now to proceed we will exit MySQL and load the data.

You can exit by running `exit;`

Load the `mysql -u root -p enron < <PATH_TO_FILE>enron-mysqldump_v5.sql`


### Install PhpMyAdmin

https://www.liquidweb.com/kb/how-to-install-and-configure-phpmyadmin-on-ubuntu-14-04/

```bash
sudo apt-get -y install phpmyadmin
```

URL: http://54.171.120.83/phpmyadmin


