import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk  # Make sure to install this by entering "pip install pillow" in the command prompt

maintenance_page = {}
image_tooltip = None

def open_plane_page(plane_tail):
    # Opens a new window for the selected maintenance record and close the main menu
    root.withdraw()  # Hides the main menu window till opened later

    # Creates a new window for the selected record
    plane_page = tk.Toplevel()
    plane_page.title(f"Plane: {plane_tail}")
    plane_page.state('zoomed')

    # Creates grid layout for plane_page
    # I did this becuase without the grid all the buttons would be very small
    plane_page.columnconfigure(0, weight=1)
    plane_page.rowconfigure(0, weight=1)

    # Creates a frame inside plane_page
    plane_frame = tk.Frame(plane_page)
    plane_frame.grid(row=0, column=0, sticky='nsew')
    plane_frame.columnconfigure((0, 1), weight=1)

    # Displays the plane's tail number
    label = tk.Label(plane_frame, text=f"Plane: {plane_tail}", font=("Arial", 20))
    label.grid(row=0, column=0, columnspan=2, pady=20, sticky='n')

    # Creates buttons for log actions and maintenance status,
    # Doesn't currently do anything
    tk.Button(plane_frame, text="View Log", width=20, font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    tk.Button(plane_frame, text="Add Log", width=20, font=("Arial", 16)).grid(row=1, column=1, padx=10, pady=10, sticky='ew')
    tk.Button(plane_frame, text="Delete Log", width=20, font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    tk.Button(plane_frame, text="Maintenance Status", width=20, font=("Arial", 16)).grid(row=2, column=1, padx=10, pady=10, sticky='ew')

    # Closes the plane's page and unhides the main menu
    back_button = tk.Button(plane_frame, text="Back to Main Menu",
                            command=lambda: go_back_to_main_menu(plane_page), font=("Arial", 16))
    back_button.grid(row=3, column=0, columnspan=2, pady=30)

    # Gets the image from maintenance_page
    image = maintenance_page[plane_tail]['image']

    # Creates a Label to display the image
    image_label = tk.Label(plane_frame, image=image)
    image_label.image = image  # Keep a reference to avoid garbage collection
    image_label.grid(row=4, column=0, columnspan=2, pady=10)

def go_back_to_main_menu(plane_page):
    #Close the record window and reopen the main menu
    plane_page.destroy()  # Closes the plane page
    root.deiconify()      # Show the main menu window
    root.state('zoomed')  # Sets the main menu to fullscreen

def add_plane():
    # Function to add a new plane page
    plane_tail = add_entry.get()
    if plane_tail:
        if plane_tail not in maintenance_page:
            # Prompts the user to select an image file
            image_path = filedialog.askopenfilename(title='Select Image',
                                                    filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.gif;*.bmp')])
            if image_path:
                # Loads and resizes the image
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

            # Creates a button for the new record
            button = tk.Button(records_frame, text=plane_tail, font=("Arial", 18),
                               command=lambda: open_plane_page(plane_tail))
            button.pack(pady=10, fill=tk.X)  # Displays the button

            # Binsd events to show/hide image tooltip
            button.bind("<Enter>", lambda event, pt=plane_tail: show_image_tooltip(event, pt))
            button.bind("<Leave>", hide_image_tooltip)

            # Stores the button and image in maintenance_page
            maintenance_page[plane_tail] = {'button': button, 'image': tk_image}

            add_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"'{plane_tail}' already exists.")
    else:
        messagebox.showwarning("Input Error", "Please enter a plane's tail number.")

def search_planes():
    # Function that filters planes based on the search.
    query = search_entry.get().lower()
    for name, data in maintenance_page.items():
        button = data['button']
        if query in name.lower():
            button.pack(pady=10, fill=tk.X)
        else:
            button.pack_forget()
            hide_image_tooltip(None)  # Hides tooltip if button is hidden

def show_image_tooltip(event, plane_tail):
    global image_tooltip
    # Gets the image from maintenance_page
    image = maintenance_page[plane_tail]['image']
    # Creates a Toplevel window
    image_tooltip = tk.Toplevel()
    image_tooltip.wm_overrideredirect(True)  # Removes window decorations
    image_tooltip.wm_geometry("+%d+%d" % (event.x_root + 20, event.y_root + 20))
    # Creates a label in the Toplevel to show the image
    label = tk.Label(image_tooltip, image=image)
    label.pack()

def hide_image_tooltip(event):
    global image_tooltip
    if image_tooltip:
        image_tooltip.destroy()
        image_tooltip = None

# Creates the main menu window
root = tk.Tk()
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

# Configure records_frame to expand
root.rowconfigure(1, weight=1)

# Start the Tkinter event loop
root.mainloop()
