## MySQL

Link for download from: https://opendata.stackexchange.com/questions/3802/enron-email-dataset-in-mysql
Description of data: http://www.ahschulz.de/enron-email-data/

General setup: https://stackoverflow.com/questions/17666249/how-to-import-an-sql-file-using-the-command-line-in-mysql


Set up sql... scp the data to server. Then load:


~~~
mysql -u root -p mysql < enron-mysqldump_v5.sql
mysql
~~~

~~~
show databases;
use mysql;
show tables;

select * from employeelist;
select * from employeelist where lastName = "Heard";
select * from employeelist where not status = "NULL" and not status = "N/A";

SELECT COUNT(*) FROM message;
show columns from message;
select * from message limit 1;
select * from message where date = "2000-01-21";
select * from message where date between '2000-01-20 00:00:00' and '2000-01-21 23:59:00' order by date desc;
select count(*) from message where date between '2000-01-20 00:00:00' and '2000-01-21 23:59:00';

#senders
# have a look at the first 10 senders in the message table
select sender from message group_by sender limit 10;
# 
SELECT DISTINCT(sender) AS sender FROM message ORDER BY date DESC;
SELECT COUNT(DISTINCT sender) FROM message;
# get 10 most popular senders
SELECT COUNT(*) AS sender, sender FROM message GROUP BY sender ORDER BY sender DESC LIMIT 10;

# And what about the recipients?

show columns from recipientinfo;
select * from recipientinfo limit 1;
#ok we need an mid
SELECT DISTINCT(mid) AS sender FROM message limit 10;
select * from message where mid = 52;
select * from recipientinfo where mid = 52;
select mid from recipientinfo where rvalue = "all.worldwide@enron.com";
select count(mid) from recipientinfo where rvalue = "all.worldwide@enron.com";

select rvalue from recipientinfo where recipientinfo.mid = 100;

Select * from recipientinfo left join message on message.mid = recipientinfo.mid where message.mid = 100;

~~~
