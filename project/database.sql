-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET armscii8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Programming language`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Programming language` (
  `idLanguage` INT NOT NULL,
  PRIMARY KEY (`idLanguage`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `idUser` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NULL,
  `Password` VARCHAR(45) NULL,
  `Lastlogin` VARCHAR(45) NULL,
  `Age` INT NULL,
  `Country` VARCHAR(45) NULL,
  `Background` VARCHAR(45) NULL,
  `Preferred programming language_idLanguage` INT NOT NULL,
  PRIMARY KEY (`idUser`, `Preferred programming language_idLanguage`),
  INDEX `fk_User_Programming language1_idx` (`Preferred programming language_idLanguage` ASC) VISIBLE,
  CONSTRAINT `fk_User_Programming language1`
    FOREIGN KEY (`Preferred programming language_idLanguage`)
    REFERENCES `mydb`.`Programming language` (`idLanguage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Challenge`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Challenge` (
  `idChallenge` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Level` INT NULL,
  `Instructions` LONGTEXT NULL,
  `Test data` LONGTEXT NULL,
  `Solution` LONGTEXT NULL,
  `Hint` LONGTEXT NULL,
  PRIMARY KEY (`idChallenge`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Language of challenge`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Language of challenge` (
  `Challenge_idChallenge` INT NOT NULL,
  `Programming language_idLanguage` INT NOT NULL,
  `Example code` LONGTEXT NULL,
  PRIMARY KEY (`Challenge_idChallenge`, `Programming language_idLanguage`),
  INDEX `fk_Challenge_has_Programming language_Programming language1_idx` (`Programming language_idLanguage` ASC) VISIBLE,
  INDEX `fk_Challenge_has_Programming language_Challenge_idx` (`Challenge_idChallenge` ASC) VISIBLE,
  CONSTRAINT `fk_Challenge_has_Programming language_Challenge`
    FOREIGN KEY (`Challenge_idChallenge`)
    REFERENCES `mydb`.`Challenge` (`idChallenge`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Challenge_has_Programming language_Programming language1`
    FOREIGN KEY (`Programming language_idLanguage`)
    REFERENCES `mydb`.`Programming language` (`idLanguage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Challenge/User statistics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Challenge/User statistics` (
  `Challenge_idChallenge` INT NOT NULL,
  `User_idUser` VARCHAR(45) NOT NULL,
  `Starting date` DATETIME NULL,
  `Ending date` DATETIME NULL,
  `Tries` INT NULL,
  `Solved status` TINYINT(1) NULL,
  `Programming language_idLanguage` INT NOT NULL,
  PRIMARY KEY (`Challenge_idChallenge`, `User_idUser`),
  INDEX `fk_Challenge_has_User_User1_idx` (`User_idUser` ASC) VISIBLE,
  INDEX `fk_Challenge_has_User_Challenge1_idx` (`Challenge_idChallenge` ASC) VISIBLE,
  INDEX `fk_Challenge_has_User_Programming language1_idx` (`Programming language_idLanguage` ASC) VISIBLE,
  CONSTRAINT `fk_Challenge_has_User_Challenge1`
    FOREIGN KEY (`Challenge_idChallenge`)
    REFERENCES `mydb`.`Challenge` (`idChallenge`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Challenge_has_User_User1`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `mydb`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Challenge_has_User_Programming language1`
    FOREIGN KEY (`Programming language_idLanguage`)
    REFERENCES `mydb`.`Programming language` (`idLanguage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Category` (
  `idCategory` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  PRIMARY KEY (`idCategory`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Category of challenge`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Category of challenge` (
  `Category_idCategory` INT NOT NULL,
  `Challenge_idChallenge` INT NOT NULL,
  PRIMARY KEY (`Category_idCategory`, `Challenge_idChallenge`),
  INDEX `fk_Category_has_Challenge_Challenge1_idx` (`Challenge_idChallenge` ASC) VISIBLE,
  INDEX `fk_Category_has_Challenge_Category1_idx` (`Category_idCategory` ASC) VISIBLE,
  CONSTRAINT `fk_Category_has_Challenge_Category1`
    FOREIGN KEY (`Category_idCategory`)
    REFERENCES `mydb`.`Category` (`idCategory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Category_has_Challenge_Challenge1`
    FOREIGN KEY (`Challenge_idChallenge`)
    REFERENCES `mydb`.`Challenge` (`idChallenge`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
