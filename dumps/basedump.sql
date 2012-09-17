
-- MySQL dump 10.13  Distrib 5.5.24, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Files
-- ------------------------------------------------------
-- Server version	5.5.24-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


create database Files character set utf8;
use Files;
set names utf8;

DROP TABLE IF EXISTS `File`;
CREATE TABLE `File` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `directory_path` varchar(1000) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `pathlen` int(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Versions`;
CREATE TABLE `Versions` (
  `id` int(5) NOT NULL,
  `date` datetime DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `FileVersion`;
CREATE TABLE `FileVersion` (
  `id` bigint(20) NOT NULL,
  `file_id` bigint(20)  NOT NULL ,
  `version_number` int(5) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY(`file_id`) REFERENCES `File`(id) ON DELETE CASCADE,
  FOREIGN KEY(`version_number`) REFERENCES `Versions`(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `FileVersionAttr`;
CREATE TABLE `FileVersionAttr` (
  `vers_id` bigint(20) NOT NULL,
  `modification_time` datetime DEFAULT NULL,
  `last_modified_time` datetime DEFAULT NULL,
  `size` bigint(100) DEFAULT NULL,
  `is_hidden` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`vers_id`),
  FOREIGN KEY (`vers_id`) REFERENCES `FileVersion`(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `KeyValue`;
CREATE TABLE `KeyValue` (
  `key` varchar(100) NOT NULL,
  `value` mediumtext,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `KeyValue` VALUES ('max_fv_id','3175726'),('max_f_id','4494855'),('max_v_id','323');

-- MySQL dump 10.13  Distrib 5.5.24, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: Files
-- ------------------------------------------------------
-- Server version	5.5.24-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `File`
--

DROP TABLE IF EXISTS `File`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `File` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `directory_path` varchar(1000) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `pathlen` int(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `File`
--

LOCK TABLES `File` WRITE;
/*!40000 ALTER TABLE `File` DISABLE KEYS */;
/*!40000 ALTER TABLE `File` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FileVersion`
--

DROP TABLE IF EXISTS `FileVersion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FileVersion` (
  `id` bigint(20) NOT NULL,
  `file_id` bigint(20) NOT NULL,
  `version_number` int(5) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `file_id` (`file_id`),
  KEY `version_number` (`version_number`),
  CONSTRAINT `FileVersion_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `File` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FileVersion_ibfk_2` FOREIGN KEY (`version_number`) REFERENCES `Versions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FileVersion`
--

LOCK TABLES `FileVersion` WRITE;
/*!40000 ALTER TABLE `FileVersion` DISABLE KEYS */;
/*!40000 ALTER TABLE `FileVersion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FileVersionAttr`
--

DROP TABLE IF EXISTS `FileVersionAttr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FileVersionAttr` (
  `vers_id` bigint(20) NOT NULL,
  `modification_time` datetime DEFAULT NULL,
  `last_modified_time` datetime DEFAULT NULL,
  `size` bigint(100) DEFAULT NULL,
  `is_hidden` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`vers_id`),
  CONSTRAINT `FileVersionAttr_ibfk_1` FOREIGN KEY (`vers_id`) REFERENCES `FileVersion` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FileVersionAttr`
--

LOCK TABLES `FileVersionAttr` WRITE;
/*!40000 ALTER TABLE `FileVersionAttr` DISABLE KEYS */;
/*!40000 ALTER TABLE `FileVersionAttr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `KeyValue`
--

DROP TABLE IF EXISTS `KeyValue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `KeyValue` (
  `key` varchar(100) NOT NULL,
  `value` mediumtext,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `KeyValue`
--

LOCK TABLES `KeyValue` WRITE;
/*!40000 ALTER TABLE `KeyValue` DISABLE KEYS */;
INSERT INTO `KeyValue` VALUES ('max_fv_id','11'),('max_f_id','75413'),('max_v_id','0');
/*!40000 ALTER TABLE `KeyValue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Versions`
--

DROP TABLE IF EXISTS `Versions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Versions` (
  `id` int(5) NOT NULL,
  `date` datetime DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Versions`
--

LOCK TABLES `Versions` WRITE;
/*!40000 ALTER TABLE `Versions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Versions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-09-18  2:36:51
