import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="root", database="busline_prisezone"):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(buffered=True)
            self.create_tables()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Error", f"Failed to connect to MySQL database: {err}")
            raise

    def create_tables(self):
        self.cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in self.cursor.fetchall()]
        
        if 'company' not in existing_tables:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Company (
                CompanyName VARCHAR(100) PRIMARY KEY,
                VAT VARCHAR(20)
            )
            ''')
            
        if 'busline' not in existing_tables:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BusLine (
                BusLineID INT PRIMARY KEY,
                Route VARCHAR(255),
                BusLineName VARCHAR(100),
                Length DECIMAL(5,2),
                CompanyName VARCHAR(100),
                AmountOfSeats INT,
                AmountOfCrew INT,
                OnWay TINYINT(1),
                FOREIGN KEY (CompanyName) REFERENCES Company(CompanyName)
            )
            ''')
            
        if 'station' not in existing_tables:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Station (
                StationNumber INT PRIMARY KEY,
                StationName VARCHAR(100),
                BusLineID INT,
                FOREIGN KEY (BusLineID) REFERENCES BusLine(BusLineID)
            )
            ''')
            
        if 'bus' not in existing_tables:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Bus (
                BusNumber VARCHAR(50) PRIMARY KEY,
                BusLineID INT,
                AmountOfSeats INT,
                AmountOfCrew INT,
                OnWay TINYINT(1),
                FOREIGN KEY (BusLineID) REFERENCES BusLine(BusLineID)
            )
            ''')
            
        if 'crew' not in existing_tables:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Crew (
                CrewID INT PRIMARY KEY,
                CrewRole VARCHAR(100),
                CrewName VARCHAR(100),
                BusNumber VARCHAR(50),
                FOREIGN KEY (BusNumber) REFERENCES Bus(BusNumber)
            )
            ''')
            
        if 'zone' not in existing_tables:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Zone (
                ZoneID INT PRIMARY KEY,
                Price DECIMAL(5,2)
            )
            ''')
            
        if 'passenger' not in existing_tables:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Passenger (
                PassengerID VARCHAR(20) PRIMARY KEY,
                PassengerName VARCHAR(100)
            )
            ''')
            
        if 'ticket' not in existing_tables:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ticket (
                TicketNumber VARCHAR(50) PRIMARY KEY,
                TicketType VARCHAR(50),
                ZoneID INT,
                SeatNumber INT,
                PassengerID VARCHAR(20),
                BusLineID INT,
                StationNumber INT,
                BusNumber VARCHAR(50),
                FOREIGN KEY (ZoneID) REFERENCES Zone(ZoneID),
                FOREIGN KEY (PassengerID) REFERENCES Passenger(PassengerID),
                FOREIGN KEY (BusLineID) REFERENCES BusLine(BusLineID),
                FOREIGN KEY (StationNumber) REFERENCES Station(StationNumber),
                FOREIGN KEY (BusNumber) REFERENCES Bus(BusNumber)
            )
            ''')
            
        self.cursor.execute("SELECT COUNT(*) FROM Company")
        self.insert_sample_data()
            
        self.conn.commit()

    def insert_sample_data(self):
        self.cursor.execute("DELETE FROM Ticket")
        self.cursor.execute("DELETE FROM Passenger")
        self.cursor.execute("DELETE FROM Zone")
        self.cursor.execute("DELETE FROM Crew")
        self.cursor.execute("DELETE FROM Bus")
        self.cursor.execute("DELETE FROM Station")
        self.cursor.execute("DELETE FROM BusLine")
        self.cursor.execute("DELETE FROM Company")
        self.conn.commit()

        self.cursor.execute('''
        INSERT INTO Company (CompanyName, VAT) 
        VALUES ('Metro Transit', 'MT123456789')
        ''')
        
        bus_lines = [
            (1, 'Downtown to North End', 'Red Line', 15.5, 'Metro Transit', 50, 2, 1),
            (2, 'Airport to South Side', 'Blue Line', 18.2, 'Metro Transit', 40, 2, 1),
            (3, 'East to West', 'Green Line', 12.8, 'Metro Transit', 60, 2, 1)
        ]
        self.cursor.executemany('''
        INSERT INTO BusLine (BusLineID, Route, BusLineName, Length, CompanyName, AmountOfSeats, AmountOfCrew, OnWay)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', bus_lines)
        
        stations = [
            (1, 'Downtown Central', 1),
            (2, 'North End Terminal', 1),
            (3, 'Airport Terminal', 2),
            (4, 'South Side Station', 2),
            (5, 'East Terminal', 3),
            (6, 'West Terminal', 3)
        ]
        self.cursor.executemany('''
        INSERT INTO Station (StationNumber, StationName, BusLineID)
        VALUES (%s, %s, %s)
        ''', stations)
        
        buses = [
            ('B001', 1, 50, 2, 1),
            ('B002', 2, 40, 2, 1),
            ('B003', 3, 60, 2, 1)
        ]
        self.cursor.executemany('''
        INSERT INTO Bus (BusNumber, BusLineID, AmountOfSeats, AmountOfCrew, OnWay)
        VALUES (%s, %s, %s, %s, %s)
        ''', buses)
        
        crew_members = [
            (1, 'Driver', 'John Smith', 'B001'),
            (2, 'Attendant', 'Mary Johnson', 'B001'),
            (3, 'Driver', 'James Brown', 'B002'),
            (4, 'Attendant', 'Sarah Davis', 'B002'),
            (5, 'Driver', 'Michael Wilson', 'B003'),
            (6, 'Attendant', 'Lisa Thompson', 'B003')
        ]
        self.cursor.executemany('''
        INSERT INTO Crew (CrewID, CrewRole, CrewName, BusNumber)
        VALUES (%s, %s, %s, %s)
        ''', crew_members)
        
        zones = [
            (1, 2.50),
            (2, 3.75),
            (3, 5.00)
        ]
        self.cursor.executemany('''
        INSERT INTO Zone (ZoneID, Price)
        VALUES (%s, %s)
        ''', zones)
        
        passengers = [
            ('P001', 'John Doe'),
            ('P002', 'Jane Smith'),
            ('P003', 'Robert Johnson')
        ]
        self.cursor.executemany('''
        INSERT INTO Passenger (PassengerID, PassengerName)
        VALUES (%s, %s)
        ''', passengers)

        tickets = [
            ('T001', 'SingleTicket', 1, 10, 'P001', 1, 1, 'B001'),
            ('T002', 'MonthlyPass', 2, 15, 'P002', 1, 1, 'B001'),
            ('T003', 'SingleTicket', 3, 20, 'P003', 2, 3, 'B002'),
            ('T004', 'SingleTicket', 1, 25, 'P001', 2, 4, 'B002'),
            ('T005', 'MonthlyPass', 2, 30, 'P002', 3, 5, 'B003'),
            ('T006', 'SingleTicket', 3, 5, 'P003', 3, 6, 'B003'),
            ('T007', 'SingleTicket', 1, 12, 'P001', 1, 2, 'B001'),
            ('T008', 'MonthlyPass', 2, 18, 'P002', 2, 3, 'B002'),
            ('T009', 'SingleTicket', 3, 22, 'P003', 3, 5, 'B003'),
            ('T010', 'SingleTicket', 1, 28, 'P001', 1, 1, 'B001'),
            ('T011', 'MonthlyPass', 2, 8, 'P002', 2, 4, 'B002'),
            ('T012', 'SingleTicket', 3, 14, 'P003', 3, 6, 'B003'),
            ('T013', 'SingleTicket', 1, 16, 'P001', 1, 1, 'B001'),
            ('T014', 'MonthlyPass', 2, 21, 'P002', 2, 3, 'B002'),
            ('T015', 'SingleTicket', 3, 27, 'P003', 3, 5, 'B003')
        ]
        self.cursor.executemany('''
        INSERT INTO Ticket (TicketNumber, TicketType, ZoneID, SeatNumber, PassengerID, BusLineID, StationNumber, BusNumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', tickets)
        
        self.conn.commit()

    def get_all_passengers(self):
        self.cursor.execute("SELECT PassengerID, PassengerName FROM Passenger")
        return self.cursor.fetchall()

    def get_passenger(self, passenger_id):
        self.cursor.execute("SELECT PassengerID, PassengerName FROM Passenger WHERE PassengerID = %s", (passenger_id,))
        return self.cursor.fetchone()

    def create_passenger(self, passenger_id, passenger_name):
        try:
            self.cursor.execute('''
            INSERT INTO Passenger (PassengerID, PassengerName)
            VALUES (%s, %s)
            ''', (passenger_id, passenger_name))
            self.conn.commit()
            return passenger_id
        except Exception as e:
            print(f"Error creating passenger: {e}")
            return None

    def update_passenger(self, passenger_id, passenger_name):
        try:
            self.cursor.execute('''
            UPDATE Passenger
            SET PassengerName = %s
            WHERE PassengerID = %s
            ''', (passenger_name, passenger_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating passenger: {e}")
            return False

    def delete_passenger(self, passenger_id):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Ticket WHERE PassengerID = %s", (passenger_id,))
            if self.cursor.fetchone()[0] > 0:
                return False, "Cannot delete passenger with existing tickets"
            
            self.cursor.execute("DELETE FROM Passenger WHERE PassengerID = %s", (passenger_id,))
            self.conn.commit()
            return True, "Passenger deleted successfully"
        except Exception as e:
            print(f"Error deleting passenger: {e}")
            return False, f"Error: {str(e)}"

    def get_all_bus_lines(self):
        self.cursor.execute("SELECT BusLineID, BusLineName FROM BusLine")
        return self.cursor.fetchall()

    def get_all_zones(self):
        self.cursor.execute("SELECT ZoneID, CONCAT('Zone ', ZoneID, ' - $', Price) FROM Zone")
        return self.cursor.fetchall()
        
    def get_all_stations(self):
        self.cursor.execute("SELECT StationNumber, StationName FROM Station")
        return self.cursor.fetchall()
        
    def get_all_buses(self):
        self.cursor.execute("SELECT BusNumber, BusLineID FROM Bus")
        return self.cursor.fetchall()

    def insert_ticket(self, ticket_number, ticket_type, bus_line_id, zone_id, passenger_id, station_number, bus_number, seat_number):
        try:
            self.cursor.execute('''
            INSERT INTO Ticket (TicketNumber, TicketType, BusLineID, ZoneID, PassengerID, StationNumber, BusNumber, SeatNumber)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (ticket_number, ticket_type, bus_line_id, zone_id, passenger_id, station_number, bus_number, seat_number))
            self.conn.commit()
            return ticket_number
        except Exception as e:
            print(f"Error inserting ticket: {e}")
            return None

    def get_all_tickets(self):
        self.cursor.execute("""
        SELECT TicketNumber, TicketType, BusLineID, ZoneID, PassengerID, StationNumber, BusNumber, SeatNumber 
        FROM Ticket
        """)
        return self.cursor.fetchall()

    def get_ticket(self, ticket_number):
        self.cursor.execute("""
        SELECT TicketNumber, TicketType, BusLineID, ZoneID, PassengerID, StationNumber, BusNumber, SeatNumber 
        FROM Ticket 
        WHERE TicketNumber = %s
        """, (ticket_number,))
        return self.cursor.fetchone()

    def update_ticket(self, ticket_number, ticket_type, bus_line_id, zone_id, passenger_id, station_number, bus_number, seat_number):
        try:
            self.cursor.execute('''
            UPDATE Ticket
            SET TicketType = %s, BusLineID = %s, ZoneID = %s, PassengerID = %s, 
                StationNumber = %s, BusNumber = %s, SeatNumber = %s
            WHERE TicketNumber = %s
            ''', (ticket_type, bus_line_id, zone_id, passenger_id, station_number, bus_number, seat_number, ticket_number))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating ticket: {e}")
            return False

    def delete_ticket(self, ticket_number):
        try:
            self.cursor.execute("DELETE FROM Ticket WHERE TicketNumber = %s", (ticket_number,))
            self.conn.commit()
            return True, "Ticket deleted successfully"
        except Exception as e:
            print(f"Error deleting ticket: {e}")
            return False, f"Error: {str(e)}"

    def close(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()


class PurchaseTicketForm(tk.Toplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager
        self.title("Purchase Ticket")
        self.geometry("500x500")
        self.resizable(True, True)

        tk.Label(self, text="Purchase Ticket", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

        form_frame = tk.Frame(self)
        form_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        passenger_frame = tk.LabelFrame(form_frame, text="Passenger Information")
        passenger_frame.pack(fill=tk.X, pady=5)

        passenger_select_frame = tk.Frame(passenger_frame)
        passenger_select_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(passenger_select_frame, text="Select Passenger:").grid(row=0, column=0, sticky="w", padx=5)
        self.passenger_var = tk.StringVar()
        self.passenger_combo = ttk.Combobox(passenger_select_frame, textvariable=self.passenger_var, width=30)
        self.passenger_combo.grid(row=0, column=1, padx=5)
        
        tk.Button(passenger_select_frame, text="Manage Passengers", command=self.open_passenger_management).grid(row=0, column=2, padx=5)

        ticket_frame = tk.LabelFrame(form_frame, text="Ticket Information")
        ticket_frame.pack(fill=tk.X, pady=5)

        tk.Label(ticket_frame, text="Ticket Number:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.ticket_number_var = tk.StringVar()
        self.ticket_number_entry = tk.Entry(ticket_frame, textvariable=self.ticket_number_var, width=30)
        self.ticket_number_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(ticket_frame, text="Bus Line:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.bus_line_var = tk.StringVar()
        self.bus_line_dropdown = ttk.Combobox(ticket_frame, textvariable=self.bus_line_var, width=30)
        self.bus_line_dropdown.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(ticket_frame, text="Station:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.station_var = tk.StringVar()
        self.station_dropdown = ttk.Combobox(ticket_frame, textvariable=self.station_var, width=30)
        self.station_dropdown.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(ticket_frame, text="Bus Number:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.bus_number_var = tk.StringVar()
        self.bus_number_dropdown = ttk.Combobox(ticket_frame, textvariable=self.bus_number_var, width=30)
        self.bus_number_dropdown.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(ticket_frame, text="Zone:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.zone_var = tk.StringVar()
        self.zone_dropdown = ttk.Combobox(ticket_frame, textvariable=self.zone_var, width=30)
        self.zone_dropdown.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Label(ticket_frame, text="Seat Number:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.seat_number_var = tk.StringVar()
        self.seat_number_entry = tk.Entry(ticket_frame, textvariable=self.seat_number_var, width=30)
        self.seat_number_entry.grid(row=5, column=1, padx=10, pady=10)

        tk.Label(ticket_frame, text="Ticket Type:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.ticket_type_var = tk.StringVar()
        self.ticket_type_dropdown = ttk.Combobox(ticket_frame, textvariable=self.ticket_type_var, width=30, 
                                               values=["SingleTicket", "MonthlyPass"])
        self.ticket_type_dropdown.grid(row=6, column=1, padx=10, pady=10)
        self.ticket_type_dropdown.current(0)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=2, column=0, pady=20)
        tk.Button(btn_frame, text="Save", width=10, command=self.save_ticket).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Purchase Ticket", width=15, command=self.purchase_ticket).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Clear", width=10, command=self.clear_form).pack(side=tk.LEFT, padx=10)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(0, weight=1)
        form_frame.grid_columnconfigure(0, weight=1)

        self.load_bus_lines()
        self.load_zones()
        self.load_passengers()
        self.load_stations()
        self.load_buses()
    
    def load_passengers(self):
        passengers = self.db_manager.get_all_passengers()
        self.passenger_combo['values'] = [f"{p[0]}: {p[1]}" for p in passengers]
        if passengers:
            self.passenger_combo.current(0)
    
    def open_passenger_management(self):
        passenger_form = PassengerManagementForm(self, self.db_manager)
        self.wait_window(passenger_form)
        self.load_passengers()

    def load_bus_lines(self):
        bus_lines = self.db_manager.get_all_bus_lines()
        self.bus_line_dropdown['values'] = [f"{bl[0]}: {bl[1]}" for bl in bus_lines]
        if bus_lines:
            self.bus_line_dropdown.current(0)

    def load_zones(self):
        zones = self.db_manager.get_all_zones()
        self.zone_dropdown['values'] = [f"{z[0]}: {z[1]}" for z in zones]
        if zones:
            self.zone_dropdown.current(0)
            
    def load_stations(self):
        stations = self.db_manager.get_all_stations()
        self.station_dropdown['values'] = [f"{s[0]}: {s[1]}" for s in stations]
        if stations:
            self.station_dropdown.current(0)
            
    def load_buses(self):
        buses = self.db_manager.get_all_buses()
        self.bus_number_dropdown['values'] = [f"{b[0]}: BusLine {b[1]}" for b in buses]
        if buses:
            self.bus_number_dropdown.current(0)

    def save_ticket(self):
        if not self.passenger_var.get() or not self.ticket_number_var.get():
            messagebox.showwarning("Validation Error", "Passenger and Ticket Number are required!")
            return
            
        passenger_id = self.passenger_var.get().split(":")[0] if self.passenger_var.get() else ""
        bus_line_id = self.bus_line_var.get().split(":")[0] if self.bus_line_var.get() else ""
        zone_id = self.zone_var.get().split(":")[0] if self.zone_var.get() else ""
        station_number = self.station_var.get().split(":")[0] if self.station_var.get() else ""
        bus_number = self.bus_number_var.get().split(":")[0] if self.bus_number_var.get() else ""
        seat_number = self.seat_number_var.get()
        ticket_type = self.ticket_type_var.get()
        ticket_number = self.ticket_number_var.get()

        if not all([passenger_id, bus_line_id, zone_id, station_number, bus_number, seat_number, ticket_type, ticket_number]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return

        result = self.db_manager.insert_ticket(
            ticket_number, ticket_type, bus_line_id, zone_id, passenger_id, 
            station_number, bus_number, seat_number
        )
        
        if result:
            messagebox.showinfo("Success", f"Ticket saved successfully!\nTicket Number: {ticket_number}")
        else:
            messagebox.showerror("Error", "Failed to save ticket!")

    def purchase_ticket(self):
        if not self.passenger_var.get() or not self.ticket_number_var.get():
            messagebox.showwarning("Validation Error", "Passenger and Ticket Number are required!")
            return
            
        passenger_id = self.passenger_var.get().split(":")[0] if self.passenger_var.get() else ""
        bus_line_id = self.bus_line_var.get().split(":")[0] if self.bus_line_var.get() else ""
        zone_id = self.zone_var.get().split(":")[0] if self.zone_var.get() else ""
        station_number = self.station_var.get().split(":")[0] if self.station_var.get() else ""
        bus_number = self.bus_number_var.get().split(":")[0] if self.bus_number_var.get() else ""
        seat_number = self.seat_number_var.get()
        ticket_type = self.ticket_type_var.get()
        ticket_number = self.ticket_number_var.get()

        if not all([passenger_id, bus_line_id, zone_id, station_number, bus_number, seat_number, ticket_type, ticket_number]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return

        result = self.db_manager.insert_ticket(
            ticket_number, ticket_type, bus_line_id, zone_id, passenger_id, 
            station_number, bus_number, seat_number
        )
        
        if result:
            messagebox.showinfo("Success", f"Ticket purchased successfully!\nTicket Number: {ticket_number}")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to create ticket!")

    def clear_form(self):
        self.ticket_number_var.set("")
        self.seat_number_var.set("")
        if self.passenger_combo['values']:
            self.passenger_combo.current(0)
        if self.bus_line_dropdown['values']:
            self.bus_line_dropdown.current(0)
        if self.zone_dropdown['values']:
            self.zone_dropdown.current(0)
        if self.station_dropdown['values']:
            self.station_dropdown.current(0)
        if self.bus_number_dropdown['values']:
            self.bus_number_dropdown.current(0)
        self.ticket_type_dropdown.current(0)


class PassengerManagementForm(tk.Toplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager
        self.title("Passenger Management")
        self.geometry("500x400")
        self.resizable(True, True)
        
        tk.Label(self, text="Passenger Management", font=("Arial", 14, "bold")).pack(pady=10)
        
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tree_frame = tk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.passenger_tree = ttk.Treeview(tree_frame, columns=("id", "name"), show="headings")
        self.passenger_tree.heading("id", text="ID")
        self.passenger_tree.heading("name", text="Name")
        
        self.passenger_tree.column("id", width=100)
        self.passenger_tree.column("name", width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.passenger_tree.yview)
        self.passenger_tree.configure(yscroll=scrollbar.set)
        
        self.passenger_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.passenger_tree.bind("<ButtonRelease-1>", self.on_passenger_select)
        
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="Add New", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_passenger).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.load_passengers).pack(side=tk.RIGHT, padx=5)
        
        right_frame = tk.LabelFrame(main_frame, text="Passenger Details")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        form_frame = tk.Frame(right_frame)
        form_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        tk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.id_var = tk.StringVar()
        self.id_entry = tk.Entry(form_frame, textvariable=self.id_var, width=30)
        self.id_entry.grid(row=0, column=1, pady=5, sticky="w")
        
        tk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(form_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=1, column=1, pady=5, sticky="w")
        
        action_frame = tk.Frame(form_frame)
        action_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        self.save_btn = tk.Button(action_frame, text="Save", width=10, command=self.save_passenger)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="Cancel", width=10, command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        form_frame.grid_rowconfigure(0, weight=1)
        form_frame.grid_rowconfigure(1, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        self.selected_passenger_id = None
        self.clear_form()
        self.load_passengers()
    
    def load_passengers(self):
        for item in self.passenger_tree.get_children():
            self.passenger_tree.delete(item)
        
        passengers = self.db_manager.get_all_passengers()
        for passenger in passengers:
            self.passenger_tree.insert("", "end", values=passenger)
    
    def on_passenger_select(self, event):
        selected = self.passenger_tree.focus()
        if selected:
            values = self.passenger_tree.item(selected, "values")
            if values:
                self.selected_passenger_id = values[0]
                passenger = self.db_manager.get_passenger(self.selected_passenger_id)
                if passenger:
                    self.id_var.set(passenger[0])
                    self.name_var.set(passenger[1])
    
    def clear_form(self):
        self.selected_passenger_id = None
        self.id_var.set("")
        self.name_var.set("")
        self.id_entry.config(state="normal")
        if self.passenger_tree.selection():
            self.passenger_tree.selection_remove(self.passenger_tree.selection())
    
    def save_passenger(self):
        passenger_id = self.id_var.get().strip()
        name = self.name_var.get().strip()
        
        if not passenger_id or not name:
            messagebox.showwarning("Validation Error", "Passenger ID and name are required!")
            return
        
        if self.selected_passenger_id:
            if self.db_manager.update_passenger(passenger_id, name):
                messagebox.showinfo("Success", "Passenger updated successfully!")
                self.clear_form()
                self.load_passengers()
            else:
                messagebox.showerror("Error", "Failed to update passenger!")
        else:
            result = self.db_manager.create_passenger(passenger_id, name)
            if result:
                messagebox.showinfo("Success", f"Passenger created successfully!\nID: {passenger_id}")
                self.clear_form()
                self.load_passengers()
            else:
                messagebox.showerror("Error", "Failed to create passenger!")
    
    def delete_passenger(self):
        if not self.selected_passenger_id:
            messagebox.showwarning("Warning", "Please select a passenger first!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this passenger?"):
            success, message = self.db_manager.delete_passenger(self.selected_passenger_id)
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.load_passengers()
            else:
                messagebox.showerror("Error", message)


class TicketManagementForm(tk.Toplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager
        self.title("Ticket Management")
        self.geometry("800x1200")
        self.resizable(True, True)
        
        tk.Label(self, text="Ticket Management", font=("Arial", 14, "bold")).pack(pady=10)
        
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tree_frame = tk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ticket_tree = ttk.Treeview(tree_frame, columns=("ticket_number", "ticket_type", "bus_line", "zone", "passenger", "station", "bus", "seat"), show="headings")
        self.ticket_tree.heading("ticket_number", text="Ticket Number")
        self.ticket_tree.heading("ticket_type", text="Type")
        self.ticket_tree.heading("bus_line", text="Bus Line")
        self.ticket_tree.heading("zone", text="Zone")
        self.ticket_tree.heading("passenger", text="Passenger")
        self.ticket_tree.heading("station", text="Station")
        self.ticket_tree.heading("bus", text="Bus")
        self.ticket_tree.heading("seat", text="Seat")
        
        self.ticket_tree.column("ticket_number", width=100)
        self.ticket_tree.column("ticket_type", width=80)
        self.ticket_tree.column("bus_line", width=80)
        self.ticket_tree.column("zone", width=80)
        self.ticket_tree.column("passenger", width=80)
        self.ticket_tree.column("station", width=80)
        self.ticket_tree.column("bus", width=80)
        self.ticket_tree.column("seat", width=80)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.ticket_tree.yview)
        self.ticket_tree.configure(yscroll=scrollbar.set)
        
        self.ticket_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.ticket_tree.bind("<ButtonRelease-1>", self.on_ticket_select)
        
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="Add New", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_ticket).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.load_tickets).pack(side=tk.RIGHT, padx=5)
        
        right_frame = tk.LabelFrame(main_frame, text="Ticket Details")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        form_frame = tk.Frame(right_frame)
        form_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        tk.Label(form_frame, text="Ticket Number:").grid(row=0, column=0, sticky="w", pady=5)
        self.ticket_number_var = tk.StringVar()
        self.ticket_number_entry = tk.Entry(form_frame, textvariable=self.ticket_number_var, width=30)
        self.ticket_number_entry.grid(row=0, column=1, pady=5, sticky="w")
        
        tk.Label(form_frame, text="Ticket Type:").grid(row=1, column=0, sticky="w", pady=5)
        self.ticket_type_var = tk.StringVar()
        self.ticket_type_dropdown = ttk.Combobox(form_frame, textvariable=self.ticket_type_var, width=30, 
                                                values=["SingleTicket", "MonthlyPass"])
        self.ticket_type_dropdown.grid(row=1, column=1, pady=5, sticky="w")
        
        tk.Label(form_frame, text="Bus Line:").grid(row=2, column=0, sticky="w", pady=5)
        self.bus_line_var = tk.StringVar()
        self.bus_line_dropdown = ttk.Combobox(form_frame, textvariable=self.bus_line_var, width=30)
        self.bus_line_dropdown.grid(row=2, column=1, pady=5, sticky="w")

        tk.Label(form_frame, text="Zone:").grid(row=3, column=0, sticky="w", pady=5)
        self.zone_var = tk.StringVar()
        self.zone_dropdown = ttk.Combobox(form_frame, textvariable=self.zone_var, width=30)
        self.zone_dropdown.grid(row=3, column=1, pady=5, sticky="w")
        
        tk.Label(form_frame, text="Passenger:").grid(row=4, column=0, sticky="w", pady=5)
        self.passenger_var = tk.StringVar()
        self.passenger_dropdown = ttk.Combobox(form_frame, textvariable=self.passenger_var, width=30)
        self.passenger_dropdown.grid(row=4, column=1, pady=5, sticky="w")
        
        tk.Label(form_frame, text="Station:").grid(row=5, column=0, sticky="w", pady=5)
        self.station_var = tk.StringVar()
        self.station_dropdown = ttk.Combobox(form_frame, textvariable=self.station_var, width=30)
        self.station_dropdown.grid(row=5, column=1, pady=5, sticky="w")
        
        tk.Label(form_frame, text="Bus Number:").grid(row=6, column=0, sticky="w", pady=5)
        self.bus_number_var = tk.StringVar()
        self.bus_number_dropdown = ttk.Combobox(form_frame, textvariable=self.bus_number_var, width=30)
        self.bus_number_dropdown.grid(row=6, column=1, pady=5, sticky="w")
        
        tk.Label(form_frame, text="Seat Number:").grid(row=7, column=0, sticky="w", pady=5)
        self.seat_number_var = tk.StringVar()
        self.seat_number_entry = tk.Entry(form_frame, textvariable=self.seat_number_var, width=30)
        self.seat_number_entry.grid(row=7, column=1, pady=5, sticky="w")
        
        action_frame = tk.Frame(form_frame)
        action_frame.grid(row=8, column=0, columnspan=2, pady=15)
        
        tk.Button(action_frame, text="Save", width=10, command=self.save_ticket).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Cancel", width=10, command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        form_frame.grid_rowconfigure(0, weight=1)
        form_frame.grid_rowconfigure(1, weight=1)
        form_frame.grid_rowconfigure(2, weight=1)
        form_frame.grid_rowconfigure(3, weight=1)
        form_frame.grid_rowconfigure(4, weight=1)
        form_frame.grid_rowconfigure(5, weight=1)
        form_frame.grid_rowconfigure(6, weight=1)
        form_frame.grid_rowconfigure(7, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        self.selected_ticket_number = None
        self.load_tickets()
        self.load_dropdowns()
    
    def load_tickets(self):
        for item in self.ticket_tree.get_children():
            self.ticket_tree.delete(item)
        
        tickets = self.db_manager.get_all_tickets()
        for ticket in tickets:
            self.ticket_tree.insert("", "end", values=ticket)
    
    def load_dropdowns(self):
        passengers = self.db_manager.get_all_passengers()
        self.passenger_dropdown['values'] = [f"{p[0]}: {p[1]}" for p in passengers]
        if passengers:
            self.passenger_dropdown.current(0)
            
        bus_lines = self.db_manager.get_all_bus_lines()
        self.bus_line_dropdown['values'] = [f"{bl[0]}: {bl[1]}" for bl in bus_lines]
        if bus_lines:
            self.bus_line_dropdown.current(0)
            
        zones = self.db_manager.get_all_zones()
        self.zone_dropdown['values'] = [f"{z[0]}: {z[1]}" for z in zones]
        if zones:
            self.zone_dropdown.current(0)
            
        stations = self.db_manager.get_all_stations()
        self.station_dropdown['values'] = [f"{s[0]}: {s[1]}" for s in stations]
        if stations:
            self.station_dropdown.current(0)
            
        buses = self.db_manager.get_all_buses()
        self.bus_number_dropdown['values'] = [f"{b[0]}: BusLine {b[1]}" for b in buses]
        if buses:
            self.bus_number_dropdown.current(0)
    
    def on_ticket_select(self, event):
        selected = self.ticket_tree.focus()
        if selected:
            values = self.ticket_tree.item(selected, "values")
            if values:
                self.selected_ticket_number = values[0]
                ticket = self.db_manager.get_ticket(self.selected_ticket_number)
                if ticket:
                    self.ticket_number_var.set(ticket[0])
                    self.ticket_type_var.set(ticket[1])
                    self.bus_line_var.set(f"{ticket[2]}: {self.get_bus_line_name(ticket[2])}")
                    self.zone_var.set(f"{ticket[3]}: Zone {ticket[3]} - ${self.get_zone_price(ticket[3])}")
                    self.passenger_var.set(f"{ticket[4]}: {self.get_passenger_name(ticket[4])}")
                    self.station_var.set(f"{ticket[5]}: {self.get_station_name(ticket[5])}")
                    self.bus_number_var.set(f"{ticket[6]}: BusLine {self.get_bus_line_id(ticket[6])}")
                    self.seat_number_var.set(ticket[7])
                    self.ticket_number_entry.config(state="disabled")
    
    def get_bus_line_name(self, bus_line_id):
        self.cursor.execute("SELECT BusLineName FROM BusLine WHERE BusLineID = %s", (bus_line_id,))
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def get_zone_price(self, zone_id):
        self.cursor.execute("SELECT Price FROM Zone WHERE ZoneID = %s", (zone_id,))
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def get_passenger_name(self, passenger_id):
        self.cursor.execute("SELECT PassengerName FROM Passenger WHERE PassengerID = %s", (passenger_id,))
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def get_station_name(self, station_number):
        self.cursor.execute("SELECT StationName FROM Station WHERE StationNumber = %s", (station_number,))
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def get_bus_line_id(self, bus_number):
        self.cursor.execute("SELECT BusLineID FROM Bus WHERE BusNumber = %s", (bus_number,))
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def clear_form(self):
        self.selected_ticket_number = None
        self.ticket_number_var.set("")
        self.ticket_type_var.set("")
        self.bus_line_var.set("")
        self.zone_var.set("")
        self.passenger_var.set("")
        self.station_var.set("")
        self.bus_number_var.set("")
        self.seat_number_var.set("")
        self.ticket_number_entry.config(state="normal")
        if self.ticket_tree.selection():
            self.ticket_tree.selection_remove(self.ticket_tree.selection())
        if self.passenger_dropdown['values']:
            self.passenger_dropdown.current(0)
        if self.bus_line_dropdown['values']:
            self.bus_line_dropdown.current(0)
        if self.zone_dropdown['values']:
            self.zone_dropdown.current(0)
        if self.station_dropdown['values']:
            self.station_dropdown.current(0)
        if self.bus_number_dropdown['values']:
            self.bus_number_dropdown.current(0)
        self.ticket_type_dropdown.current(0)
    
    def save_ticket(self):
        ticket_number = self.ticket_number_var.get().strip()
        ticket_type = self.ticket_type_var.get().strip()
        bus_line_id = self.bus_line_var.get().split(":")[0] if self.bus_line_var.get() else ""
        zone_id = self.zone_var.get().split(":")[0] if self.zone_var.get() else ""
        passenger_id = self.passenger_var.get().split(":")[0] if self.passenger_var.get() else ""
        station_number = self.station_var.get().split(":")[0] if self.station_var.get() else ""
        bus_number = self.bus_number_var.get().split(":")[0] if self.bus_number_var.get() else ""
        seat_number = self.seat_number_var.get().strip()
        
        if not all([ticket_number, ticket_type, bus_line_id, zone_id, passenger_id, station_number, bus_number, seat_number]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return
        
        if self.selected_ticket_number:
            if self.db_manager.update_ticket(
                ticket_number, ticket_type, bus_line_id, zone_id, passenger_id, 
                station_number, bus_number, seat_number
            ):
                messagebox.showinfo("Success", "Ticket updated successfully!")
                self.clear_form()
                self.load_tickets()
            else:
                messagebox.showerror("Error", "Failed to update ticket!")
        else:
            result = self.db_manager.insert_ticket(
                ticket_number, ticket_type, bus_line_id, zone_id, passenger_id, 
                station_number, bus_number, seat_number
            )
            if result:
                messagebox.showinfo("Success", f"Ticket created successfully!\nTicket Number: {ticket_number}")
                self.clear_form()
                self.load_tickets()
            else:
                messagebox.showerror("Error", "Failed to create ticket!")
    
    def delete_ticket(self):
        if not self.selected_ticket_number:
            messagebox.showwarning("Warning", "Please select a ticket first!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this ticket?"):
            success, message = self.db_manager.delete_ticket(self.selected_ticket_number)
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.load_tickets()
            else:
                messagebox.showerror("Error", message)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bus Ticket System")
        self.geometry("400x300")
        self.resizable(True, True)

        try:
            self.db_manager = DatabaseManager(
                host="localhost", 
                user="root",
                password="root",
                database="busline_prisezone"
            )
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            self.destroy()
            return

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Bus Ticket System", font=("Arial", 16, "bold")).pack(pady=20)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True)

        tk.Button(button_frame, text="Purchase Ticket", width=20, height=2, 
                 command=self.open_purchase_form).pack(pady=10)
        tk.Button(button_frame, text="Manage Passengers", width=20, height=2, 
                 command=self.open_passenger_management).pack(pady=10)
        tk.Button(button_frame, text="Manage Tickets", width=20, height=2, 
                 command=self.open_ticket_management).pack(pady=10)
        tk.Button(button_frame, text="Exit", width=20, height=2, 
                 command=self.quit_app).pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.quit_app)

    def open_purchase_form(self):
        try:
            PurchaseTicketForm(self, self.db_manager)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Purchase Ticket form: {str(e)}")

    def open_passenger_management(self):
        try:
            PassengerManagementForm(self, self.db_manager)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Passenger Management form: {str(e)}")

    def open_ticket_management(self):
        try:
            TicketManagementForm(self, self.db_manager)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Ticket Management form: {str(e)}")

    def quit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            if hasattr(self, 'db_manager'):
                self.db_manager.close()
            self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()