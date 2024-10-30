import tkinter as tk
from tkinter import messagebox

maintenance_page = {}

def open_plane_page(plane_tail):
    #Opens a new window for the selected maintenance record and close the main menu
    root.withdraw()  # Hides the main menu window till opened later

    # Creates a new window for the selected record
    plane_page = tk.Toplevel()
    plane_page.title(f"Plane: {plane_tail}")
    plane_page.geometry("300x300")

    # Displays the planes tail number
    tk.Label(plane_page, text=f"Plane: {plane_tail}", font=("Arial", 16)).pack(pady=20)

    # Creates buttons for log actions and maintenance status
    # Doesn't currently do anything
    tk.Button(plane_page, text="View Log", width=20).pack(pady=5)
    tk.Button(plane_page, text="Add Log", width=20).pack(pady=5)
    tk.Button(plane_page, text="Delete Log", width=20).pack(pady=5)
    tk.Button(plane_page, text="Maintenance Status", width=20).pack(pady=5)

    # Closes the plane's page and unhides the main menu
    back_button = tk.Button(plane_page, text="Back to Main Menu", 
                            command=lambda: go_back_to_main_menu(plane_page))
    back_button.pack(pady=20)

def go_back_to_main_menu(plane_page):
    """Close the record window and reopen the main menu."""
    plane_page.destroy()  # Closes the plane page
    root.deiconify()  # Show the main menu window

def add_plane():
    #Function to add a new plane page
    plane_tail = add_entry.get()
    if plane_tail:
        if plane_tail not in maintenance_page:
            # Create a button for the new record
            button = tk.Button(records_frame, text=plane_tail, font=("Arial", 12),
                               command=lambda: open_plane_page(plane_tail))
            maintenance_page[plane_tail] = button
            button.pack(pady=2, fill=tk.X)  # Displays the button
            add_entry.delete(0, tk.END)  # Clears the entry field
        else:
            messagebox.showerror("Error", f"'{plane_tail}' already exists.")
    else:
        messagebox.showwarning("Input Error", "Please enter a plane's tail number.")

def search_planes():
    #Function that filters planes based on the search.
    query = search_entry.get().lower()
    for name, button in maintenance_page.items():
        if query in name.lower():
            button.pack(pady=2, fill=tk.X)
        else:
            button.pack_forget()

# Creates the main menu window
root = tk.Tk()
root.title("Maintenance Tracker")
root.geometry("500x400")

# Creates a frame for the top section (search and add)
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X, padx=10, pady=5)

# Adds the Plab e Section
add_label = tk.Label(top_frame, text="Add Plane:")
add_label.grid(row=0, column=0, padx=5, pady=5)

add_entry = tk.Entry(top_frame, width=20)
add_entry.grid(row=0, column=1, padx=5, pady=5)

add_button = tk.Button(top_frame, text="Add", command=add_plane)
add_button.grid(row=0, column=2, padx=5, pady=5)

# Adds the Search Section
search_label = tk.Label(top_frame, text="Search:")
search_label.grid(row=0, column=3, padx=5, pady=5)

search_entry = tk.Entry(top_frame, width=20)
search_entry.grid(row=0, column=4, padx=5, pady=5)

search_button = tk.Button(top_frame, text="Search", command=search_planes)
search_button.grid(row=0, column=5, padx=5, pady=5)

# Frame that displays maintenance page buttons
records_frame = tk.Frame(root)
records_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
