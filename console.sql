CREATE DATABASE IF NOT EXISTS busline_prisezone;
USE busline_prisezone;

-- Company Table
CREATE TABLE Company (
    CompanyName VARCHAR(100) PRIMARY KEY,
    VAT VARCHAR(20)
);

-- BusLine Table
CREATE TABLE BusLine (
    BusLineID INT PRIMARY KEY,
    Route VARCHAR(255),
    BusLineName VARCHAR(100),
    Length DECIMAL(5,2),
    CompanyName VARCHAR(100),
    AmountOfSeats INT,
    AmountOfCrew INT,
    OnWay TINYINT(1),
    FOREIGN KEY (CompanyName) REFERENCES Company(CompanyName)
);

-- Station Table
CREATE TABLE Station (
    StationNumber INT PRIMARY KEY,
    StationName VARCHAR(100),
    BusLineID INT,
    FOREIGN KEY (BusLineID) REFERENCES BusLine(BusLineID)
);

-- Bus Table
CREATE TABLE Bus (
    BusNumber VARCHAR(50) PRIMARY KEY,
    BusLineID INT,
    AmountOfSeats INT,
    AmountOfCrew INT,
    OnWay TINYINT(1),
    FOREIGN KEY (BusLineID) REFERENCES BusLine(BusLineID)
);

-- Crew Table
CREATE TABLE Crew (
    CrewID INT PRIMARY KEY,
    CrewRole VARCHAR(100),
    CrewName VARCHAR(100),
    BusNumber VARCHAR(50),
    FOREIGN KEY (BusNumber) REFERENCES Bus(BusNumber)
);

-- Zone Table
CREATE TABLE Zone (
    ZoneID INT PRIMARY KEY,
    Price DECIMAL(5,2)
);

-- Ticket Table
CREATE TABLE Ticket (
    TicketNumber VARCHAR(50) PRIMARY KEY,
    TicketType VARCHAR(50),
    ZoneID INT,
    SeatNumber INT,
    PassengerID VARCHAR(20),
    BusLineID INT,
    StationNumber INT,
    BusNumber INT,
    FOREIGN KEY (ZoneID) REFERENCES Zone(ZoneID),
    FOREIGN KEY (PassengerID) REFERENCES Passenger(PassengerID),
    FOREIGN KEY (BusLineID) REFERENCES BusLine(BusLineID),
    FOREIGN KEY (StationNumber) REFERENCES Station(StationNumber),
    FOREIGN KEY (BusNumber) REFERENCES Bus(BusNumber)
);

-- Passenger Table
CREATE TABLE Passenger (
    PassengerID VARCHAR(20) PRIMARY KEY,
    PassengerName VARCHAR(100)
);