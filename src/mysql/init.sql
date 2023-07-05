CREATE DATABASE challenge;
USE challenge;

-- Creamos tabla
CREATE TABLE `users` (
  `id` int NOT NULL,
  `first_name` varchar(50) NOT NULL DEFAULT '',
  `last_name` varchar(50) NOT NULL DEFAULT '',
  `email` varchar(80) NOT NULL DEFAULT '',
  `gender` varchar(40) NOT NULL DEFAULT '',
  `ip_address` varchar(40) NOT NULL DEFAULT '',
  `uploaded_date` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_email` (`email`)
  );

-- Insertamos una data pequeña
INSERT INTO challenge.users (id, first_name, last_name, email, gender, ip_address) VALUES
(1, 'Mag', 'Gothard', 'mgothard0@umich.edu', 'queer', '244.202.57.31'), 
(2, 'Netti', 'Gonnelly', 'ngonnelly1@bbc.co.uk', 'Female', '251.246.248.160'), 
(3, 'Abagail', 'Hitscher', 'ahitscher2@hp.com', 'Female', '22.26.240.152'), 
(4, 'Gerek', 'Burgwin', 'gburgwin3@mysql.com', 'Male', '164.157.41.163'), 
(5, 'Ollie', 'Mackelworth', 'omackelworth4@hubpages.com', 'Male', '217.5.234.128');

