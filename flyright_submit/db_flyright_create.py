"""-- MySQL dump 10.9
--
-- Host: localhost    Database: db_flyright
-- ------------------------------------------------------
-- Server version	4.1.22-community-nt"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
############################################################################################
# File:     createDB.py
# Author:   Kaia Chapman
# Version:  1.0
# Purpose:  create db_flyright database & populate with test data
"""##########################################db_flyright####################################
PAYMENT:
+-----------+--------------+------+-----+---------------------+----------------+
| Field     | Type         | Null | Key | Default             | Extra          |
+-----------+--------------+------+-----+---------------------+----------------+
| id        | mediumint(9) |      | PRI | NULL                | auto_increment |
| amount    | decimal(7,2) |      |     | 0.00                |                |
| day       | datetime     |      |     | 0000-00-00 00:00:00 |                |
| method    | varchar(11)  |      |     |                     |                |
| number    | bigint(20)   |      |     | 0                   |                |
| ccv       | smallint(6)  |      |     | 0                   |                |
| card_date | datetime     |      |     | 0000-00-00 00:00:00 |                |
| card_name | varchar(30)  |      |     |                     |                |
+-----------+--------------+------+-----+---------------------+----------------+
RESERVATION:
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | mediumint(9) |      | PRI | NULL    | auto_increment |
| payment_id | mediumint(9) |      | MUL | 0       |                |
+------------+--------------+------+-----+---------+----------------+
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| id             | mediumint(9) |      | PRI | NULL    | auto_increment |
| customer_id    | mediumint(9) |      | MUL | 0       |                |
| reservation_id | mediumint(9) |      | MUL | 0       |                |
| seat_id        | mediumint(9) |      | MUL | 0       |                |
| meal           | tinyint(1)   |      |     | 0       |                |
| bags           | int(2)       |      |     | 0       |                |
| assist         | tinyint(1)   |      |     | 0       |                |
| comment        | varchar(200) | YES  |     | NULL    |                |
| class          | tinyint(1)   |      |     | 0       |                |
+----------------+--------------+------+-----+---------+----------------+
CUSTOMER:    
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| id      | mediumint(9) |      | PRI | NULL    | auto_increment |
| fname   | varchar(20)  |      |     |         |                |
| lname   | varchar(30)  |      |     |         |                |
| address | varchar(200) |      |     |         |                |
| city    | varchar(50)  |      |     |         |                |
| zip     | int(11)      |      |     | 0       |                |
| email   | varchar(100) | YES  |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+
SEAT:
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | mediumint(9) |      | PRI | NULL    | auto_increment |
| position  | char(1)      |      |     |         |                |
| flight_id | mediumint(9) |      | MUL | 0       |                |
| available | tinyint(1)   |      |     | 1       |                |
+-----------+--------------+------+-----+---------+----------------+
FLIGHT:
+-------------------+--------------+------+-----+---------------------+----------------+
| Field             | Type         | Null | Key | Default             | Extra          |
+-------------------+--------------+------+-----+---------------------+----------------+
| id                | mediumint(9) |      | PRI | NULL                | auto_increment |
| depart_airport_id | mediumint(9) |      | MUL | 0                   |                |
| arrive_airport_id | mediumint(9) |      | MUL | 0                   |                |
| depart_dt         | datetime     |      |     | 0000-00-00 00:00:00 |                |
| arrive_dt         | datetime     |      |     | 0000-00-00 00:00:00 |                |
| rate_id           | mediumint(9) |      | MUL | 0                   |                |
+-------------------+--------------+------+-----+---------------------+----------------+
AIRPORT:
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | mediumint(9) |      | PRI | NULL    | auto_increment |
| city  | varchar(20)  |      |     |         |                |
| state | char(3)      |      |     |         |                |
| name  | varchar(4)   |      |     |         |                |
+-------+--------------+------+-----+---------+----------------+
RATE:
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | mediumint(9) |      | PRI | NULL    | auto_increment |
| coach      | decimal(8,2) | YES  |     | NULL    |                |
| firstclass | decimal(8,2) | YES  |     | NULL    |                |
| adjust     | decimal(4,2) | YES  |     | 0.00    |                |
+------------+--------------+------+-----+---------+----------------+
"""#########################################################################################
import pymysql

class createDB:
    ###########################
    def __init__(self): #constuctor
        self.cnx = pymysql.connect(user='root', passwd='Redfox1!',
                                      host='127.0.0.1', port=3306)
        self.cursor=self.cnx.cursor()


        self.cursor.execute("/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;")
        self.cursor.execute("/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;")
        self.cursor.execute("/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;")
        self.cursor.execute("/*!40101 SET NAMES utf8 */;")
        self.cursor.execute("/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;")
        self.cursor.execute("/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;")
        self.cursor.execute("/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;")
        self.cursor.execute("/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;")

        """--
        -- Current Database: `db_flyright`
        --"""

        self.cursor.execute("CREATE DATABASE /*!32312 IF NOT EXISTS*/ `db_flyright` /*!40100 DEFAULT CHARACTER SET latin1 */;")

        self.cursor.execute("USE `db_flyright`;")

        """--
        -- Table structure for table `airport`
        --"""

        self.cursor.execute("DROP TABLE IF EXISTS `airport`;")
        self.cursor.execute("""CREATE TABLE `airport` (
          `id` mediumint(9) NOT NULL auto_increment,
          `city` varchar(20) NOT NULL default '',
          `state` char(3) NOT NULL default '',
          `name` varchar(4) NOT NULL default '',
          PRIMARY KEY  (`id`),
          UNIQUE KEY `name` (`name`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""")

        """--
        -- Dumping data for table `airport`
        --"""

        self.cursor.execute("LOCK TABLES `airport` WRITE;")
        self.cursor.execute("/*!40000 ALTER TABLE `airport` DISABLE KEYS */;")
        self.cursor.execute("INSERT INTO `airport` VALUES (1,'Dallas','TX','DFW'),(2,'Los Angeles','CA','LAX'),(3,'Denver','CO','DIA'),(4,'Las Vegas','NV','LAS'),(5,'Miami','FL','MIA'),(6,'San Francisco','CA','SFO'),(7,'New York','NY','JFK');")
        self.cursor.execute("/*!40000 ALTER TABLE `airport` ENABLE KEYS */;")
        self.cursor.execute("UNLOCK TABLES;")

        """--
        -- Table structure for table `customer`
        --"""

        self.cursor.execute("DROP TABLE IF EXISTS `customer`;")
        self.cursor.execute("""CREATE TABLE `customer` (
          `id` mediumint(9) NOT NULL auto_increment,
          `fname` varchar(20) NOT NULL default '',
          `lname` varchar(30) NOT NULL default '',
          `address` varchar(200) NOT NULL default '',
          `city` varchar(50) NOT NULL default '',
          `zip` int(11) NOT NULL default '0',
          `email` varchar(100) default NULL,
          PRIMARY KEY  (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""")

        """--
        -- Dumping data for table `customer`
        --"""

        self.cursor.execute("LOCK TABLES `customer` WRITE;")
        self.cursor.execute("/*!40000 ALTER TABLE `customer` DISABLE KEYS */;")
        self.cursor.execute("INSERT INTO `customer` VALUES (22,'Kaia','Chapman','555 A St.','Houston',80454,NULL),(24,'Joe','Blow','555 someplace','Houston',55555,NULL),(25,'Jolene','Blow','555 someplace','Houston',55555,NULL),(35,'Jill','Rogers','123 Brook St','Houston',11111,NULL),(40,'Zoe','Zhara','123 B St','Houston',84896,NULL),(41,'Ely','Ericson','123 B St','Houston',55555,NULL),(42,'JAROD','JACOBSON','123 B St','Houston',55544,NULL),(43,'Jodi','Culpepper','123 B St','Houston',88578,NULL),(44,'John','Jacob','123 B St','Houston',58854,NULL),(45,'JOLENE','JARODSON','123 B St','Houston',85878,NULL),(48,'Abe','Bee','123 B St','Houston',56855,NULL),(49,'Sarah','Rodreguez','123 B St','Houston',90210,NULL),(50,'Jerry','Garcia','123 B St','Houston',64888,NULL),(51,'Harry','Haroldson','123 B St','Houston',55786,NULL),(52,'Herietta','Haroldson','123 B St','Houston',55786,NULL),(60,'John','Smith','123 B St','Houston',57885,NULL),(61,'Jill','Smith','123 B St','Houston',57885,NULL),(62,'Jill','Johnson','123 B St','Houston',88888,NULL),(63,'Jake','Johnson','123 B St','Houston',88888,NULL),(64,'john','jacob','123 B St','Houston',88685,NULL),(65,'jill','jacob','123 B St','Houston',88685,NULL),(66,'Mo','Jacobson','123 B St','Houston',55888,NULL),(67,'Mary','Johnson','123 B St','Houston',55888,NULL),(68,'a','b','123 B St','Houston',54544,NULL),(69,'h','i','123 B St','d',54544,NULL),(70,'Jill','McCoy','123 B St','Houston',44554,NULL),(75,'Jolene','Johnson','555 someplace','Houston',55555,NULL);")
        self.cursor.execute("/*!40000 ALTER TABLE `customer` ENABLE KEYS */;")
        self.cursor.execute("UNLOCK TABLES;")

        """--
        -- Table structure for table `flight`
        --"""

        self.cursor.execute("DROP TABLE IF EXISTS `flight`;")
        self.cursor.execute("""CREATE TABLE `flight` (
          `id` mediumint(9) NOT NULL auto_increment,
          `depart_airport_id` mediumint(9) NOT NULL default '0',
          `arrive_airport_id` mediumint(9) NOT NULL default '0',
          `depart_dt` datetime NOT NULL default '0000-00-00 00:00:00',
          `arrive_dt` datetime NOT NULL default '0000-00-00 00:00:00',
          `rate_id` mediumint(9) NOT NULL default '0',
          PRIMARY KEY  (`id`),
          KEY `depart_airport_id` (`depart_airport_id`),
          KEY `arrive_airport_id` (`arrive_airport_id`),
          KEY `rate_id` (`rate_id`),
          CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`depart_airport_id`) REFERENCES `airport` (`id`),
          CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`arrive_airport_id`) REFERENCES `airport` (`id`),
          CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`rate_id`) REFERENCES `rate` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""")

        """--
        -- Dumping data for table `flight`
        --"""

        self.cursor.execute("LOCK TABLES `flight` WRITE;")
        self.cursor.execute("/*!40000 ALTER TABLE `flight` DISABLE KEYS */;")
        self.cursor.execute("INSERT INTO `flight` VALUES (4,1,2,'2015-04-25 01:52:00','2015-04-25 03:46:00',3),(5,1,3,'2015-04-27 01:02:00','2015-04-27 02:26:00',2),(6,2,1,'2015-04-27 15:02:00','2015-04-27 16:26:00',3),(7,3,1,'2015-04-27 23:02:00','2015-04-27 01:26:00',1),(8,4,1,'2015-04-28 23:02:00','2015-04-28 01:56:00',3),(9,5,1,'2015-04-28 23:02:00','2015-04-28 01:56:00',4),(10,5,3,'2015-04-28 23:02:00','2015-04-28 01:56:00',5),(11,5,2,'2015-04-28 23:02:00','2015-04-28 01:56:00',7),(12,5,2,'2015-04-28 23:02:00','2015-04-28 00:00:00',7),(13,2,5,'2015-04-25 11:02:00','2015-04-25 15:56:00',7),(14,3,2,'2015-04-29 08:59:00','2015-04-29 01:02:00',3),(15,3,2,'2015-05-02 08:59:00','2015-05-02 01:02:00',3),(16,3,4,'2015-05-02 08:59:00','2015-05-02 01:02:00',1),(17,4,2,'2015-05-02 02:59:00','2015-05-02 05:02:00',1),(18,4,2,'2015-05-02 04:59:00','2015-05-02 06:02:00',1),(19,3,4,'2015-04-29 15:26:00','2015-04-30 17:26:00',2),(20,4,3,'2015-04-29 15:26:00','2015-04-30 17:26:00',2),(21,6,1,'2015-04-26 15:19:00','2015-04-16 00:00:00',3),(22,6,7,'2015-04-27 09:26:00','2015-04-27 12:52:00',5),(23,6,5,'2015-04-27 09:26:00','2015-04-27 12:52:00',5),(24,7,5,'2015-04-27 09:26:00','2015-04-27 12:52:00',5),(25,7,4,'2015-04-27 09:26:00','2015-04-27 12:52:00',5),(26,7,1,'2015-04-27 09:26:00','2015-04-27 12:52:00',5),(27,7,3,'2015-04-27 09:26:00','2015-04-27 12:52:00',5);")
        self.cursor.execute("/*!40000 ALTER TABLE `flight` ENABLE KEYS */;")
        self.cursor.execute("UNLOCK TABLES;")

        """--
        -- Table structure for table `passenger`
        --"""

        self.cursor.execute("DROP TABLE IF EXISTS `passenger`;")
        self.cursor.execute("""CREATE TABLE `passenger` (
          `id` mediumint(9) NOT NULL auto_increment,
          `customer_id` mediumint(9) NOT NULL default '0',
          `reservation_id` mediumint(9) NOT NULL default '0',
          `seat_id` mediumint(9) NOT NULL default '0',
          `meal` tinyint(1) NOT NULL default '0',
          `bags` int(2) NOT NULL default '0',
          `assist` tinyint(1) NOT NULL default '0',
          `comment` varchar(200) default NULL,
          `class` tinyint(1) NOT NULL default '0',
          PRIMARY KEY  (`id`),
          UNIQUE KEY `seat_id` (`seat_id`),
          KEY `customer_id` (`customer_id`),
          KEY `reservation_id` (`reservation_id`),
          CONSTRAINT `passenger_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
          CONSTRAINT `passenger_ibfk_2` FOREIGN KEY (`reservation_id`) REFERENCES `reservation` (`id`),
          CONSTRAINT `passenger_ibfk_3` FOREIGN KEY (`seat_id`) REFERENCES `seat` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""")

        """--
        -- Dumping data for table `passenger`
        --"""

        self.cursor.execute("LOCK TABLES `passenger` WRITE;")
        self.cursor.execute("/*!40000 ALTER TABLE `passenger` DISABLE KEYS */;")
        self.cursor.execute("INSERT INTO `passenger` VALUES (44,24,48,15,1,1,0,NULL,1),(45,24,48,158,1,1,0,NULL,1),(46,24,48,27,1,1,0,NULL,1),(47,75,48,16,1,2,0,'Vegetarian',1),(48,75,48,159,1,2,0,'Vegetarian',1),(49,75,48,28,1,2,0,'Vegetarian',1),(50,22,49,41,1,1,0,'extra peanuts',1),(51,22,49,160,1,1,0,'extra peanuts',1);")
        self.cursor.execute("/*!40000 ALTER TABLE `passenger` ENABLE KEYS */;")
        self.cursor.execute("UNLOCK TABLES;")

        """--
        -- Table structure for table `payment`
        --"""

        self.cursor.execute("DROP TABLE IF EXISTS `payment`;")
        self.cursor.execute("""CREATE TABLE `payment` (
          `id` mediumint(9) NOT NULL auto_increment,
          `amount` decimal(7,2) NOT NULL default '0.00',
          `day` datetime NOT NULL default '0000-00-00 00:00:00',
          `method` varchar(11) NOT NULL default '',
          `number` bigint(20) NOT NULL default '0',
          `ccv` smallint(6) NOT NULL default '0',
          `card_date` datetime NOT NULL default '0000-00-00 00:00:00',
          `card_name` varchar(30) NOT NULL default '',
          PRIMARY KEY  (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""")

        """--
        -- Dumping data for table `payment`
        --"""

        self.cursor.execute("LOCK TABLES `payment` WRITE;")
        self.cursor.execute("/*!40000 ALTER TABLE `payment` DISABLE KEYS */;")
        self.cursor.execute("INSERT INTO `payment` VALUES (57,'339.00','2015-04-22 20:56:28','MasterCard',1585878585558855,589,'2015-11-28 00:00:00','J J BLOW'),(58,'389.00','2015-04-22 21:29:58','MasterCard',6168168168033666,478,'2017-09-19 00:00:00','KAIA A CHAPMAN'),(59,'120.00','2015-04-22 22:36:52','MasterCard',1686848334464646,466,'2017-12-15 00:00:00','JILL ROGERS');")
        self.cursor.execute("/*!40000 ALTER TABLE `payment` ENABLE KEYS */;")
        self.cursor.execute("UNLOCK TABLES;")

        """--
        -- Table structure for table `rate`
        --"""

        self.cursor.execute("DROP TABLE IF EXISTS `rate`;")
        self.cursor.execute("""CREATE TABLE `rate` (
          `id` mediumint(9) NOT NULL auto_increment,
          `coach` decimal(8,2) default NULL,
          `firstclass` decimal(8,2) default NULL,
          `adjust` decimal(4,2) default '0.00',
          PRIMARY KEY  (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""")

        """--
        -- Dumping data for table `rate`
        --"""

        self.cursor.execute("LOCK TABLES `rate` WRITE;")
        self.cursor.execute("/*!40000 ALTER TABLE `rate` DISABLE KEYS */;")
        self.cursor.execute("INSERT INTO `rate` VALUES (1,'100.00','120.00','0.00'),(2,'79.00','100.00','0.00'),(3,'120.00','160.00','0.00'),(4,'150.00','220.00','0.00'),(5,'200.00','310.00','0.00'),(6,'300.00','420.00','0.00'),(7,'400.00','500.00','0.00');")
        self.cursor.execute("/*!40000 ALTER TABLE `rate` ENABLE KEYS */;")
        self.cursor.execute("UNLOCK TABLES;")

        """--
        -- Table structure for table `reservation`
        --"""

        self.cursor.execute("DROP TABLE IF EXISTS `reservation`;")
        self.cursor.execute("""CREATE TABLE `reservation` (
          `id` mediumint(9) NOT NULL auto_increment,
          `payment_id` mediumint(9) NOT NULL default '0',
          PRIMARY KEY  (`id`),
          KEY `payment_id` (`payment_id`),
          CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""")

        """--
        -- Dumping data for table `reservation`
        --"""

        self.cursor.execute("LOCK TABLES `reservation` WRITE;")
        self.cursor.execute("/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;")
        self.cursor.execute("INSERT INTO `reservation` VALUES (48,57),(49,58),(50,59);")
        self.cursor.execute("/*!40000 ALTER TABLE `reservation` ENABLE KEYS */;")
        self.cursor.execute("UNLOCK TABLES;")

        """--
        -- Table structure for table `seat`
        --"""

        self.cursor.execute("DROP TABLE IF EXISTS `seat`;")
        self.cursor.execute("""CREATE TABLE `seat` (
          `id` mediumint(9) NOT NULL auto_increment,
          `position` char(1) NOT NULL default '',
          `flight_id` mediumint(9) NOT NULL default '0',
          `available` tinyint(1) NOT NULL default '1',
          `class` char(1) NOT NULL default 'C',
          PRIMARY KEY  (`id`),
          KEY `flight_id` (`flight_id`),
          CONSTRAINT `seat_ibfk_1` FOREIGN KEY (`flight_id`) REFERENCES `flight` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""")

        """--
        -- Dumping data for table `seat`
        --"""

        self.cursor.execute("LOCK TABLES `seat` WRITE;")
        self.cursor.execute("/*!40000 ALTER TABLE `seat` DISABLE KEYS */;")
        self.cursor.execute("INSERT INTO `seat` VALUES (14,'I',4,1,'C'),(15,'I',5,0,'C'),(16,'I',5,0,'C'),(17,'C',5,1,'C'),(18,'C',5,1,'C'),(19,'C',5,1,'C'),(20,'C',5,1,'C'),(21,'I',5,1,'C'),(22,'I',5,1,'C'),(23,'I',6,1,'C'),(24,'I',6,1,'C'),(25,'I',7,1,'C'),(26,'I',7,1,'C'),(27,'I',8,0,'C'),(28,'I',8,0,'C'),(29,'I',8,1,'C'),(30,'I',8,1,'C'),(31,'W',8,1,'C'),(32,'I',8,1,'C'),(33,'W',8,1,'C'),(34,'W',8,1,'C'),(35,'W',9,1,'C'),(36,'W',9,1,'C'),(37,'W',9,1,'C'),(38,'W',9,1,'C'),(39,'I',9,1,'C'),(40,'I',9,1,'C'),(41,'I',10,0,'C'),(42,'I',10,1,'C'),(43,'I',10,1,'C'),(44,'I',11,1,'C'),(45,'I',11,1,'C'),(46,'W',11,1,'C'),(47,'W',11,1,'C'),(48,'W',11,1,'C'),(49,'C',11,1,'C'),(50,'C',12,1,'C'),(51,'C',12,1,'C'),(52,'I',12,1,'C'),(53,'I',12,1,'C'),(54,'I',13,1,'C'),(55,'I',14,1,'C'),(56,'I',16,1,'C'),(57,'I',15,1,'C'),(58,'I',17,0,'C'),(59,'I',18,1,'C'),(60,'I',18,1,'C'),(61,'I',18,1,'C'),(62,'I',18,1,'C'),(63,'I',18,1,'C'),(64,'I',18,1,'C'),(65,'I',27,1,'C'),(66,'I',27,1,'C'),(67,'I',27,1,'C'),(68,'W',27,1,'C'),(69,'W',27,1,'C'),(70,'C',27,1,'C'),(71,'C',27,1,'C'),(72,'C',26,1,'C'),(73,'C',26,1,'C'),(74,'W',26,1,'C'),(75,'W',26,1,'C'),(76,'W',26,1,'C'),(77,'W',26,1,'C'),(78,'I',26,1,'C'),(79,'I',25,1,'C'),(80,'I',25,1,'C'),(81,'W',25,1,'C'),(82,'W',25,1,'C'),(83,'W',24,1,'C'),(84,'W',24,1,'C'),(85,'W',24,1,'C'),(86,'I',24,1,'C'),(87,'I',24,1,'C'),(88,'I',24,1,'C'),(89,'I',23,1,'C'),(90,'I',23,1,'C'),(91,'I',23,1,'C'),(92,'I',22,1,'C'),(93,'I',22,1,'C'),(94,'I',22,1,'C'),(95,'I',22,1,'C'),(96,'C',22,1,'C'),(97,'C',22,1,'C'),(98,'C',21,1,'C'),(99,'C',21,1,'C'),(100,'W',21,1,'C'),(101,'W',21,1,'C'),(102,'W',21,1,'C'),(103,'I',21,1,'C'),(104,'I',21,1,'C'),(105,'I',21,1,'C'),(106,'I',20,1,'C'),(107,'I',20,1,'C'),(108,'I',20,1,'C'),(109,'W',20,1,'C'),(110,'W',20,1,'C'),(111,'W',20,1,'C'),(112,'W',4,1,'F'),(113,'W',4,1,'F'),(114,'W',4,1,'F'),(115,'W',5,1,'F'),(116,'W',5,1,'F'),(117,'W',5,1,'F'),(118,'W',6,1,'F'),(119,'W',6,1,'F'),(120,'W',6,1,'F'),(121,'W',7,1,'F'),(122,'W',7,1,'F'),(123,'W',8,1,'F'),(124,'W',8,1,'F'),(125,'W',8,1,'F'),(126,'W',9,1,'F'),(127,'W',9,1,'F'),(128,'W',9,1,'F'),(129,'W',10,1,'F'),(130,'W',10,1,'F'),(131,'W',10,1,'F'),(132,'W',11,1,'F'),(133,'W',11,1,'F'),(134,'W',11,1,'F'),(135,'W',12,1,'F'),(136,'W',12,1,'F'),(137,'W',12,1,'F'),(138,'W',13,1,'F'),(139,'W',13,1,'F'),(140,'W',13,1,'F'),(141,'W',14,1,'F'),(142,'W',14,1,'F'),(143,'W',14,1,'F'),(144,'W',15,1,'F'),(145,'W',15,1,'F'),(146,'W',15,1,'F'),(147,'W',15,1,'F'),(148,'W',16,1,'F'),(149,'W',16,1,'F'),(150,'W',16,1,'F'),(151,'W',16,1,'F'),(152,'W',17,1,'F'),(153,'W',17,1,'F'),(154,'W',17,1,'F'),(155,'W',18,1,'F'),(156,'W',18,1,'F'),(157,'W',18,1,'F'),(158,'W',19,0,'F'),(159,'W',19,0,'F'),(160,'W',19,0,'F'),(161,'W',20,1,'F'),(162,'W',20,1,'F'),(163,'W',20,1,'F'),(164,'W',21,1,'F'),(165,'W',21,1,'F'),(166,'W',21,1,'F'),(167,'W',22,1,'F'),(168,'W',22,1,'F'),(169,'W',22,1,'F'),(170,'W',23,1,'F'),(171,'W',23,1,'F'),(172,'W',23,1,'F'),(173,'W',24,1,'F'),(174,'W',24,1,'F'),(175,'W',24,1,'F'),(176,'W',25,1,'F'),(177,'W',25,1,'F'),(178,'W',25,1,'F'),(179,'W',26,1,'F'),(180,'W',26,1,'F'),(181,'W',26,1,'F'),(182,'W',27,1,'F'),(183,'W',27,1,'F'),(184,'W',27,1,'F');")
        self.cursor.execute("/*!40000 ALTER TABLE `seat` ENABLE KEYS */;")
        self.cursor.execute("UNLOCK TABLES;")

        self.cursor.execute("/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;")
        self.cursor.execute("/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;")
        self.cursor.execute("/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;")
        self.cursor.execute("/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;")
        self.cursor.execute("/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;")
        self.cursor.execute("/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;")
        self.cursor.execute("/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;")
        self.cnx.commit()
        self.cnx.close()

createDB()
