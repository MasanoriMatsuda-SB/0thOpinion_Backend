-- Active: 1732756335965@@localhost@3306@0thopiniondb
-- データベースを作成
CREATE DATABASE IF NOT EXISTS 0thOpinionDB;

-- 作成したデータベースを使用
USE 0thOpinionDB;

-- AnimalHospital テーブル
CREATE TABLE AnimalHospital (
    Hospital_id INT PRIMARY KEY AUTO_INCREMENT,
    Hospital_name VARCHAR(255) NOT NULL,
    Hospital_address VARCHAR(255) NOT NULL
);

-- Veterinarian テーブル
CREATE TABLE Veterinarian (
    Veterinarian_id INT PRIMARY KEY AUTO_INCREMENT,
    Veterinarian_name VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Screen_name VARCHAR(255),
    Sex CHAR(1),
    Birth_date DATE,
    Hospital_id INT,
    Email VARCHAR(255),
    FOREIGN KEY (Hospital_id) REFERENCES AnimalHospital(Hospital_id)
);

-- User テーブル
CREATE TABLE User (
    User_id INT PRIMARY KEY AUTO_INCREMENT,
    User_name VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Screen_name VARCHAR(255),
    Sex CHAR(1),
    Birth_date DATE,
    Address VARCHAR(255),
    Email VARCHAR(255)    
);

-- Disease テーブル
CREATE TABLE Disease (
    Disease_id INT PRIMARY KEY AUTO_INCREMENT,
    Disease_name VARCHAR(255) NOT NULL
);

-- Pet テーブル
CREATE TABLE Pet (
    Pet_id INT PRIMARY KEY AUTO_INCREMENT,
    Pet_name VARCHAR(255) NOT NULL,
    Image BLOB,
    Gender CHAR(1),
    Birth_date DATE,
    Neuter_Spay BOOLEAN,
    Disease_id INT,
    User_id INT,
    FOREIGN KEY (Disease_id) REFERENCES Disease(Disease_id),
    FOREIGN KEY (User_id) REFERENCES User(User_id)
);

-- Question テーブル
CREATE TABLE Question (
    Question_id INT PRIMARY KEY AUTO_INCREMENT,
    User_id INT,
    Question_date DATETIME NOT NULL,
    Content TEXT NOT NULL,
    Image VARCHAR(255),
    Movie VARCHAR(255),
    AI_answer TEXT,
    Resolved BOOLEAN,
    FOREIGN KEY (User_id) REFERENCES User(User_id)
);

-- Answer テーブル
CREATE TABLE Answer (
    Answer_id INT PRIMARY KEY AUTO_INCREMENT,
    Veterinarian_id INT,
    Question_id INT,
    Answer_date DATETIME NOT NULL,
    FOREIGN KEY (Veterinarian_id) REFERENCES Veterinarian(Veterinarian_id),
    FOREIGN KEY (Question_id) REFERENCES Question(Question_id)
);

-- Animal テーブル
CREATE TABLE Animal (
    Animal_id INT PRIMARY KEY AUTO_INCREMENT,
    Animal_name VARCHAR(255) NOT NULL
);

-- Breed テーブル
CREATE TABLE Breed (
    Breed_id INT PRIMARY KEY AUTO_INCREMENT,
    Breed_name VARCHAR(255) NOT NULL
);

-- AnimalBreed テーブル
CREATE TABLE AnimalBreed (
    Animal_id INT,
    Breed_id INT,
    PRIMARY KEY (Animal_id, Breed_id),
    FOREIGN KEY (Animal_id) REFERENCES Animal(Animal_id),
    FOREIGN KEY (Breed_id) REFERENCES Breed(Breed_id)
);

-- PetAnimal テーブル
CREATE TABLE PetAnimal (
    Pet_id INT,
    Animal_id INT,
    PRIMARY KEY (Pet_id, Animal_id),
    FOREIGN KEY (Pet_id) REFERENCES Pet(Pet_id),
    FOREIGN KEY (Animal_id) REFERENCES Animal(Animal_id)
);