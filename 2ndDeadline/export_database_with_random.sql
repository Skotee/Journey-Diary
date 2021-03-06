-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sys
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user`
(
  `ID` int NOT NULL AUTO_INCREMENT,
  `USERNAME` varchar
(15) NOT NULL,
  `PASSWORD` varchar
(15) NOT NULL,
  `EMAIL` varchar
(50) NOT NULL,
  PRIMARY KEY
(`ID`),
  UNIQUE KEY `USERNAME_UNIQUE`
(`USERNAME`),
  UNIQUE KEY `EMAIL_UNIQUE`
(`EMAIL`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `journey`
--

DROP TABLE IF EXISTS `journey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `journey`
(
  `ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `TITLE` varchar
(50) NOT NULL,
  PRIMARY KEY
(`ID`),
  CONSTRAINT `FK_JOURNEY` FOREIGN KEY
(`USER_ID`) REFERENCES `user`
(`ID`) ON
DELETE CASCADE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `day`
--

DROP TABLE IF EXISTS `day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `day`
(
  `ID` int NOT NULL AUTO_INCREMENT,
  `JOURNEY_ID` int NOT NULL,
  `DATE` date NOT NULL,
  `DESCRIPTION` varchar
(10000) DEFAULT NULL,
  PRIMARY KEY
(`ID`),
  CONSTRAINT `FK_DAY` FOREIGN KEY
(`JOURNEY_ID`) REFERENCES `journey`
(`ID`) ON
DELETE CASCADE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image`
(
  `ID` int NOT NULL AUTO_INCREMENT,
  `DAY_ID` int NOT NULL,
  `EXTENSION` varchar
(45) NOT NULL,
  PRIMARY KEY
(`ID`),
  UNIQUE KEY `ID_UNIQUE`
(`ID`),
  CONSTRAINT `FK_IMAGE` FOREIGN KEY
(`DAY_ID`) REFERENCES `day`
(`ID`) ON
DELETE CASCADE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Dumping data
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (NULL,'Roman','user','r@op.pl'),(NULL,'Remi','user','remi@wp.pl');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `journey` WRITE;
/*!40000 ALTER TABLE `journey` DISABLE KEYS */;
INSERT INTO `journey` VALUES (NULL,1,'Egypt'),(NULL,2,'France'),(NULL,1,'Russia'),(NULL,2,'South Africa');
/*!40000 ALTER TABLE `journey` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `day` WRITE;
/*!40000 ALTER TABLE `day` DISABLE KEYS */;
INSERT INTO `day` VALUES (NULL,1,'2019-01-09','I liked my day in Egypt'),(NULL,2,'2019-09-20','Today I saw tour eiffel !'), (NULL,2,'2019-09-25','Chill day in Marseille'),
(NULL,3,'2017-03-10','Discovering Moscow'), (NULL,4,'2015-02-01','Johannesburg is amazing');
/*!40000 ALTER TABLE `day` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (NULL,1,'png'),(NULL,2,'jpg'),(NULL,3,'jpg'),(NULL,2,'png'),(NULL,4,'jpg'),(NULL,6,'jpg');
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-15 20:55:24
