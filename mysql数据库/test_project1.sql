/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50620
Source Host           : localhost:3306
Source Database       : test_project1

Target Server Type    : MYSQL
Target Server Version : 50620
File Encoding         : 65001

Date: 2020-06-26 16:42:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `admin`
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_psw` varchar(32) NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('2', '123456');
INSERT INTO `admin` VALUES ('3', '123456');

-- ----------------------------
-- Table structure for `alembic_version`
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('43e3712b519b');

-- ----------------------------
-- Table structure for `department`
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department` (
  `depart_id` int(11) NOT NULL AUTO_INCREMENT,
  `depart_name` varchar(32) NOT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`depart_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of department
-- ----------------------------
INSERT INTO `department` VALUES ('1', '人事部', '0');
INSERT INTO `department` VALUES ('2', '市场部', '0');

-- ----------------------------
-- Table structure for `recruiter`
-- ----------------------------
DROP TABLE IF EXISTS `recruiter`;
CREATE TABLE `recruiter` (
  `recruiter_id` int(11) NOT NULL AUTO_INCREMENT,
  `recruiter_name` varchar(32) NOT NULL,
  `recruiter_age` int(11) DEFAULT NULL,
  `recruiter_gender` enum('MAN','WOMAN') DEFAULT NULL,
  `recruiter_mobile` varchar(11) NOT NULL,
  `recruiter_email` varchar(60) NOT NULL,
  PRIMARY KEY (`recruiter_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of recruiter
-- ----------------------------
INSERT INTO `recruiter` VALUES ('1', '王晓婷', '23', 'WOMAN', '1308491234', 'xiaoting@163.com');
INSERT INTO `recruiter` VALUES ('2', '李晓天', '25', 'MAN', '13598081235', 'xiaotian@qq.com');

-- ----------------------------
-- Table structure for `rewardspunishment`
-- ----------------------------
DROP TABLE IF EXISTS `rewardspunishment`;
CREATE TABLE `rewardspunishment` (
  `user_id` int(11) NOT NULL,
  `reward` int(11) DEFAULT NULL,
  `punishment` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `rewardspunishment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of rewardspunishment
-- ----------------------------
INSERT INTO `rewardspunishment` VALUES ('1001', '300', '100', '0');
INSERT INTO `rewardspunishment` VALUES ('1002', '500', '200', '0');

-- ----------------------------
-- Table structure for `superadmin`
-- ----------------------------
DROP TABLE IF EXISTS `superadmin`;
CREATE TABLE `superadmin` (
  `superadmin_id` int(11) NOT NULL AUTO_INCREMENT,
  `superadmin_psw` varchar(32) NOT NULL,
  PRIMARY KEY (`superadmin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of superadmin
-- ----------------------------
INSERT INTO `superadmin` VALUES ('1', '123456');

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(32) NOT NULL,
  `user_age` int(11) DEFAULT NULL,
  `user_gender` enum('MAN','WOMAN') DEFAULT NULL,
  `depart_id` int(11) DEFAULT NULL,
  `user_mobile` varchar(11) NOT NULL,
  `user_email` varchar(60) NOT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `depart_id` (`depart_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`depart_id`) REFERENCES `department` (`depart_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1003 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1001', '李威', '28', 'MAN', '1', '13508312034', 'liwei@126.com', '0');
INSERT INTO `user` VALUES ('1002', '王国胜', '30', 'MAN', '2', '15082083023', 'guosheng@163.com', '0');
