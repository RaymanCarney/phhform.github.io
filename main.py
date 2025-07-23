import customtkinter as ctk
from tkinter import messagebox
import csv
from datetime import datetime
from flask import Flask

# Now you can create a Flask application instance
app = Flask(__name__)

# Define routes and other Flask application logic here
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

def check_in():
    guest_name = entry_name.get()
    reason_for_visit = entry_visit.get()
    who_meeting = entry_who_meeting.get()

    if not guest_name or not reason_for_visit or not who_meeting:
        messagebox.showerror("Error", "Please enter all fields.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("check_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([guest_name, reason_for_visit, who_meeting, timestamp, "Check In", ""])
    
    messagebox.showinfo("Success", f"{guest_name} checked in at {timestamp}")
    clear_fields()

    # entry_name = ctk.CTkEntry(root, font=("Arial", 14))  # Change font to Arial, size 14
    # entry_time = ctk.CTkEntry(root, font=("Arial", 14))  # Change font to Arial, size 14
    # entry_visit = ctk.CTkEntry(root, font=("Arial", 14))  # Change font to Arial, size 14
    # entry_who_meeting = ctk.CTkEntry(root, font=("Arial", 14))  # Change font to Arial, size 14

def check_out():
    guest_name = entry_name.get()
    if not guest_name:
        messagebox.showerror("Error", "Please enter Guest Name for check out.")
        return

    rows = []
    found = False
    with open("check_log.csv", "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    for i in range(len(rows) - 1, -1, -1):
        if rows[i][0] == guest_name and rows[i][4] == "Check In" and not rows[i][5]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rows[i][5] = timestamp
            rows[i][4] = "Check Out"
            found = True
            break

    if found:
        with open("check_log.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        messagebox.showinfo("Success", f"Guest {guest_name} checked out.")
    else:
        messagebox.showerror("Error", "No active check-in found for this Guest.")
    
    clear_fields()

def clear_fields():
    entry_name.delete(0, ctk.END)
    entry_visit.delete(0, ctk.END)
    entry_who_meeting.delete(0, ctk.END)

# GUI Setup
ctk.set_appearance_mode("light")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Change the theme color

root = ctk.CTk()  # Use CustomTkinter's CTk class
root.title("Guest Check-in/out")
root.geometry("850x800")  # Set a fixed size for the window

# Configure grid
root.grid_rowconfigure(0, weight=0)  # Header row, doesn't expand
root.grid_rowconfigure(1, weight=1)  # Form frame row, expands
root.grid_rowconfigure(4, weight=0)  # Button row, doesn't expand
for j in range(2):
    root.grid_columnconfigure(j, weight=1)

# Form Frame
form_frame = ctk.CTkFrame(root, corner_radius=10)
form_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
for i in range(5):  # total rows in form_frame
    form_frame.grid_rowconfigure(i, weight=1)
form_frame.grid_columnconfigure(0, weight=1)
form_frame.grid_columnconfigure(1, weight=1)

# Header
header = ctk.CTkLabel(root, text="Guest Check-in/out", font=("Arial", 18, "bold"))
header.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")

# Labels and Entry Fields
label_font = ("Arial", 14, "bold")
entry_font = ("Arial", 14)

ctk.CTkLabel(form_frame, text="Guest Name:", font=label_font).grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
entry_name = ctk.CTkEntry(form_frame, font=entry_font, corner_radius=8)
entry_name.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

ctk.CTkLabel(form_frame, text="Reason for Visit:", font=label_font).grid(row=1, column=0, padx=(10, 5), pady=10, sticky="nsew")
entry_visit = ctk.CTkEntry(form_frame, font=entry_font, corner_radius=8)
entry_visit.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

ctk.CTkLabel(form_frame, text="Who Meeting:", font=label_font).grid(row=2, column=0, padx=(10, 5), pady=10, sticky="nsew")
entry_who_meeting = ctk.CTkEntry(form_frame, font=entry_font, corner_radius=8)
entry_who_meeting.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")

# Buttons
button_font = ("Arial", 14, "bold")
btn_check_in = ctk.CTkButton(form_frame, text="Check In", command=check_in, font=button_font, corner_radius=8)
btn_check_in.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

btn_check_out = ctk.CTkButton(form_frame, text="Check Out", command=check_out, font=button_font, corner_radius=8)
btn_check_out.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

root.mainloop()