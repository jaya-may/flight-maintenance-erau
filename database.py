import sqlite3

class AirframeDatabase:
    def setup_database(self, db_name='airframes.db'):
        self.db_name = db_name
        self.create_airframes_table()
        self.create_maintenance_logs_table()

    def create_airframes_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Airframes (
                id INTEGER PRIMARY KEY,
                tailnumber TEXT NOT NULL,
                image BLOB
            )
        ''')
        conn.commit()
        conn.close()

    def create_maintenance_logs_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS MaintenanceLogs (
                id INTEGER PRIMARY KEY,
                airframe_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                tag TEXT,
                body TEXT,
                image BLOB,
                FOREIGN KEY (airframe_id) REFERENCES Airframes (id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        conn.close()

    def add_airframe(self, tailnumber, image_path=None):
        image_data = None
        if image_path:
            with open(image_path, 'rb') as file:
                image_data = file.read()

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Airframes (tailnumber, image)
            VALUES (?, ?)
        ''', (tailnumber, image_data))
        conn.commit()
        conn.close()

    def get_all_airframes(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Airframes')
        airframes = cursor.fetchall()
        conn.close()
        return airframes

    def add_maintenance_log(self, airframe_id, title, tag, body, image_path=None):
        image_data = None
        if image_path:
            with open(image_path, 'rb') as file:
                image_data = file.read()

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO MaintenanceLogs (airframe_id, title, tag, body, image)
            VALUES (?, ?, ?, ?, ?)
        ''', (airframe_id, title, tag, body, image_data))
        conn.commit()
        conn.close()

    def get_maintenance_logs_for_airframe(self, airframe_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM MaintenanceLogs WHERE airframe_id = ?
        ''', (airframe_id,))
        logs = cursor.fetchall()
        conn.close()
        return logs

    def get_maintenance_log_image(self, log_id, output_path):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT image FROM MaintenanceLogs WHERE id = ?
        ''', (log_id,))
        image_data = cursor.fetchone()
        conn.close()

        if image_data and image_data[0]:
            with open(output_path, 'wb') as file:
                file.write(image_data[0])
            print(f"{output_path}")
        else:
            print("WHY")


db = AirframeDatabase()
db.setup_database()

db.add_airframe('N12345', 'C:\\Users\\NEBS\\Documents\\BRUH.png')

db.add_maintenance_log(1, 'inspected', 'inspected', 'dummy', 'C:\\Users\\NEBS\\Documents\\BRUH.png')
db.add_maintenance_log(1, 'repair', 'repair', 'dummy repair')

logs = db.get_maintenance_logs_for_airframe(1)
print("Maintenance Logs:", logs)

db.get_maintenance_log_image(1, 'output_log_image.jpg')

input("waiting")