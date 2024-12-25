-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: raw_materials
-- ------------------------------------------------------
-- Server version	9.1.0

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
-- Table structure for table `batches`
--

DROP TABLE IF EXISTS `batches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `batches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `material_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `batches_ibfk_1` FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `batches`
--

LOCK TABLES `batches` WRITE;
/*!40000 ALTER TABLE `batches` DISABLE KEYS */;
INSERT INTO `batches` VALUES (1,'Сахар 001',2),(2,'Мука 001',1),(3,'Какао 001',3),(4,'Молоко 001',4),(5,'Яичный порошок 001',5),(6,'Мука пшеничная 002',1),(7,'003',1),(8,'Молоко сухое 001',4),(9,'001',1),(10,'002',1),(11,'Мука пшеничная 001',1),(12,'Сахар-песок 001',2),(13,'Сахар-песок 002',2),(14,'Какао-порошок 001',3),(15,'Какао-порошок 003',3),(16,'Молоко сухое 005',4),(17,'Молоко сухое 002',4),(18,'Мука пшеничная 005',1);
/*!40000 ALTER TABLE `batches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materials`
--

DROP TABLE IF EXISTS `materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materials`
--

LOCK TABLES `materials` WRITE;
/*!40000 ALTER TABLE `materials` DISABLE KEYS */;
INSERT INTO `materials` VALUES (1,'Мука пшеничная'),(2,'Сахар-песок'),(3,'Какао-порошок'),(4,'Молоко сухое'),(5,'Яичный порошок');
/*!40000 ALTER TABLE `materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_plans`
--

DROP TABLE IF EXISTS `production_plans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `production_plans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `batch_name` varchar(255) NOT NULL,
  `raw_material` varchar(255) NOT NULL,
  `need_quantity` float NOT NULL,
  `production_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `production_plans_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_plans`
--

