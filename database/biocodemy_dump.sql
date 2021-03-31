-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=armscii8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Introduction'),(2,'DNA'),(3,'Proteins'),(4,'Transcription');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories_challenges`
--

DROP TABLE IF EXISTS `categories_challenges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories_challenges` (
  `categories_id` int NOT NULL,
  `challenges_id` int NOT NULL,
  PRIMARY KEY (`categories_id`,`challenges_id`),
  KEY `fk_Category_has_Challenge_Challenge1_idx` (`challenges_id`),
  KEY `fk_Category_has_Challenge_Category1_idx` (`categories_id`),
  CONSTRAINT `fk_Category_has_Challenge_Category1` FOREIGN KEY (`categories_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `fk_Category_has_Challenge_Challenge1` FOREIGN KEY (`challenges_id`) REFERENCES `challenges` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=armscii8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories_challenges`
--

LOCK TABLES `categories_challenges` WRITE;
/*!40000 ALTER TABLE `categories_challenges` DISABLE KEYS */;
INSERT INTO `categories_challenges` VALUES (1,1),(2,1),(1,2),(3,2),(1,3),(1,4),(2,5),(4,5),(1,6);
/*!40000 ALTER TABLE `categories_challenges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `challenges`
--

DROP TABLE IF EXISTS `challenges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `challenges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `level` int DEFAULT NULL,
  `instructions` longtext,
  `mock_solution` longtext,
  `test_data` longtext,
  `solution` longtext,
  `hint` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=armscii8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `challenges`
--

LOCK TABLES `challenges` WRITE;
/*!40000 ALTER TABLE `challenges` DISABLE KEYS */;
INSERT INTO `challenges` VALUES (1,'Position in sequence',3,'Find the starting position of the GAG trinucleotide in a given sequence. If it appears more than once, provide the latest position.','13','AGCTTTTCATTCTGAGTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC','54','The genome is not 0-based!'),(2,'Protein charge',2,'To simplify the problem, let us consider pH to be neutral. Calculate if a protein has more negatively-charged amino acids than positively-charged amino acids.','False','MSDAAVDTSSEITTKDLKEKKEVVEEAENGRDAPANGNAENEENGEQEADNEVDDGDEDEEAESATGKRAAEDDEDDDVDTKKQKTDEDD','True','The negatively-charged amino acids are the Aspartic acid (D) and Glutamic acid (E), the positive amino acids are Arginine (R), Histidine (H) and Lysine (K).'),(3,'GC content',1,'Calculate percentage of G or C nucleotides in a DNA sequence and provide the answer below with a 5-decimal precision.','0.33333','AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC','0.41428','Use a count function.'),(4,'Dinucleotide count',2,'Calculate the number of occurrences of the dinucleotides AA or TT given a DNA sequence. In the answer, order the dinucleotides alphabetically.','AA 33 TT 27','AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC','AA 8 TT 5','Be aware that trinucleotides such as TTT can be contain 2 dincucleotides TT and TT.'),(5,'Open Reading Frames',5,'Find the length of the longest open reading frame in a given DNA sequence. To be considered an open reading frame, a start codon and a stop codon are needed.','400','CTCAAAAGTCTAGAGCCACCGTCCAGGGAGCAGGTAGCTGCTGGGCTCCGGGGACACTTTGCGTTCGGGCTGGGAGCGTGCTTTCCACGACGGTGACACGCTTCCCTGGATTGGCAGCCAGACTGCCTTCCGGGTCACTGCCATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCAGACCTATGGAAACTACTTCCTGAAAACAACGTTCTGTCCCCCTTGCCGTCCCAAGCAATGGATGATTTGATGCTGTCCCCGGACGATATTGAACAATGGTTCACTGAAGACCCAGGTCCAGATGAAGCTCCCAGAATGCCAGAGGCTGCTCCCCCCGTGGCCCCTGCACCAGCAGCTCCTACACCGGCGGCCCCTGCACCAGCCCCCTCCTGGCCCCTGTCATCTTCTGTCCCTTCCCAGAAAACCTACCAGGGCAGCTACGGTTTCCGTCTGGGCTTCTTGCATTCTGGGACAGCCAAGTCTGTGACTTGCACGTACTCCCCTGCCCTCAACAAGATGTTTTGCCAACTGGCCAAGACCTGCCCTGTGCAGCTGTGGGTTGATTCCACACCCCCGCCCGGCACCCGCGTCCGCGCCATGGCCATCTACAAGCAGTCACAGCACATGACGGAGGTTGTGAGGCGCTGCCCCCACCATGAGCGCTGCTCAGATAGCGATGGTCTGGCCCCTCCTCAGCATCTTATCCGAGTGGAAGGAAATTTGCGTGTGGAGTATTTGGATGACAGAAACACTTTTCGACATAGTGTGGTGGTGCCCTATGAGCCGCCTGAGGTTGGCTCTGACTGTACCACCATCCACTACAACTACATGTGTAACAGTTCCTGCATGGGCGGCATGAACCGGAGGCCCATCCTCACCATCATCACACTGGAAGACTCCAGTGGTAATCTACTGGGACGGAACAGCTTTGAGGTGCGTGTTTGTGCCTGTCCTGGGAGAGACCGGCGCACAGAGGAAGAGAATCTCCGCAAGAAAGGGGAGCCTCACCACGAGCTGCCCCCAGGGAGCACTAAGCGAGCACTGCCCAACAACACCAGCTCCTCTCCCCAGCCAAAGAAGAAACCACTGGATGGAGAATATTTCACCCTTCAGATCCGTGGGCGTGAGCGCTTCGAGATGTTCCGAGAGCTGAATGAGGCCTTGGAACTCAAGGATGCCCAGGCTGGGAAGGAGCCAGGGGGGAGCAGGGCTCACTCCAGCCACCTGAAGTCCAAAAAGGGTCAGTCTACCTCCCGCCATAAAAAACTCATGTTCAAGACAGAAGGGCCTGACTCAGACTGACATTCTCCACTTCTTGTTCCCCACTGACAGCCTCCCACCCCCATCTCTCCCTCCCCTGCCATTTTGGGTTTTGGGTCTTTGAACCCTTGCTTGCAATAGGTGTGCGTCAGAAGCACCCAGGACTTCCATTTGCTTTGTCCCGGGGCTCCACTGAACAAGTTGGCCTGCACTGGTGTTTTGTTGTGGGGAGGAGGATGGGGAGTAGGACATACCAGCTTAGATTTTAAGGTTTTTACTGTGAGGGATGTTTGGGAGATGTAAGAAATGTTCTTGCAGTTAAGGGTTAGTTTACAATCAGCCACATTCTAGGTAGGGGCCCACTTCACCGTACTAACCAGGGAAGCTGTCCCTCACTGTTGAATTTTCTCTAACTTCAAGGCCCATATCTGTGAAATGCTGGCATTTGCACCTACCTCACAGAGTGCATTGTGAGGGTTAATGAAATAATGTACATCTGGCCTTGAAACCACCTTTTATTACATGGGGTCTAGAACTTGACCCCCTTGAGGGTGCTTGTTCCCTCTCCCTGTTGGTCGGTGGGTTGGTAGTTTCTACAGTTGGGCAGCTGGTTAGGTAGAGGGAGTTGTCAAGTCTCTGCTGGCCCAGCCAAACCCTGTCTGACAACCTCTTGGTGAACCTTAGTACCTAAAAGGAAATCTCACCCCATCCCACACCCTGGAGGATTTCATCTCTTGTATATGATGATCTGGATCCACCAAGACTTGTTTTATGCTCAGGGTCAATTTCTTTTTTCTTTTTTTTTTTTTTTTTTCTTTTTCTTTGAGACTGGGTCTCGCTTTGTTGCCCAGGCTGGAGTGGAGTGGCGTGATCTTGGCTTACTGCAGCCTTTGCCTCCCCGGCTCGAGCAGTCCTGCCTCAGCCTCCGGAGTAGCTGGGACCACAGGTTCATGCCACCATGGCCAGCCAACTTTTGCATGTTTTGTAGAGATGGGGTCTCACAGTGTTGCCCAGGCTGGTCTCAAACTCCTGGGCTCAGGCGATCCACCTGTCTCAGCCTCCCAGAGTGCTGGGATTACAATTGTGAGCCACCACGTCCAGCTGGAAGGGTCAACATCTTTTACATTCTGCAAGCACATCTGCATTTTCACCCCACCCTTCCCCTCCTTCTCCCTTTTTATATCCCATTTTTATATCGATCTCTTATTTTACAATAAAACTTTGCTGCCA','2292','Use regular expressions to identify start codons (ATG) and stop codons (TAA, TAG, TGA).\nExplore the nucleotides one by one to find a start codon, afterwards, read 3 nucleotides at a time (a codon).'),(6,'Protein Sequence Summary',4,'Given a protein FASTA file, output the identifier, first 10 aminoacids, last 5 aminoacids and the absolute frequency of the aminoacids found in the protein (aminoacidsnot present in the protein should not be present in the output). Fields must be tab-separated.','Prot1 EFTRPTSTWS  RWSPD E:1,F:1,T:5,R:3,P:2,S:6,W:2,A:3,L:1,M:1,D:1','>PROTX\nRNDAMQEGJLFFPSWWWXVYPSTFFNNJJKJIQRCDNFPSTWQARN','ProtX  RNDAMQEGJL  WQARN R:3,N:5,D:2,A:2,M:1,Q:3,E:1,G:1,J:4,L:1,F:5,P:3,S:3,W:4,X:1,V:1,Y:1,T:2,K:1,I:1,C:1','A dictionary (or similar) can be used to store unique aminoacids, were the aminoacid is the key and the value the count');
/*!40000 ALTER TABLE `challenges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `challenges_stats`
--

DROP TABLE IF EXISTS `challenges_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `challenges_stats` (
  `challenges_id` int NOT NULL,
  `users_id` int NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `tries` int DEFAULT NULL,
  `solved` tinyint(1) DEFAULT NULL,
  `programming_languages_id` int NOT NULL,
  `score` float DEFAULT NULL,
  PRIMARY KEY (`challenges_id`,`users_id`,`programming_languages_id`),
  KEY `fk_Challenge_has_User_User1_idx` (`users_id`),
  KEY `fk_Challenge_has_User_Challenge1_idx` (`challenges_id`),
  KEY `fk_challenges_stats_programming_languages1_idx` (`programming_languages_id`),
  CONSTRAINT `fk_Challenge_has_User_Challenge1` FOREIGN KEY (`challenges_id`) REFERENCES `challenges` (`id`),
  CONSTRAINT `fk_Challenge_has_User_User1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_challenges_stats_programming_languages1` FOREIGN KEY (`programming_languages_id`) REFERENCES `programming_languages` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=armscii8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `challenges_stats`
--

LOCK TABLES `challenges_stats` WRITE;
/*!40000 ALTER TABLE `challenges_stats` DISABLE KEYS */;
INSERT INTO `challenges_stats` VALUES (1,1,'2021-03-31 23:24:03',NULL,0,0,2,NULL),(2,1,'2021-03-31 23:23:51','2021-03-31 23:23:56',1,1,1,7),(3,1,'2021-03-31 23:23:01','2021-03-31 23:23:10',1,1,2,9.33333),(4,1,'2021-03-31 23:23:14','2021-03-31 23:23:33',1,1,3,9.33333);
/*!40000 ALTER TABLE `challenges_stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `languages_challenges`
--

DROP TABLE IF EXISTS `languages_challenges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `languages_challenges` (
  `challenges_id` int NOT NULL,
  `programming_languages_id` int NOT NULL,
  `example_code` longtext,
  PRIMARY KEY (`challenges_id`,`programming_languages_id`),
  KEY `fk_Challenge_has_Programming language_Programming language1_idx` (`programming_languages_id`),
  KEY `fk_Challenge_has_Programming language_Challenge_idx` (`challenges_id`),
  CONSTRAINT `fk_Challenge_has_Programming language_Challenge` FOREIGN KEY (`challenges_id`) REFERENCES `challenges` (`id`),
  CONSTRAINT `fk_Challenge_has_Programming language_Programming language1` FOREIGN KEY (`programming_languages_id`) REFERENCES `programming_languages` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=armscii8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `languages_challenges`
--

LOCK TABLES `languages_challenges` WRITE;
/*!40000 ALTER TABLE `languages_challenges` DISABLE KEYS */;
INSERT INTO `languages_challenges` VALUES (1,1,'example_code'),(1,2,'example_code'),(1,3,'example_code'),(2,1,'example_code'),(2,2,'example_code'),(2,3,'example_code'),(3,1,'example_code'),(3,2,'example_code'),(3,3,'example_code'),(4,1,'example_code'),(4,2,'example_code'),(4,3,'example_code'),(5,1,'example_code'),(5,2,'example_code'),(5,3,'example_code'),(6,1,'example_code'),(6,2,'example_code'),(6,3,'example_code');
/*!40000 ALTER TABLE `languages_challenges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programming_languages`
--

DROP TABLE IF EXISTS `programming_languages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programming_languages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=armscii8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programming_languages`
--

LOCK TABLES `programming_languages` WRITE;
/*!40000 ALTER TABLE `programming_languages` DISABLE KEYS */;
INSERT INTO `programming_languages` VALUES (1,'Python3.8'),(2,'Perl5'),(3,'R4.0.2');
/*!40000 ALTER TABLE `programming_languages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `password` varchar(256) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `age` int DEFAULT NULL,
  `country` varchar(45) DEFAULT NULL,
  `background` varchar(45) DEFAULT NULL,
  `preferred_programming_languages` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_User_Programming language1_idx` (`preferred_programming_languages`),
  CONSTRAINT `fk_User_Programming language1` FOREIGN KEY (`preferred_programming_languages`) REFERENCES `programming_languages` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'test@gmail.com','test','sha256$lwnigDKL$2775a00e29c5dae34f052a5e07abb96d3794f97d3b9dbcf2d445ceecb839584b',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-31 23:27:52
