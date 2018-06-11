-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 11, 2018 at 12:46 AM
-- Server version: 5.7.22-0ubuntu0.16.04.1
-- PHP Version: 7.0.30-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tangri`
--

-- --------------------------------------------------------

--
-- Table structure for table `users_user`
--

CREATE TABLE `users_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(255) NOT NULL,
  `user_name` varchar(30) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `otp` varchar(300) NOT NULL,
  `otp_expiration` datetime(6),
  `forget_otp` varchar(300) NOT NULL,
  `forget_otp_expiration` datetime(6),
  `address` varchar(300) NOT NULL,
  `intro_text` varchar(300) NOT NULL,
  `phone` varchar(300) NOT NULL,
  `specialization` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users_user`
--

INSERT INTO `users_user` (`id`, `password`, `is_superuser`, `email`, `user_name`, `date_joined`, `last_login`, `avatar`, `is_active`, `is_admin`, `otp`, `otp_expiration`, `forget_otp`, `forget_otp_expiration`, `address`, `intro_text`, `phone`, `specialization`) VALUES
(1, 'pbkdf2_sha256$30000$IaRU4okO8dD7$wU4xzlUSzZ2R01FDS3ibrWbEggYBs703EfIqjc+DdMs=', 1, 'karan@drtangri.com', 'Karan Tangri', '2018-06-06 13:44:46.000000', '2018-06-10 01:27:57.000000', 'avatars/0003_zdvRwpu.jpg', 1, 1, '', NULL, '', NULL, '', '', '9810289955', ''),
(2, 'pbkdf2_sha256$30000$XFUc9OEIa8rM$c6/v6clkqJbAogKUiCGYsxU8UfhKj49VKcbywMWxPlo=', 0, 'charoo@drtangri.com', 'Charoo Tangri', '2018-06-08 23:03:06.000000', NULL, 'avatars/0002.jpg', 1, 1, '', NULL, '', NULL, '', '', '9868525050', ''),
(3, 'pbkdf2_sha256$30000$PRWG17smwR7v$tWDOJ8YNBnIcsn7sQQbJF7RbNNbKDlS3aFZ2gDje5fw=', 0, 'sunil@drtangri.com', 'Sunil Tangri', '2018-06-08 23:03:53.000000', NULL, 'avatars/0001.jpg', 1, 1, '', NULL, '', NULL, '', '', '9810219955', ''),
(4, 'pbkdf2_sha256$30000$vsrmCGFguWzY$T8U5cv7bYGfIYZ2yWVLjrEq8SLJngV0e3qm/ZRvKdr4=', 0, 'sonal@drtangri.com', 'Sonal Tangri', '2018-06-08 23:04:26.000000', NULL, 'avatars/0004.jpg', 1, 1, '', NULL, '', NULL, '', '', '8447985788', ''),
(5, 'pbkdf2_sha256$30000$8V2cJy46W3hT$28WYi6Ye46WkbtwZVDDVNMEdZpWisIMaFXFUBDegfvw=', 0, 'tanya@drtangri.com', 'Tanya Tangri', '2018-06-08 23:05:07.000000', NULL, 'avatars/0005.jpg', 1, 1, '', NULL, '', NULL, '', '', '9810249955', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users_user`
--
ALTER TABLE `users_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users_user`
--
ALTER TABLE `users_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
