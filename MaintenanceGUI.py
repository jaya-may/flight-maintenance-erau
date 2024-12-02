import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import io
import LogInGUI

# AirframeDatabase class handles database operations
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
        airframe_id = cursor.lastrowid
        conn.close()
        return airframe_id

    def get_all_airframes(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, tailnumber, image FROM Airframes')
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
        log_id = cursor.lastrowid
        conn.close()
        return log_id

    def get_maintenance_logs_for_airframe(self, airframe_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, tag, body FROM MaintenanceLogs WHERE airframe_id = ?
        ''', (airframe_id,))
        logs = cursor.fetchall()
        conn.close()
        return logs

    def get_maintenance_log_image(self, log_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT image FROM MaintenanceLogs WHERE id = ?
        ''', (log_id,))
        image_data = cursor.fetchone()
        conn.close()
        return image_data[0] if image_data and image_data[0] else None

    def get_airframe_image(self, airframe_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT image FROM Airframes WHERE id = ?
        ''', (airframe_id,))
        image_data = cursor.fetchone()
        conn.close()
        return image_data[0] if image_data and image_data[0] else None

# Initializes the database
db = AirframeDatabase()
db.setup_database()

# Dictionary that stores GUI elements and images
maintenance_page = {}
image_tooltip = None

def load_planes_from_database():
    airframes = db.get_all_airframes()
    for airframe in airframes:
        airframe_id, tailnumber, image_data = airframe
        # Creates the image from image_data
        if image_data:
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((300, 300), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(image)
        else:
            tk_image = None
        # Creates button for the plane
        button = tk.Button(records_frame, text=tailnumber, font=("Arial", 18),
                           command=lambda tid=airframe_id, tnumber=tailnumber: open_plane_page(tid, tnumber))
        button.pack(pady=10, fill=tk.X)
        # Binds events for tooltip
        button.bind("<Enter>", lambda event, tid=airframe_id: show_image_tooltip(event, tid))
        button.bind("<Leave>", hide_image_tooltip)
        # Stores in maintenance_page
        maintenance_page[airframe_id] = {'tailnumber': tailnumber, 'button': button, 'image': tk_image}

def delete_log_prompt(log_id, logs_window):
    # Displays a confirmation prompt for deleting a maintenance log.
    prompt_window = tk.Toplevel()
    prompt_window.title("Delete Log Confirmation")
    prompt_window.geometry('400x200')

    tk.Label(prompt_window, text="Are you sure you want to delete this log?", font=("Arial", 14)).pack(pady=10)
    tk.Label(prompt_window, text="(This action cannot be undone)", font=("Arial", 12), fg="red").pack(pady=5)

    def confirm_delete():
        prompt_window.destroy()
        confirmation_window = tk.Toplevel()
        confirmation_window.title("Final Confirmation")
        confirmation_window.geometry('400x200')

        tk.Label(confirmation_window, text="Type 'delete' to confirm:", font=("Arial", 14)).pack(pady=10)
        delete_entry = tk.Entry(confirmation_window, font=("Arial", 14))
        delete_entry.pack(pady=10)

        def final_delete():
            if delete_entry.get().lower() == "delete":
                conn = sqlite3.connect(db.db_name)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM MaintenanceLogs WHERE id = ?", (log_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Maintenance log deleted successfully.")
                confirmation_window.destroy()
                logs_window.destroy()
            else:
                messagebox.showerror("Error", "Incorrect confirmation. Log not deleted.")

        tk.Button(confirmation_window, text="Confirm", command=final_delete, font=("Arial", 14)).pack(pady=10)
        tk.Button(confirmation_window, text="Back", command=confirmation_window.destroy, font=("Arial", 14)).pack(pady=10)

    tk.Button(prompt_window, text="Yes", command=confirm_delete, font=("Arial", 14)).pack(side=tk.LEFT, padx=20, pady=20)
    tk.Button(prompt_window, text="No", command=prompt_window.destroy, font=("Arial", 14)).pack(side=tk.RIGHT, padx=20, pady=20)


def open_plane_page(airframe_id, plane_tail):
    root.withdraw()  # Hides the main menu window

    plane_page = tk.Toplevel()
    plane_page.title(f"Plane: {plane_tail}")
    plane_page.state('zoomed')

    plane_page.columnconfigure(0, weight=1)
    plane_page.rowconfigure(0, weight=1)

    plane_frame = tk.Frame(plane_page)
    plane_frame.grid(row=0, column=0, sticky='nsew')
    plane_frame.columnconfigure((0, 1), weight=1)

    label = tk.Label(plane_frame, text=f"Plane: {plane_tail}", font=("Arial", 20))
    label.grid(row=0, column=0, columnspan=2, pady=20, sticky='n')

    tk.Button(plane_frame, text="View Log", width=20, font=("Arial", 16),
              command=lambda: view_logs(airframe_id)).grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    tk.Button(plane_frame, text="Add Log", width=20, font=("Arial", 16),
              command=lambda: add_log(airframe_id)).grid(row=1, column=1, padx=10, pady=10, sticky='ew')

    back_button = tk.Button(plane_frame, text="Back to Main Menu",
                            command=lambda: go_back_to_main_menu(plane_page), font=("Arial", 16))
    back_button.grid(row=3, column=0, columnspan=2, pady=30)

    image_data = db.get_airframe_image(airframe_id)
    if image_data:
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((300, 300), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)
        image_label = tk.Label(plane_frame, image=tk_image)
        image_label.image = tk_image
        image_label.grid(row=4, column=0, columnspan=2, pady=10)

def go_back_to_main_menu(plane_page):
    plane_page.destroy()
    root.deiconify()
    root.state('zoomed')

def add_plane():
    plane_tail = add_entry.get()
    if plane_tail:
        airframes = db.get_all_airframes()
        existing_tailnumbers = [tailnumber for _, tailnumber, _ in airframes]
        if plane_tail not in existing_tailnumbers:
            image_path = filedialog.askopenfilename(title='Select Image',
                                                    filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.gif;*.bmp')])
            if image_path:
                try:
                    image = Image.open(image_path)
                    image = image.resize((300, 300), Image.LANCZOS)
                    tk_image = ImageTk.PhotoImage(image)
                except Exception as e:
                    messagebox.showerror("Error", f"Unable to load image: {e}")
                    return
            else:
                messagebox.showwarning("Input Error", "No image selected. Plane will not be added.")
                return

            airframe_id = db.add_airframe(plane_tail, image_path)

            button = tk.Button(records_frame, text=plane_tail, font=("Arial", 18),
                               command=lambda tid=airframe_id, tnumber=plane_tail: open_plane_page(tid, tnumber))
            button.pack(pady=10, fill=tk.X)

            button.bind("<Enter>", lambda event, tid=airframe_id: show_image_tooltip(event, tid))
            button.bind("<Leave>", hide_image_tooltip)

            maintenance_page[airframe_id] = {'tailnumber': plane_tail, 'button': button, 'image': tk_image}

            add_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"'{plane_tail}' already exists.")
    else:
        messagebox.showwarning("Input Error", "Please enter a plane's tail number.")

def search_planes():
    query = search_entry.get().lower()
    for airframe_id, data in maintenance_page.items():
        tailnumber = data['tailnumber']
        button = data['button']
        if query in tailnumber.lower():
            button.pack(pady=10, fill=tk.X)
        else:
            button.pack_forget()
            hide_image_tooltip(None)

def show_image_tooltip(event, airframe_id):
    global image_tooltip
    image = maintenance_page[airframe_id]['image']
    if image:
        image_tooltip = tk.Toplevel()
        image_tooltip.wm_overrideredirect(True)
        image_tooltip.wm_geometry("+%d+%d" % (event.x_root + 20, event.y_root + 20))
        label = tk.Label(image_tooltip, image=image)
        label.pack()

def hide_image_tooltip(event):
    global image_tooltip
    if image_tooltip:
        image_tooltip.destroy()
        image_tooltip = None

def add_log(airframe_id):
    log_window = tk.Toplevel()
    log_window.title("Add Maintenance Log")
    log_window.geometry('500x600')

    tk.Label(log_window, text="Title:", font=("Arial", 14)).pack(pady=5)
    title_entry = tk.Entry(log_window, font=("Arial", 14))
    title_entry.pack(pady=5)

    tk.Label(log_window, text="Tag:", font=("Arial", 14)).pack(pady=5)
    tag_entry = tk.Entry(log_window, font=("Arial", 14))
    tag_entry.pack(pady=5)

    tk.Label(log_window, text="Body:", font=("Arial", 14)).pack(pady=5)
    body_text = tk.Text(log_window, font=("Arial", 14), height=10)
    body_text.pack(pady=5)

    def select_image():
        image_path = filedialog.askopenfilename(title='Select Image',
                                                filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.gif;*.bmp')])
        image_path_var.set(image_path)

    image_path_var = tk.StringVar()

    tk.Button(log_window, text="Select Image", command=select_image, font=("Arial", 14)).pack(pady=5)
    tk.Label(log_window, textvariable=image_path_var, font=("Arial", 12)).pack(pady=5)

    # Variable to track whether to save the log to a file
    save_to_file_var = tk.IntVar()

    tk.Checkbutton(log_window, text="Save log to a file", variable=save_to_file_var, font=("Arial", 12)).pack(pady=5)

    def save_log():
        title = title_entry.get()
        tag = tag_entry.get()
        body = body_text.get("1.0", tk.END).strip()
        image_path = image_path_var.get()

        if title and body:
            log_id = db.add_maintenance_log(airframe_id, title, tag, body, image_path)
            if save_to_file_var.get():
                # Saves the log to a text file
                file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                         filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                         title="Save Log As")
                if file_path:
                    try:
                        with open(file_path, 'w') as f:
                            f.write(f"Title: {title}\n")
                            f.write(f"Tag: {tag}\n")
                            f.write(f"Body:\n{body}\n")
                            if image_path:
                                f.write(f"Image Path: {image_path}\n")
                        messagebox.showinfo("Success", "Log saved to file successfully.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to save log to file: {e}")
            else:
                messagebox.showinfo("Success", "Maintenance log added successfully.")
            log_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Title and Body are required.")

    tk.Button(log_window, text="Save Log", command=save_log, font=("Arial", 14)).pack(pady=10)

def view_logs(airframe_id):
    def search_logs():
        query = search_entry.get().lower()
        for frame, log in zip(log_frames, logs):
            log_title = log[1].lower()
            if query in log_title:
                frame.pack(fill=tk.X, padx=10, pady=5)
            else:
                frame.pack_forget()

    logs_window = tk.Toplevel()
    logs_window.title("Maintenance Logs")
    logs_window.geometry('600x400')

    # Search bar
    search_frame = tk.Frame(logs_window)
    search_frame.pack(fill=tk.X, pady=5)

    tk.Label(search_frame, text="Search Logs:", font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 14))
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    search_button = tk.Button(search_frame, text="Search", command=search_logs, font=("Arial", 14))
    search_button.pack(side=tk.LEFT, padx=5)

    # Logs display area
    log_display_frame = tk.Frame(logs_window)
    log_display_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    logs = db.get_maintenance_logs_for_airframe(airframe_id)
    log_frames = []

    if logs:
        for log in logs:
            log_id, title, tag, body = log
            frame = tk.Frame(log_display_frame, bd=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=10, pady=5)

            log_frames.append(frame)  # Store the frame for searching

            tk.Label(frame, text=f"Title: {title}", font=("Arial", 14)).pack(anchor='w')
            tk.Label(frame, text=f"Tag: {tag}", font=("Arial", 12)).pack(anchor='w')
            tk.Label(frame, text=f"Body: {body}", font=("Arial", 12), wraplength=500).pack(anchor='w')

            def show_log_image(log_id=log_id):
                image_data = db.get_maintenance_log_image(log_id)
                if image_data:
                    image = Image.open(io.BytesIO(image_data))
                    image = image.resize((300, 300), Image.LANCZOS)
                    tk_image = ImageTk.PhotoImage(image)

                    image_window = tk.Toplevel()
                    image_window.title("Log Image")
                    tk.Label(image_window, image=tk_image).pack()
                    image_window.image = tk_image
                else:
                    messagebox.showinfo("No Image", "No image available for this log.")

            tk.Button(frame, text="View Image", command=show_log_image, font=("Arial", 12)).pack(pady=5)
            tk.Button(frame, text="Delete Log", command=lambda log_id=log_id: delete_log_prompt(log_id, logs_window),
                      font=("Arial", 12), fg="red").pack(pady=5)
    else:
        tk.Label(log_display_frame, text="No maintenance logs found for this plane.", font=("Arial", 14)).pack(pady=20)



def setup_main_menu():
    global add_entry, search_entry, records_frame
    # Now set up the main menu GUI
    root.title("Maintenance Tracker")
    root.state('zoomed') 

    # Configures root window grid
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    # Creates a frame for the top section (search and add)
    top_frame = tk.Frame(root)
    top_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)

    # Configures columns in top_frame
    top_frame.columnconfigure(1, weight=1)
    top_frame.columnconfigure(4, weight=1)

    # Adds the Plane Section
    add_label = tk.Label(top_frame, text="Add Plane:", font=("Arial", 16))
    add_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    add_entry = tk.Entry(top_frame, font=("Arial", 16))
    add_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    add_button = tk.Button(top_frame, text="Add", command=add_plane, font=("Arial", 16))
    add_button.grid(row=0, column=2, padx=5, pady=5)

    # Adds the Search Section
    search_label = tk.Label(top_frame, text="Search:", font=("Arial", 16))
    search_label.grid(row=0, column=3, padx=5, pady=5, sticky='w')

    search_entry = tk.Entry(top_frame, font=("Arial", 16))
    search_entry.grid(row=0, column=4, padx=5, pady=5, sticky='ew')

    search_button = tk.Button(top_frame, text="Search", command=search_planes, font=("Arial", 16))
    search_button.grid(row=0, column=5, padx=5, pady=5)

    # Frame that displays maintenance page buttons
    records_frame = tk.Frame(root)
    records_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

    # Configures records_frame to expand
    root.rowconfigure(1, weight=1)

    # Loads existing planes from the database
    load_planes_from_database()

# Initialize the main application
root = tk.Tk()

# Call the login_page function from LogInGUI.py
login_successful = LogInGUI.login_page(root)

if login_successful:
    # Proceed to main menu
    setup_main_menu()
else:
    # Show error message and exit
    messagebox.showerror("Login Failed", "Incorrect username or password.")
    root.destroy()


# Starts the Tkinter event loop
root.mainloop()
