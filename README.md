# Bus Ticket System

## Overview

The **Bus Ticket System** is a desktop application developed using **Python**, **Tkinter**, and **MySQL**. It is designed to facilitate the management of bus tickets, passenger information, and related data through an intuitive graphical user interface. The system enables users to purchase tickets, maintain passenger records, and manage ticket details efficiently.

---

## Features

- **Ticket Purchasing**: Generate new tickets by selecting a passenger, bus line, station, bus, zone, and ticket type.
- **Passenger Management**: Add, update, or delete passenger records from the system.
- **Ticket Management**: View, edit, or remove existing tickets.
- **Persistent Data Storage**: All information is stored in a MySQL database to ensure data integrity and consistency.

---

## System Requirements

- **Python** version 3.6 or higher
- **MySQL Server**
- Required Python packages:
  - `mysql-connector-python`
  - `tkinter` (typically bundled with Python)

---

## Installation Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/bus-ticket-system.git
cd bus-ticket-system
```

Alternatively, download and extract the ZIP archive.

### 2. Configure MySQL

- Ensure MySQL Server is installed and running.
- Create the application database:

```sql
CREATE DATABASE busline_prisezone;
```

- If your MySQL credentials differ from the default, update the database connection in the `DatabaseManager` class:

```python
self.db_manager = DatabaseManager(
    host="localhost",
    user="root",
    password="root",
    database="busline_prisezone"
)
```

### 3. Install Dependencies

Use the following command to install the required package:

```bash
pip install mysql-connector-python
```

### 4. Launch the Application

Execute the following command:

```bash
python bus_ticket_system.py
```

---

## Usage Guide

### Launching the Application

Upon execution, the main interface will appear, offering the following options:
- Purchase Tickets
- Manage Passengers
- Manage Tickets

### Ticket Purchase Workflow

1. Select **"Purchase Ticket"**.
2. Complete the form with all required details (passenger, bus line, station, bus, zone, ticket type, etc.).
3. Click **"Purchase Ticket"** to save and reset the form or **"Save"** to retain the entered data.

### Passenger Management

1. Select **"Manage Passengers"**.
2. Enter passenger ID and name to add a new entry.
3. Select an existing passenger to edit or delete the record.

### Ticket Management

1. Select **"Manage Tickets"**.
2. View existing tickets in the list.
3. Select a ticket to update its details or delete it.
4. Use **"Add New"** to create a new ticket entry.

### Exiting the Application

Click **"Exit"** or close the application window. A confirmation prompt will appear before exiting.

---

## Database Schema

The application uses the following MySQL tables:

| Table      | Description                                                                 |
|------------|-----------------------------------------------------------------------------|
| `Company`  | Stores company details (e.g., name, VAT number)                             |
| `BusLine`  | Stores information about bus lines (e.g., route, name, length, status)      |
| `Station`  | Stores station data including the associated bus line                       |
| `Bus`      | Contains details about individual buses, including assigned crew            |
| `Crew`     | Stores data about bus crew members, including roles and assigned buses      |
| `Zone`     | Represents fare zones and corresponding prices                              |
| `Passenger`| Contains records of passengers (ID and name)                                |
| `Ticket`   | Stores detailed ticket information including associations with other tables |

> The database is automatically populated with sample data upon application startup.

---

## Troubleshooting

- **Database Connection Failure**:  
  Ensure that the MySQL Server is active and that the connection credentials are correct in the code.

- **Tickets Not Displayed**:  
  Confirm that the database was populated with sample data. To verify:

  ```sql
  SELECT * FROM Ticket;
  ```

- **Dependency Issues**:  
  Make sure all required packages are installed using `pip`.

---

## License

This project is distributed under the terms of the [MIT License](LICENSE). You are free to use, modify, and distribute it as needed.

---

## Acknowledgments

- Developed using **Python**, **Tkinter**, and **MySQL**
- Inspired and supported by the open-source software community
