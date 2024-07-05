-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: taobao
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `goodslist`
--

DROP TABLE IF EXISTS `goodslist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goodslist` (
  `goods_ID` int NOT NULL AUTO_INCREMENT,
  `goods_name` varchar(255) NOT NULL,
  `goods_price` decimal(10,2) NOT NULL,
  `goods_number` int NOT NULL,
  `goods_weight` decimal(10,2) NOT NULL,
  `goods_status` tinyint NOT NULL,
  `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `hot_number` int NOT NULL,
  `is_hot` tinyint(1) NOT NULL,
  PRIMARY KEY (`goods_ID`),
  CONSTRAINT `goodslist_chk_1` CHECK ((`goods_status` in (0,1,2)))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goodslist`
--

LOCK TABLES `goodslist` WRITE;
/*!40000 ALTER TABLE `goodslist` DISABLE KEYS */;
INSERT INTO `goodslist` VALUES (1,'商品A',99.99,100,1.50,1,'2024-05-26 02:53:42','2024-05-26 02:53:42',10,1),(2,'商品B',199.99,50,2.25,0,'2024-05-26 02:53:42','2024-05-26 02:53:42',5,0),(3,'商品C',299.99,20,0.75,2,'2024-05-26 02:53:42','2024-05-26 02:53:42',2,1);
/*!40000 ALTER TABLE `goodslist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person` (
  `username` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES ('ccc','123@qq.com','1358749'),('hhhh','999@qq.com','123456'),('HHHHqqqq','288@qq.com','123456'),('te','21@qq.com','2134'),('te0000','1222@qq.com','123'),('test','2933@qq.com','123456'),('test02','2933724627@qq.com','123456'),('test03','29337@qq.com','123456'),('test06','2933987@qq.com','123456'),('test100','3655@qq.com','123456'),('test1111','140286@qq.com','123456'),('test99','140285@qq.com','123456'),('yep','12399999999999@qq.com','123456');
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `register`
--

DROP TABLE IF EXISTS `register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `register` (
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `register`
--

LOCK TABLES `register` WRITE;
/*!40000 ALTER TABLE `register` DISABLE KEYS */;
INSERT INTO `register` VALUES ('test','123456','13825600730');
/*!40000 ALTER TABLE `register` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rolelist`
--

DROP TABLE IF EXISTS `rolelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rolelist` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `RoleName` varchar(255) NOT NULL,
  `RoleDescription` text,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rolelist`
--

LOCK TABLES `rolelist` WRITE;
/*!40000 ALTER TABLE `rolelist` DISABLE KEYS */;
INSERT INTO `rolelist` VALUES (4,'财务管理员','负责管理和审计商店的财务活动'),(5,'库存管理员','负责监控和更新库存信息'),(6,'订单处理员','处理客户订单和退货'),(7,'客服代表','提供客户支持和解决问题'),(8,'市场营销专员','负责商店的市场推广和广告活动'),(9,'产品经理','负责产品规划和定价策略'),(10,'技术支持','解决技术问题和维护系统稳定运行'),(11,'test','123456'),(12,'test02','123456789'),(13,'test03','123456789'),(14,'test05','123456789'),(19,'test','test'),(20,'员工','1111111');
/*!40000 ALTER TABLE `rolelist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `roles` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  CONSTRAINT `CK_status` CHECK (((`status` = _utf8mb4'true') or (`status` = _utf8mb4'false')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('h','1234567890@qq.com','13134411117','用户','false'),('test','11@qq.com','18512351628','用户','false'),('test','222@qq.com','15685244589','用户','true'),('sinzeng','1544875982@qq.com','13854866582','用户','true');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-05 17:02:26
