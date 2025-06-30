-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 30, 2025 at 12:23 PM
-- Server version: 8.0.31
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smsdjango`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_german2_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(3, 'Student Default Group');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(11, 3, 26),
(13, 3, 28),
(12, 3, 27),
(10, 3, 25);

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_german2_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_german2_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add student', 7, 'add_student'),
(26, 'Can change student', 7, 'change_student'),
(27, 'Can delete student', 7, 'delete_student'),
(28, 'Can view student', 7, 'view_student');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$870000$CROs1ZCD6bd0DyZcRUqzPD$Br+lzp0FhFbmxUemclxbYmLJk5w1fDcP7xwi2ZcH3oM=', '2025-06-30 16:11:08.646511', 1, 'admin', 'Admin', 'User', 'adminuser@gmail.com', 1, 1, '2025-06-24 18:49:29.000000'),
(2, 'pbkdf2_sha256$870000$raqkhQz8I4pcH5kZzZVQ6h$qYPDpT51Lr5PTKUDum20myc7yHJE+fg5mZGm0rlvqH4=', NULL, 0, 'chinmaymishra', 'Chinmay', 'Mishra', 'chinmaymishra0609@gmail.com', 1, 1, '2025-06-30 16:04:54.272298');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(11, 6, 3),
(9, 4, 3),
(10, 5, 3),
(7, 2, 3),
(12, 7, 3),
(13, 3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `auth_user_user_permissions`
--

INSERT INTO `auth_user_user_permissions` (`id`, `user_id`, `permission_id`) VALUES
(8, 1, 28),
(7, 1, 27),
(6, 1, 26),
(5, 1, 25),
(102, 2, 14);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_german2_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_german2_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_german2_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-06-24 20:27:02.022865', '1', 'Can Log', 1, '[{\"added\": {}}]', 3, 1),
(2, '2025-06-24 20:27:18.617370', '2', 'Can Student', 1, '[{\"added\": {}}]', 3, 1),
(3, '2025-06-25 14:12:14.256182', '1', 'Can Log', 3, '', 3, 1),
(4, '2025-06-25 14:12:37.117031', '2', 'Can Student', 2, '[{\"changed\": {\"fields\": [\"Permissions\"]}}]', 3, 1),
(5, '2025-06-25 14:28:10.117600', '2', 'Can Student', 2, '[{\"changed\": {\"fields\": [\"Permissions\"]}}]', 3, 1),
(6, '2025-06-25 14:28:38.021802', '2', 'Can Student', 3, '', 3, 1),
(7, '2025-06-25 18:10:59.547706', '3', 'Student Default Group', 1, '[{\"added\": {}}]', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_german2_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_german2_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'student', 'student');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_german2_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_german2_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-06-24 16:11:35.525237'),
(2, 'auth', '0001_initial', '2025-06-24 16:11:36.160133'),
(3, 'admin', '0001_initial', '2025-06-24 16:11:36.395012'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-06-24 16:11:36.401863'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-24 16:11:36.408793'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-06-24 16:11:36.488774'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-06-24 16:11:36.525885'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-06-24 16:11:36.571116'),
(9, 'auth', '0004_alter_user_username_opts', '2025-06-24 16:11:36.579078'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-06-24 16:11:36.620064'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-06-24 16:11:36.621507'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-06-24 16:11:36.627591'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-06-24 16:11:36.671136'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-06-24 16:11:36.707946'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-06-24 16:11:36.754198'),
(16, 'auth', '0011_update_proxy_permissions', '2025-06-24 16:11:36.760735'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-06-24 16:11:36.806564'),
(18, 'sessions', '0001_initial', '2025-06-24 16:11:36.852081'),
(19, 'student', '0001_initial', '2025-06-24 16:11:36.872469');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_german2_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_german2_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1npgrkqssmiqwr1a4rg07px6046y6wu1', '.eJxVjDsOwyAQRO9CHSG-C06Z3mdAu4CDkwgkY1dR7h5bcpF0o3lv5s0CbmsJW89LmBO7MsUuvx1hfOZ6gPTAem88trouM_FD4SftfGwpv26n-3dQsJd97a0xpNSAABKsT1qCIIkJRQa0e5wEOZWltl57F2GgPKGS5IiMAu_Y5wu_nzcy:1uUM37:D8Cz8j4EDYYXsx8cZoA6D29CGstMhbDS3PQ-X52pgSw', '2025-07-09 14:34:09.757008'),
('pvbwhm0ptcrjygqgsqords939cxwzz1l', '.eJxVjDsOwyAQRO9CHSHzWcAp0_sMaGEhOIlAMnYV5e6xJRdJN5r3Zt7M47YWv_W0-JnYlUl2-e0CxmeqB6AH1nvjsdV1mQM_FH7SzqdG6XU73b-Dgr3saxcFQghRS5MECAtaUQbtgkQasjUSnBu0I9QiKqespVFHJcOe8ohg2OcL0UA3HA:1uUSGi:UDMfCUvr-c1wpaNSfqFsw-yqppCRw9q_MpaAn_m31pc', '2025-07-09 21:12:36.510170'),
('u0ckflxm2pyh3908u827ltw5i82e0ug5', '.eJxVjDsOwyAQRO9CHSHzWcAp0_sMaGEhOIlAMnYV5e6xJRdJN5r3Zt7M47YWv_W0-JnYlSl2-e0CxmeqB6AH1nvjsdV1mQM_FH7SzqdG6XU73b-Dgr3saxcFQghRS5MECAtaUQbtgkQasjUSnBu0I9QiKqespVFHJcOe8ohg2OcL0dk3HQ:1uUmv4:6mBVyit1u6x1eP7WNfr4bz8CRiXugIcpc5mNILyKYQc', '2025-07-10 19:15:38.379910'),
('meg7r3mp75xzkknwad5078a1csg4scg9', '.eJxVjDsOwyAQRO9CHSHzWcAp0_sMaGEhOIlAMnYV5e6xJRdJN5r3Zt7M47YWv_W0-JnYlSl2-e0CxmeqB6AH1nvjsdV1mQM_FH7SzqdG6XU73b-Dgr3saxcFQghRS5MECAtaUQbtgkQasjUSnBu0I9QiKqespVFHJcOe8ohg2OcL0dk3HQ:1uV5M8:Q3Ah1m_SpQznu76Junucs8CQEvv_cjC-Vzkgnty8zSk', '2025-07-11 14:56:48.365228');

-- --------------------------------------------------------

--
-- Table structure for table `student_student`
--

DROP TABLE IF EXISTS `student_student`;
CREATE TABLE IF NOT EXISTS `student_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `student_first_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_middle_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_last_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_father_first_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_father_middle_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_father_last_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_mother_first_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_mother_middle_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_mother_last_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_email` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_phone_number` varchar(15) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_birth_date` date DEFAULT NULL,
  `student_gender` varchar(15) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_id` varchar(10) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_entry_year` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_semester` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_address_line_1` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_address_line_2` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_city` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_state` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_country` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_zip` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `student_image` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `guardian_address_line_1` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `guardian_address_line_2` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `guardian_city` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `guardian_state` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `guardian_country` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `guardian_zip` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `first_emergency_first_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `first_emergency_middle_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `first_emergency_last_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `first_emergency_phone_number` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `first_emergency_relationship` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `second_emergency_first_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `second_emergency_middle_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `second_emergency_last_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `second_emergency_phone_number` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `second_emergency_relationship` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `physician_first_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `physician_middle_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `physician_last_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `physician_primary_phone_number` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `physician_secondary_phone_number` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `preferred_hospital_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `physician_special_notes` longtext COLLATE utf8mb4_german2_ci,
  `previous_school_name` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `previous_school_city` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `previous_school_state` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `previous_school_country` varchar(100) COLLATE utf8mb4_german2_ci DEFAULT NULL,
  `previous_school_date_started` date DEFAULT NULL,
  `previous_school_date_ended` date DEFAULT NULL,
  `previous_school_notes` longtext COLLATE utf8mb4_german2_ci,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `student_student`
--

INSERT INTO `student_student` (`id`, `student_first_name`, `student_middle_name`, `student_last_name`, `student_father_first_name`, `student_father_middle_name`, `student_father_last_name`, `student_mother_first_name`, `student_mother_middle_name`, `student_mother_last_name`, `student_email`, `student_phone_number`, `student_birth_date`, `student_gender`, `student_id`, `student_entry_year`, `student_semester`, `student_address_line_1`, `student_address_line_2`, `student_city`, `student_state`, `student_country`, `student_zip`, `student_image`, `guardian_address_line_1`, `guardian_address_line_2`, `guardian_city`, `guardian_state`, `guardian_country`, `guardian_zip`, `first_emergency_first_name`, `first_emergency_middle_name`, `first_emergency_last_name`, `first_emergency_phone_number`, `first_emergency_relationship`, `second_emergency_first_name`, `second_emergency_middle_name`, `second_emergency_last_name`, `second_emergency_phone_number`, `second_emergency_relationship`, `physician_first_name`, `physician_middle_name`, `physician_last_name`, `physician_primary_phone_number`, `physician_secondary_phone_number`, `preferred_hospital_name`, `physician_special_notes`, `previous_school_name`, `previous_school_city`, `previous_school_state`, `previous_school_country`, `previous_school_date_started`, `previous_school_date_ended`, `previous_school_notes`) VALUES
(1, 'Chinmay', '', 'Mishra', 'Ram', 'Surat', 'Mishra', 'Sushila', 'Devi', 'Mishra', 'chinmaymishra0609@gmail.com', '8690736210', '1995-11-06', 'male', 'CM0609', '2013', 'first', 'BEDAL ROAD', 'BEHIND OLD ST WORK SHOP', 'FALNA', 'RAJASTHAN', 'India', '306116', 'student/images/student_58fc54cc3b8f4884b73614b55729e89d.jpeg', 'BEDAL ROAD', 'BEHIND OLD ST WORK SHOP', 'FALNA', 'RAJASTHAN', 'India', '306116', 'KULDEEP', 'CHAND', 'MISHRA', '9799455505', 'ELDER BROTHER', 'MOHIT', 'KUMAR', 'MISHRA', '6376983909', 'ELDER BROTHER', 'VIJAY', 'KUMAR', 'SHARMA', '01234567890', '08690736210', 'VYAS HOSPITAL FALNA', 'VOMITING ISSUE', 'SPU PG COLLEGE', 'FALNA', 'RAJASTHAN', 'India', '2013-07-01', '2019-05-28', 'GOOD'),
(2, 'Mohit', 'Kumar', 'Mishra', 'Ram', 'Surat', 'Mishra', 'Sushila', 'Devi', 'Mishra', 'mohitmishra.falna850@gmail.com', '6376983909', '1994-05-18', 'male', 'MM1805', '2013', 'first', 'BEDAL ROAD', 'BEHIND OLD ST WORK SHOP', 'FALNA', 'RAJASTHAN', 'India', '306116', 'student/images/student_816a7d665fe44a3e89fd701da565c072.jpg', 'BEDAL ROAD', 'BEHIND OLD ST WORK SHOP', 'FALNA', 'RAJASTHAN', 'India', '306116', 'KULDEEP', 'CHAND', 'MISHRA', '9799455505', 'ELDER BROTHER', 'NAMITA', '', 'MISHRA', '9672374459', 'ELDER BROTHER IN LAW', 'VIJAY', 'KUMAR', 'SHARMA', '1234567890', '1234567809', 'VYAS HOSPITAL FALNA', 'VOMITING ISSUE', 'SPU PG COLLEGE', 'FALNA', 'RAJASTHAN', 'India', '2013-07-01', '2019-05-28', 'GOOD');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
