-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bookclubfav2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bookclubfav2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bookclubfav2` DEFAULT CHARACTER SET utf8 ;
USE `bookclubfav2` ;

-- -----------------------------------------------------
-- Table `bookclubfav2`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookclubfav2`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(50) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookclubfav2`.`bookclubs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookclubfav2`.`bookclubs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `description` TEXT(300) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_bookclubs_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_bookclubs_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `bookclubfav2`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bookclubfav2`.`favsubscriptions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookclubfav2`.`favsubscriptions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `bookclub_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_favorited_reviews_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_favorited_reviews_reviews1_idx` (`bookclub_id` ASC) VISIBLE,
  CONSTRAINT `fk_favorited_reviews_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `bookclubfav2`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_favorited_reviews_reviews1`
    FOREIGN KEY (`bookclub_id`)
    REFERENCES `bookclubfav2`.`bookclubs` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
