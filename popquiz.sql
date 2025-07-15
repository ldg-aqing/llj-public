/*
 Navicat Premium Dump SQL

 Source Server         : pop
 Source Server Type    : MySQL
 Source Server Version : 80036 (8.0.36)
 Source Host           : 150.158.10.177:3306
 Source Schema         : popquiz

 Target Server Type    : MySQL
 Target Server Version : 80036 (8.0.36)
 File Encoding         : 65001

 Date: 14/07/2025 20:37:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add uploaded material', 7, 'add_uploadedmaterial');
INSERT INTO `auth_permission` VALUES (26, 'Can change uploaded material', 7, 'change_uploadedmaterial');
INSERT INTO `auth_permission` VALUES (27, 'Can delete uploaded material', 7, 'delete_uploadedmaterial');
INSERT INTO `auth_permission` VALUES (28, 'Can view uploaded material', 7, 'view_uploadedmaterial');
INSERT INTO `auth_permission` VALUES (29, 'Can add users', 8, 'add_users');
INSERT INTO `auth_permission` VALUES (30, 'Can change users', 8, 'change_users');
INSERT INTO `auth_permission` VALUES (31, 'Can delete users', 8, 'delete_users');
INSERT INTO `auth_permission` VALUES (32, 'Can view users', 8, 'view_users');
INSERT INTO `auth_permission` VALUES (33, 'Can add quiz', 9, 'add_quiz');
INSERT INTO `auth_permission` VALUES (34, 'Can change quiz', 9, 'change_quiz');
INSERT INTO `auth_permission` VALUES (35, 'Can delete quiz', 9, 'delete_quiz');
INSERT INTO `auth_permission` VALUES (36, 'Can view quiz', 9, 'view_quiz');
INSERT INTO `auth_permission` VALUES (37, 'Can add presentation attendee', 10, 'add_presentationattendee');
INSERT INTO `auth_permission` VALUES (38, 'Can change presentation attendee', 10, 'change_presentationattendee');
INSERT INTO `auth_permission` VALUES (39, 'Can delete presentation attendee', 10, 'delete_presentationattendee');
INSERT INTO `auth_permission` VALUES (40, 'Can view presentation attendee', 10, 'view_presentationattendee');
INSERT INTO `auth_permission` VALUES (41, 'Can add quiz answer', 11, 'add_quizanswer');
INSERT INTO `auth_permission` VALUES (42, 'Can change quiz answer', 11, 'change_quizanswer');
INSERT INTO `auth_permission` VALUES (43, 'Can delete quiz answer', 11, 'delete_quizanswer');
INSERT INTO `auth_permission` VALUES (44, 'Can view quiz answer', 11, 'view_quizanswer');
INSERT INTO `auth_permission` VALUES (45, 'Can add presentation', 12, 'add_presentation');
INSERT INTO `auth_permission` VALUES (46, 'Can change presentation', 12, 'change_presentation');
INSERT INTO `auth_permission` VALUES (47, 'Can delete presentation', 12, 'delete_presentation');
INSERT INTO `auth_permission` VALUES (48, 'Can view presentation', 12, 'view_presentation');
INSERT INTO `auth_permission` VALUES (49, 'Can add discussion message', 13, 'add_discussionmessage');
INSERT INTO `auth_permission` VALUES (50, 'Can change discussion message', 13, 'change_discussionmessage');
INSERT INTO `auth_permission` VALUES (51, 'Can delete discussion message', 13, 'delete_discussionmessage');
INSERT INTO `auth_permission` VALUES (52, 'Can view discussion message', 13, 'view_discussionmessage');
INSERT INTO `auth_permission` VALUES (53, 'Can add feedback', 14, 'add_feedback');
INSERT INTO `auth_permission` VALUES (54, 'Can change feedback', 14, 'change_feedback');
INSERT INTO `auth_permission` VALUES (55, 'Can delete feedback', 14, 'delete_feedback');
INSERT INTO `auth_permission` VALUES (56, 'Can view feedback', 14, 'view_feedback');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$1000000$ZtwSXe21NaoDVEjttBApvz$AFWVzmueU5dBdmunHSF6L5BleVS1TZVUJNx+ydK0dNU=', '2025-07-14 08:07:53.334448', 1, '14104', '', '', '1410446243@qq.com', 1, 1, '2025-07-14 08:07:48.802892');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for comment_discussionmessage
-- ----------------------------
DROP TABLE IF EXISTS `comment_discussionmessage`;
CREATE TABLE `comment_discussionmessage`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `presentation_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `comment_discussionme_presentation_id_20c0a49a_fk_show_pres`(`presentation_id` ASC) USING BTREE,
  INDEX `comment_discussionmessage_user_id_2a106485_fk_users_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `comment_discussionme_presentation_id_20c0a49a_fk_show_pres` FOREIGN KEY (`presentation_id`) REFERENCES `show_presentation` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comment_discussionmessage_user_id_2a106485_fk_users_users_id` FOREIGN KEY (`user_id`) REFERENCES `users_users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comment_discussionmessage
-- ----------------------------

-- ----------------------------
-- Table structure for comment_feedback
-- ----------------------------
DROP TABLE IF EXISTS `comment_feedback`;
CREATE TABLE `comment_feedback`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `feedback_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `presentation_id` bigint NOT NULL,
  `related_quiz_id` bigint NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `comment_feedback_presentation_id_504068cd_fk_show_pres`(`presentation_id` ASC) USING BTREE,
  INDEX `comment_feedback_related_quiz_id_a30aab62_fk_quiz_quiz_id`(`related_quiz_id` ASC) USING BTREE,
  INDEX `comment_feedback_user_id_7d57d474_fk_users_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `comment_feedback_presentation_id_504068cd_fk_show_pres` FOREIGN KEY (`presentation_id`) REFERENCES `show_presentation` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comment_feedback_related_quiz_id_a30aab62_fk_quiz_quiz_id` FOREIGN KEY (`related_quiz_id`) REFERENCES `quiz_quiz` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comment_feedback_user_id_7d57d474_fk_users_users_id` FOREIGN KEY (`user_id`) REFERENCES `users_users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comment_feedback
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (13, 'comment', 'discussionmessage');
INSERT INTO `django_content_type` VALUES (14, 'comment', 'feedback');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (10, 'manager', 'presentationattendee');
INSERT INTO `django_content_type` VALUES (7, 'material', 'uploadedmaterial');
INSERT INTO `django_content_type` VALUES (9, 'quiz', 'quiz');
INSERT INTO `django_content_type` VALUES (11, 'record', 'quizanswer');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (12, 'show', 'presentation');
INSERT INTO `django_content_type` VALUES (8, 'users', 'users');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-07-14 08:05:53.485199');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2025-07-14 08:05:54.573672');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2025-07-14 08:05:54.829830');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2025-07-14 08:05:54.849614');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-14 08:05:54.869770');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2025-07-14 08:05:55.026036');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2025-07-14 08:05:55.109129');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2025-07-14 08:05:55.164031');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2025-07-14 08:05:55.185064');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2025-07-14 08:05:55.269864');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2025-07-14 08:05:55.286627');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2025-07-14 08:05:55.307621');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2025-07-14 08:05:55.416216');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2025-07-14 08:05:55.510011');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2025-07-14 08:05:55.561137');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2025-07-14 08:05:55.622722');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2025-07-14 08:05:55.721916');
INSERT INTO `django_migrations` VALUES (18, 'users', '0001_initial', '2025-07-14 08:05:55.786146');
INSERT INTO `django_migrations` VALUES (19, 'show', '0001_initial', '2025-07-14 08:05:56.033048');
INSERT INTO `django_migrations` VALUES (20, 'quiz', '0001_initial', '2025-07-14 08:05:56.175100');
INSERT INTO `django_migrations` VALUES (21, 'comment', '0001_initial', '2025-07-14 08:05:56.742485');
INSERT INTO `django_migrations` VALUES (22, 'manager', '0001_initial', '2025-07-14 08:05:57.004551');
INSERT INTO `django_migrations` VALUES (23, 'material', '0001_initial', '2025-07-14 08:05:57.079288');
INSERT INTO `django_migrations` VALUES (24, 'material', '0002_alter_uploadedmaterial_title', '2025-07-14 08:05:57.123293');
INSERT INTO `django_migrations` VALUES (25, 'material', '0003_uploadedmaterial_extracted_text', '2025-07-14 08:05:57.174192');
INSERT INTO `django_migrations` VALUES (26, 'material', '0004_userinfo', '2025-07-14 08:05:57.251007');
INSERT INTO `django_migrations` VALUES (27, 'material', '0005_delete_userinfo', '2025-07-14 08:05:57.291971');
INSERT INTO `django_migrations` VALUES (28, 'record', '0001_initial', '2025-07-14 08:05:57.538226');
INSERT INTO `django_migrations` VALUES (29, 'sessions', '0001_initial', '2025-07-14 08:05:57.655392');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('afwao19gyi310hn0nqfn8h7qph85e9mr', 'eyJ1c2VyX2lkIjoxLCJ1c2VyX3JvbGUiOiJPUkdBTklaRVIifQ:1ubFBS:wgd9_ebxojXTpTMCqhKidZ6gxOFfSpr-HAmanm2ogVg', '2025-07-28 09:09:14.523495');
INSERT INTO `django_session` VALUES ('h0ji0kvhkaseam9upef2bnqb6v47musf', 'eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFxaW5nIiwicm9sZSI6Ik9SR0FOSVpFUiJ9:1ubIJu:CvX4m9B9DJqNnqFYGII1SfkDu9ifUW12BV-VPSbUKzk', '2025-07-28 12:30:10.868616');
INSERT INTO `django_session` VALUES ('q0tpjb1gyl6i36khshgh2n31sq9nvt2s', 'eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImptYyIsInJvbGUiOiJPUkdBTklaRVIifQ:1ubHfB:nh4IZL-EZD5NrN1kgIqyig29PQxHan8HIglG726k4l4', '2025-07-28 11:48:05.004668');
INSERT INTO `django_session` VALUES ('uwx0fd6pw9uu3cyhyxhh25mtm2vqp5ng', '.eJxVjksLwjAQhP9LzhLapMmm3hREPKjQo5eSx8ZWawJ9nMT_boNF9DY73-wwT1LraWzqacC-bh1Zk5ysfj2j7R1DAu6mwzVSG8PYt4amCF3oQI_RYbddsn8FjR6a-btUKDIsUeYguVOZAMdLK0F4sMpYK4BZbY1TWHg0UnpgkuXaA4LnYNhc-t1YfHTQD0yDGZ9hH7t0nKv95nS47CryegPT1kZY:1ubHmU:hP32_uXBNPfYFLOpZ6Kv9lNUyS3j9dZCjoDV7d13I6E', '2025-07-28 11:55:38.802262');

-- ----------------------------
-- Table structure for manager_presentationattendee
-- ----------------------------
DROP TABLE IF EXISTS `manager_presentationattendee`;
CREATE TABLE `manager_presentationattendee`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `joined_at` datetime(6) NOT NULL,
  `attendee_id` bigint NOT NULL,
  `presentation_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `manager_presentationatte_presentation_id_attendee_033df8db_uniq`(`presentation_id` ASC, `attendee_id` ASC) USING BTREE,
  INDEX `manager_presentation_attendee_id_dffb1e91_fk_users_use`(`attendee_id` ASC) USING BTREE,
  CONSTRAINT `manager_presentation_attendee_id_dffb1e91_fk_users_use` FOREIGN KEY (`attendee_id`) REFERENCES `users_users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `manager_presentation_presentation_id_671e1145_fk_show_pres` FOREIGN KEY (`presentation_id`) REFERENCES `show_presentation` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of manager_presentationattendee
-- ----------------------------

-- ----------------------------
-- Table structure for material_uploadedmaterial
-- ----------------------------
DROP TABLE IF EXISTS `material_uploadedmaterial`;
CREATE TABLE `material_uploadedmaterial`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `file` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `file_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `upload_time` datetime(6) NOT NULL,
  `extracted_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of material_uploadedmaterial
-- ----------------------------
INSERT INTO `material_uploadedmaterial` VALUES (1, 'aq', 'materials/922106840429罗东果_5XON1nd.pdf', 'pdf', '2025-07-14 08:26:21.979590', '个人简历\n一、基本信息\n姓名：罗东果\n性别：男\n联系电话：15211832257\n邮箱：2389893881@qq.com\n求职意向：软件开发工程师\n二、教育背景\n南京理工大学— 软件工程本科\n核心课程：数据结构与算法、编译原理、操作系统、计算机网络、数据库基础\n三、专业技能\n编程语言：精通C/C++、Python，熟悉Java、SQL\n开发框架：PyTorch、Flask、Vue、MyBatis、Spring Boot\n数据库：熟练使用MySQL、SQLite，了解Redis、MongoDB\n工具平台：Git、Linux、Docker、VS Code、IDEA\n算法能力：熟悉动态规划、搜索、图论等算法\n四、项目经历\n1. 帝国时代人机对抗（C++）\n2023.07 – 2023.10\n使用qt 编写的人机对抗，要求在固定时间内完成任务；课程评比中排名第三\n2.校园二手交易系统\n2024.06 – 2023.07\n实现校园二手交易系统，使用IDEA 编程，实现界面美化，交互流畅\n3. 健康管理系统（Java + SQLite）\n2024.09 – 2024.12\n实现用户健康信息管理系统，记录每日步数、热量摄入与睡眠质量；使用MPAndroidChart 可\n视化健康趋势图表；课程评比中排名前5\n4. 基于C++的词法分析器和LR(1)语法分析器\n2025.02 – 2025.04\n支持上下文无关文法的语法分析器，构造Action / Goto 表，支持分析错误定位与解释；处理\n移进-归约冲突，构建项目集族与闭包\n技术栈：C++ + NFA/DFA 自动机构建+ FIRST/ FOLLOW 集+ LR(1)表生成\n功能点：从文法文件中解析产生式，构造闭包与项目集族，自动构建Action / Goto\n表，支持分析错误定位与解释\n技术难点：处理移进-归约冲突，通过优先级规则优化决策\n五、自我评价\n扎实的专业基础，能迅速上手新语言/框架\n动手能力强，具备完整项目开发与调试经验\n重视团队协作与代码规范，具备良好沟通能力\n热爱技术，乐于钻研前沿技术与开源项目\n有较强的学习能力和自我驱动能力，能胜任高强度实习或入职工作');

-- ----------------------------
-- Table structure for quiz_quiz
-- ----------------------------
DROP TABLE IF EXISTS `quiz_quiz`;
CREATE TABLE `quiz_quiz`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `options` json NOT NULL,
  `correct_answer` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `explanation` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `time_limit` int UNSIGNED NOT NULL,
  `presentation_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `quiz_quiz_presentation_id_7f237608_fk_show_presentation_id`(`presentation_id` ASC) USING BTREE,
  CONSTRAINT `quiz_quiz_presentation_id_7f237608_fk_show_presentation_id` FOREIGN KEY (`presentation_id`) REFERENCES `show_presentation` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `quiz_quiz_chk_1` CHECK (`time_limit` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of quiz_quiz
-- ----------------------------

-- ----------------------------
-- Table structure for record_quizanswer
-- ----------------------------
DROP TABLE IF EXISTS `record_quizanswer`;
CREATE TABLE `record_quizanswer`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `selected_answer` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `answered_at` datetime(6) NOT NULL,
  `answer_time` int UNSIGNED NOT NULL,
  `quality_rating` smallint UNSIGNED NULL DEFAULT NULL,
  `quiz_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `record_quizanswer_quiz_id_41bb088b_fk_quiz_quiz_id`(`quiz_id` ASC) USING BTREE,
  INDEX `record_quizanswer_user_id_89824726_fk_users_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `record_quizanswer_quiz_id_41bb088b_fk_quiz_quiz_id` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_quiz` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `record_quizanswer_user_id_89824726_fk_users_users_id` FOREIGN KEY (`user_id`) REFERENCES `users_users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `record_quizanswer_chk_1` CHECK (`answer_time` >= 0),
  CONSTRAINT `record_quizanswer_chk_2` CHECK (`quality_rating` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of record_quizanswer
-- ----------------------------

-- ----------------------------
-- Table structure for show_presentation
-- ----------------------------
DROP TABLE IF EXISTS `show_presentation`;
CREATE TABLE `show_presentation`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `start_time` datetime(6) NULL DEFAULT NULL,
  `end_time` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `organizer_id` bigint NOT NULL,
  `speaker_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code` ASC) USING BTREE,
  INDEX `show_presentation_organizer_id_8450fa2f_fk_users_users_id`(`organizer_id` ASC) USING BTREE,
  INDEX `show_presentation_speaker_id_662ddd3f_fk_users_users_id`(`speaker_id` ASC) USING BTREE,
  CONSTRAINT `show_presentation_organizer_id_8450fa2f_fk_users_users_id` FOREIGN KEY (`organizer_id`) REFERENCES `users_users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `show_presentation_speaker_id_662ddd3f_fk_users_users_id` FOREIGN KEY (`speaker_id`) REFERENCES `users_users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of show_presentation
-- ----------------------------

-- ----------------------------
-- Table structure for users_users
-- ----------------------------
DROP TABLE IF EXISTS `users_users`;
CREATE TABLE `users_users`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `role` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_users
-- ----------------------------
INSERT INTO `users_users` VALUES (1, 'aqing', '15211832257pt', '2389893881@qq.com', 'ORGANIZER', '2025-07-14 08:57:34.030830');
INSERT INTO `users_users` VALUES (2, 'zhangsan1', '123', '12345678@qq.com', 'ORGANIZER', '2025-07-14 10:08:41.305457');
INSERT INTO `users_users` VALUES (3, 'jmc', '123', '1379925133@qq.com', 'ORGANIZER', '2025-07-14 11:28:24.504892');
INSERT INTO `users_users` VALUES (4, '123', '123', '1410446243@qq.com', 'ORGANIZER', '2025-07-14 11:55:31.372614');

SET FOREIGN_KEY_CHECKS = 1;
