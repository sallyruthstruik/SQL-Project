
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