LOCK TABLES `production_plans` WRITE;
/*!40000 ALTER TABLE `production_plans` DISABLE KEYS */;
INSERT INTO `production_plans` VALUES (1,1,'Шоколадная партия 1','Какао',200,'2024-12-30'),(2,1,'Шоколадная партия 2','Молоко',150,'2024-12-31'),(3,2,'Конфеты партия 1','Сахар',500,'2024-12-29'),(4,3,'Печенье партия 1','Мука',300,'2024-12-28'),(5,4,'Торт партия 1','Яйца',100,'2024-12-27'),(6,5,'Карамель партия 1','Сироп',250,'2024-12-26'),(7,3,'Печенье партия 2','Мука',250,'2024-12-25'),(8,5,'Карамель партия 2','Сахар',300,'2024-12-24'),(9,4,'Торт партия 4','Мука',125,'2024-12-28');
/*!40000 ALTER TABLE `production_plans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Шоколад'),(2,'Конфеты'),(3,'Печенье'),(4,'Торт'),(5,'Карамель');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchases`
--

DROP TABLE IF EXISTS `purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `supplier_id` int NOT NULL,
  `raw_material_name` varchar(255) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `delivery_date` date NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `report_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `supplier_id` (`supplier_id`),
  CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchases`
--

LOCK TABLES `purchases` WRITE;
/*!40000 ALTER TABLE `purchases` DISABLE KEYS */;
INSERT INTO `purchases` VALUES (1,1,'Сахар',1000.50,'2024-12-30',45.50,'2024-12-25 00:44:21',NULL),(2,2,'Мука',500.00,'2024-12-31',32.00,'2024-12-25 00:44:21',NULL),(13,4,'Орехи грецкие',500.00,'2024-12-28',37.57,'2024-12-25 02:26:13',NULL),(14,2,'Карамель',500.00,'2024-12-11',65.00,'2024-12-25 02:28:04',NULL),(15,5,'Сахар',350.00,'2024-12-12',25.00,'2024-12-25 02:29:15',NULL),(17,5,'Яйца',250.00,'2024-12-29',50.00,'2024-12-25 15:23:25',NULL),(18,4,'Какао-бобы',800.00,'2024-12-28',80.00,'2024-12-25 20:12:58',NULL);
/*!40000 ALTER TABLE `purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quality_tests`
--

DROP TABLE IF EXISTS `quality_tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quality_tests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `batch_id` int NOT NULL,
  `material_id` int NOT NULL,
  `test_type` varchar(255) NOT NULL,
  `test_result` varchar(255) NOT NULL,
  `test_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `batch_id` (`batch_id`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `quality_tests_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quality_tests`
--

LOCK TABLES `quality_tests` WRITE;
/*!40000 ALTER TABLE `quality_tests` DISABLE KEYS */;
INSERT INTO `quality_tests` VALUES (18,11,1,'Клейковина','Норма','2024-12-25'),(19,11,1,'Чистота','Норма','2024-12-25'),(21,6,1,'Влага','Превышение','2024-12-25'),(22,12,2,'Сахароза','Высокая','2024-12-25'),(23,13,2,'Чистота','Норма','2024-12-25'),(24,14,3,'Жирность','Соответствует','2024-12-25'),(25,15,3,'Чистота','Не норма','2024-12-25'),(26,16,4,'Чистота','Норма','2024-12-25'),(27,5,5,'Влага','Превышение','2024-12-25'),(28,17,4,'Влага','Норма','2024-12-25'),(29,18,1,'Клейковина','Норма','2024-12-25');
/*!40000 ALTER TABLE `quality_tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material`
--

DROP TABLE IF EXISTS `raw_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `raw_material` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `shelf_life` int DEFAULT NULL,
  `quantity` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material`
--

LOCK TABLES `raw_material` WRITE;
/*!40000 ALTER TABLE `raw_material` DISABLE KEYS */;
INSERT INTO `raw_material` VALUES (1,'Сахар','Сладкие ингредиенты','кг',365,1900),(2,'Мука','Основные ингредиенты','кг',180,500),(3,'Шоколад','Сладкие ингредиенты','кг',360,200),(4,'Молоко','Жидкости','л',90,300),(5,'Ванилин','Ароматизаторы','г',365,50),(6,'Сахар','Сладкие ингредиенты','кг',365,1790),(7,'Сгущенное молоко','Жидкости','л',365,450),(10,'Какао бобы','Основные ингредиенты','кг',180,1075);
/*!40000 ALTER TABLE `raw_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material_incoming`
--

DROP TABLE IF EXISTS `raw_material_incoming`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `raw_material_incoming` (
  `id` int NOT NULL AUTO_INCREMENT,
  `raw_material_id` int DEFAULT NULL,
  `quantity` decimal(10,2) DEFAULT NULL,
  `supplier` varchar(255) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `raw_material_id` (`raw_material_id`),
  CONSTRAINT `raw_material_incoming_ibfk_1` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_incoming`
--

LOCK TABLES `raw_material_incoming` WRITE;
/*!40000 ALTER TABLE `raw_material_incoming` DISABLE KEYS */;
/*!40000 ALTER TABLE `raw_material_incoming` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material_outgoing`
--

DROP TABLE IF EXISTS `raw_material_outgoing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `raw_material_outgoing` (
  `id` int NOT NULL AUTO_INCREMENT,
  `raw_material_id` int DEFAULT NULL,
  `quantity` decimal(10,2) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `disposal_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `raw_material_id` (`raw_material_id`),
  CONSTRAINT `raw_material_outgoing_ibfk_1` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_outgoing`
--

LOCK TABLES `raw_material_outgoing` WRITE;
/*!40000 ALTER TABLE `raw_material_outgoing` DISABLE KEYS */;
/*!40000 ALTER TABLE `raw_material_outgoing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_types`
--

DROP TABLE IF EXISTS `report_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_name` varchar(255) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_types`
--

LOCK TABLES `report_types` WRITE;
/*!40000 ALTER TABLE `report_types` DISABLE KEYS */;
INSERT INTO `report_types` VALUES (1,'Отчёт по закупкам','Отчёт, который показывает информацию о закупках сырья'),(2,'Отчёт по складу','Отчёт о текущем состоянии склада с сырыми материалами'),(3,'Отчёт по производству','Отчёт о производственном процессе и использованных материалах');
/*!40000 ALTER TABLE `report_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_type_id` int NOT NULL,
  `date` date NOT NULL,
  `material` varchar(255) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_type_id` (`report_type_id`),
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`report_type_id`) REFERENCES `report_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports`
--

LOCK TABLES `reports` WRITE;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
INSERT INTO `reports` VALUES (1,1,'2024-12-01','Сахар',1000.00,'Завершён'),(2,1,'2024-12-02','Мука',500.00,'В процессе'),(3,1,'2024-12-03','Шоколад',300.00,'Ожидает поставки'),(4,1,'2024-12-04','Молоко',1500.00,'Завершён'),(5,1,'2024-12-05','Какао-порошок',200.00,'В процессе'),(6,2,'2024-12-01','Сахар',1200.00,'В наличии'),(7,2,'2024-12-02','Мука',700.00,'В наличии'),(8,2,'2024-12-03','Шоколад',400.00,'Ожидает поставки'),(9,2,'2024-12-04','Молоко',1600.00,'В наличии'),(10,2,'2024-12-05','Какао-порошок',250.00,'В наличии'),(11,3,'2024-12-01','Сахар',500.00,'В процессе'),(12,3,'2024-12-02','Мука',300.00,'Завершён'),(13,3,'2024-12-03','Шоколад',600.00,'Ожидает поставки'),(14,3,'2024-12-04','Молоко',1800.00,'Завершён'),(15,3,'2024-12-05','Какао-порошок',350.00,'В процессе'),(16,1,'2024-12-06','Яйца',1000.00,'Завершён'),(17,1,'2024-12-07','Ваниль',50.00,'Ожидает поставки'),(18,2,'2024-12-06','Сахар',1500.00,'В наличии'),(19,2,'2024-12-07','Мука',800.00,'В наличии'),(20,3,'2024-12-06','Молоко',2000.00,'Завершён'),(21,3,'2024-12-07','Шоколад',700.00,'Ожидает поставки');
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'Поставщик 1','2024-12-25 00:38:38'),(2,'Поставщик 2','2024-12-25 00:38:38'),(4,'Поставщик 3','2024-12-25 02:26:07'),(5,'Поставщик 4','2024-12-25 02:29:15'),(6,'','2024-12-25 15:19:06');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `role` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'админ','Администратор','2024-12-25 15:52:07'),(2,'пользователь1','Просмотр','2024-12-25 15:52:07'),(3,'пользователь2','Редактор','2024-12-25 15:52:07'),(5,'менеджер','Менеджер','2024-12-25 15:52:07'),(6,'модератор','Модератор','2024-12-25 15:52:07'),(7,'гость','Гость','2024-12-25 15:52:07'),(8,'пользователь4','Просмотр','2024-12-25 15:52:07'),(9,'редактор1','Редактор','2024-12-25 15:52:07'),(10,'руководитель','Администратор','2024-12-25 15:52:07');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse`
--

DROP TABLE IF EXISTS `warehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse` (
  `id` int NOT NULL AUTO_INCREMENT,
  `raw_material_name` varchar(255) NOT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `delivery_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse`
--

LOCK TABLES `warehouse` WRITE;
/*!40000 ALTER TABLE `warehouse` DISABLE KEYS */;
/*!40000 ALTER TABLE `warehouse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'raw_materials'
--

--
-- Dumping routines for database 'raw_materials'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-25 23:39:21
