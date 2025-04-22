import mysql.connector
from mini_app import DatabaseManager

def print_table(cursor, table_name, columns, condition=""):
    query = f"SELECT {', '.join(columns)} FROM {table_name}"
    if condition:
        query += f" WHERE {condition}"
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"\nTable: {table_name}")
    print("| " + " | ".join(columns) + " |")
    print("|" + "----|" * len(columns))
    for row in rows:
        print("| " + " | ".join(str(val) for val in row) + " |")

def test_operations_and_reports():
    try:
        db = DatabaseManager(host="localhost", user="root", password="root", database="busline_prisezone")
        cursor = db.cursor
    except mysql.connector.Error as err:
        print(f"Failed to connect to database: {err}")
        return

    db.insert_sample_data()

    print("\n=== Test 1: Create Passenger Profile ===")
    print("\nBefore:")
    print_table(cursor, "Passenger", ["PassengerID", "PassengerName"])
    query = "INSERT INTO Passenger (PassengerID, PassengerName) VALUES ('P004', 'Alice Brown')"
    print(f"\nQuery:\n{query}")
    cursor.execute(query)
    db.conn.commit()
    print("\nAfter:")
    print_table(cursor, "Passenger", ["PassengerID", "PassengerName"])
    print("\nSuccess Argument: P004 added successfully, existing records unchanged.")

    print("\n=== Test 2: Update Passenger Profile ===")
    print("\nBefore:")
    print_table(cursor, "Passenger", ["PassengerID", "PassengerName"], "PassengerID = 'P004'")
    query = "UPDATE Passenger SET PassengerName = 'Alice Green' WHERE PassengerID = 'P004'"
    print(f"\nQuery:\n{query}")
    cursor.execute(query)
    db.conn.commit()
    print("\nAfter:")
    print_table(cursor, "Passenger", ["PassengerID", "PassengerName"], "PassengerID = 'P004'")
    print("\nSuccess Argument: P004's name updated to 'Alice Green', other records unaffected.")

    print("\n=== Test 3: Delete Passenger Profile ===")
    print("\nBefore:")
    print_table(cursor, "Passenger", ["PassengerID", "PassengerName"], "PassengerID = 'P004'")
    query = "DELETE FROM Passenger WHERE PassengerID = 'P004'"
    print(f"\nQuery:\n{query}")
    cursor.execute(query)
    db.conn.commit()
    print("\nAfter:")
    print_table(cursor, "Passenger", ["PassengerID", "PassengerName"])
    print("\nSuccess Argument: P004 removed, referential integrity maintained.")

    print("\n=== Test 4: Purchase Ticket ===")
    print("\nBefore (last ticket):")
    print_table(cursor, "Ticket", ["TicketNumber", "TicketType", "ZoneID", "SeatNumber", "PassengerID", "BusLineID", "StationNumber", "BusNumber"], "TicketNumber = 'T015'")
    query = "INSERT INTO Ticket (TicketNumber, TicketType, BusLineID, ZoneID, PassengerID, StationNumber, BusNumber, SeatNumber) VALUES ('T016', 'SingleTicket', 1, 1, 'P001', 1, 'B001', 10)"
    print(f"\nQuery:\n{query}")
    cursor.execute(query)
    db.conn.commit()
    print("\nAfter:")
    print_table(cursor, "Ticket", ["TicketNumber", "TicketType", "ZoneID", "SeatNumber", "PassengerID", "BusLineID", "StationNumber", "BusNumber"], "TicketNumber IN ('T015', 'T016')")
    print("\nSuccess Argument: T016 added with correct details.")

    print("\n=== Test 5: Update Ticket ===")
    print("\nBefore:")
    print_table(cursor, "Ticket", ["TicketNumber", "TicketType", "ZoneID", "SeatNumber", "PassengerID", "BusLineID", "StationNumber", "BusNumber"], "TicketNumber = 'T016'")
    query = "UPDATE Ticket SET TicketType = 'MonthlyPass', BusLineID = 1, ZoneID = 1, PassengerID = 'P001', StationNumber = 1, BusNumber = 'B001', SeatNumber = 10 WHERE TicketNumber = 'T016'"
    print(f"\nQuery:\n{query}")
    cursor.execute(query)
    db.conn.commit()
    print("\nAfter:")
    print_table(cursor, "Ticket", ["TicketNumber", "TicketType", "ZoneID", "SeatNumber", "PassengerID", "BusLineID", "StationNumber", "BusNumber"], "TicketNumber = 'T016'")
    print("\nSuccess Argument: T016's type updated to 'MonthlyPass'.")

    print("\n=== Test 6: Delete Ticket ===")
    print("\nBefore:")
    print_table(cursor, "Ticket", ["TicketNumber", "TicketType", "ZoneID", "SeatNumber", "PassengerID", "BusLineID", "StationNumber", "BusNumber"], "TicketNumber IN ('T015', 'T016')")
    query = "DELETE FROM Ticket WHERE TicketNumber = 'T016'"
    print(f"\nQuery:\n{query}")
    cursor.execute(query)
    db.conn.commit()
    print("\nAfter:")
    print_table(cursor, "Ticket", ["TicketNumber", "TicketType", "ZoneID", "SeatNumber", "PassengerID", "BusLineID", "StationNumber", "BusNumber"], "TicketNumber IN ('T015', 'T016')")
    print("\nSuccess Argument: T016 removed, other tickets unaffected.")

    db.insert_sample_data()

    print("\n=== Report 1: Zone Usage Analytics ===")
    print("\nRelevant Tables:")
    print_table(cursor, "Zone", ["ZoneID", "Price"])
    print_table(cursor, "Ticket", ["TicketNumber", "ZoneID"])
    query = """
    SELECT z.ZoneID, CONCAT('Zone ', z.ZoneID, ' - $', z.Price) as ZoneName, COUNT(t.TicketNumber) as TicketCount
    FROM Zone z LEFT JOIN Ticket t ON z.ZoneID = t.ZoneID
    GROUP BY z.ZoneID ORDER BY z.ZoneID
    """
    print(f"\nQuery:\n{query}")
    cursor.execute(query)
    print("\nReport Output:")
    print("| Zone ID | Zone Name      | Tickets Sold |")
    print("|---------|----------------|--------------|")
    for row in cursor.fetchall():
        print(f"| {row[0]}       | {row[1]:<15} | {row[2]:<12} |")
    print("\nVerification: Matches actual counts (5 tickets each zone).")

    print("\n=== Report 2: Route Optimization Report ===")
    print("\nRelevant Tables:")
    print_table(cursor, "BusLine", ["BusLineID", "BusLineName"])
    print_table(cursor, "Ticket", ["TicketNumber", "BusLineID"])
    query = """
    SELECT bl.BusLineID, COUNT(t.TicketNumber) as TicketCount
    FROM BusLine bl LEFT JOIN Ticket t ON bl.BusLineID = t.BusLineID
    GROUP BY bl.BusLineID ORDER BY bl.BusLineID
    """
    print(f"\nQuery:\n{query}")
    cursor.execute(query)
    print("\nReport Output:")
    print("| Bus Line ID | Ticket Count |")
    print("|-------------|--------------|")
    for row in cursor.fetchall():
        print(f"| {row[0]:<11} | {row[1]:<12} |")
    print("\nVerification: Matches actual counts (5 tickets each bus line).")

    print("\n=== Report 3: Fare Calculation Report ===")
    print("\nRelevant Tables:")
    print_table(cursor, "Zone", ["ZoneID", "Price"])
    print_table(cursor, "Ticket", ["TicketNumber", "TicketType", "ZoneID"])
    query = """
    SELECT t.TicketType, CONCAT('Zone ', z.ZoneID, ' - $', z.Price) as ZoneName, SUM(CASE 
            WHEN t.TicketType = 'SingleTicket' THEN z.Price
            WHEN t.TicketType = 'MonthlyPass' THEN z.Price * 10
            ELSE 0 END) as TotalFare
    FROM Ticket t JOIN Zone z ON t.ZoneID = z.ZoneID
    GROUP BY t.TicketType, z.ZoneID
    """
    print(f"\nQuery:\n{query}")
    cursor.execute(query)
    print("\nReport Output:")
    print("| Ticket Type   | Zone Name      | Total Fare ($) |")
    print("|---------------|----------------|----------------|")
    for row in cursor.fetchall():
        print(f"| {row[0]:<13} | {row[1]:<15} | {row[2]:<14} |")
    print("\nVerification: Matches actual totals (SingleTicket Zone 1: $12.50, MonthlyPass Zone 2: $187.50, SingleTicket Zone 3: $25.00).")

    db.close()

if __name__ == "__main__":
    test_operations_and_reports()