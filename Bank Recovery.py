"""
    SC2 Replay Bank Rebuilder
    Author: TheJoe570
    Version: 1.0
    Date: 2024-05-23
    Description: This script provides a GUI application for processing SC2 replay files (.SC2Replay),
                 extracting player and bank data, and rebuilding bank data using the s2repdump tool.
"""

import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import re
import threading

dropped_replay_file_path = None  # Initialize dropped_replay_file_path globally

# Function to process the dropped replay file
def process_file(file_path):
    global dropped_replay_file_path  # Declare dropped_replay_file_path as global
    try:
        # Update status and start the progress bar
        update_status("Processing...")
        start_progress()
        
        # Set the dropped_replay_file_path
        dropped_replay_file_path = file_path
        
        # Extract players and banks information and update the display
        replay_data = extract_players_and_banks(file_path)
        update_display(replay_data)
        
        # Rebuild bank with user-selected output directory
        rebuild_bank(file_path)
        
        # Update status to success
        update_status("Success")
        
        # Inform the user that the operation is successful
        messagebox.showinfo("Success", "Bank data rebuilt successfully.")
    except Exception as e:
        # Show error message if any exception occurs
        messagebox.showerror("Error", str(e))
        update_status("Error")
    finally:
        # Stop the progress bar
        stop_progress()

def extract_players_and_banks(replay_file_path):
    # Run the s2repdump command to extract players and banks information
    command = f"s2repdump -d players -d banks {replay_file_path}"
    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    
    # Parse the result
    replay_data = parse_s2repdump_output(result.stdout)
    return replay_data

def parse_s2repdump_output(output):
    replay_data = {
        'players': [],
        'banks': []
    }
    
    # Extract player information
    players_section = re.search(r"## PLAYERS\n\n(.*?)(##|$)", output, re.DOTALL)
    if players_section:
        players_data = players_section.group(1).strip().split('\n')[3:]  # Skip headers
        for player in players_data:
            columns = re.split(r'\s*\|\s*', player.strip('|'))
            if len(columns) >= 8:
                player_info = {
                    'name': columns[3],
                    'handle': columns[6]
                }
                replay_data['players'].append(player_info)
    
    # Extract bank information
    banks_section = re.search(r"## BANKS\n\n(.*?)(##|$)", output, re.DOTALL)
    if banks_section:
        banks_data = banks_section.group(1).strip().split('\n')[3:]  # Skip headers
        for bank in banks_data:
            columns = re.split(r'\s*\|\s*', bank.strip('|'))
            if len(columns) >= 9:
                bank_info = {
                    'player': columns[1],
                    'name': columns[2],
                    'uid': columns[3]
                }
                replay_data['banks'].append(bank_info)
    
    return replay_data

def rebuild_bank(replay_file_path):
    # Ask the user to choose the output directory
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    
    # Check if the user canceled the dialog
    if not output_dir:
        return
    
    # Run the s2repdump command to rebuild the bank file with the chosen output directory
    command = f"s2repdump --bank-rebuild --out {output_dir} {replay_file_path}"
    subprocess.run(command, shell=True, check=True)

def update_display(replay_data):
    # Clear the existing content
    text_display.delete(1.0, tk.END)
    
    # Add player information to the display
    if 'players' in replay_data:
        text_display.insert(tk.END, "## PLAYERS\n\n")
        for player in replay_data['players']:
            text_display.insert(tk.END, f"Name: {player.get('name')}, Handle: {player.get('handle')}\n")
        text_display.insert(tk.END, "\n")
    
    # Add bank information to the display
    if 'banks' in replay_data:
        text_display.insert(tk.END, "## BANKS\n\n")
        for bank in replay_data['banks']:
            text_display.insert(tk.END, f"Player: {bank.get('player')}, Name: {bank.get('name')}, UID: {bank.get('uid')}\n")
        text_display.insert(tk.END, "\n")

# Function to handle file drop
def drop(event):
    file_path = event.data
    # Start processing the file in a new thread
    threading.Thread(target=process_file, args=(file_path,)).start()

# Function to start progress bar
def start_progress():
    progress.start()

# Function to stop progress bar
def stop_progress():
    progress.stop()

# Function to update status label
def update_status(message):
    status_label.config(text=message)

# Function to rebuild bank with a specific output directory
def rebuild_bank_with_output_dir(output_dir, replay_file_path):
    # Run the s2repdump command to rebuild the bank file with the chosen output directory
    command = f"s2repdump --bank-rebuild --out {output_dir} {replay_file_path}"
    subprocess.run(command, shell=True, check=True)

# Function to handle the "Save Banks" button click
def save_banks():
    try:
        # Check if a replay file has been dropped
        if not dropped_replay_file_path:
            messagebox.showwarning("No Replay File", "Please drop a .SC2Replay file first.")
            return
        
        # Ask the user to choose the output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        
        # Check if the user canceled the dialog
        if not output_dir:
            return
        
        # Rebuild bank with the selected output directory
        rebuild_bank_with_output_dir(output_dir, dropped_replay_file_path)
        
        # Inform the user that the operation is successful
        messagebox.showinfo("Success", "Banks saved successfully.")
    except Exception as e:
        # Show error message if any exception occurs
        messagebox.showerror("Error", str(e))


# Create the main window
root = TkinterDnD.Tk()
root.geometry('600x400')
root.configure(bg='black')  # Set background color to black
root.wm_title("SC2 Replay Bank Rebuilder")  # Set window title
root.wm_attributes("-topmost", 1)  # Make the window stay on top


# Change the title bar color
root.tk_setPalette(background='#008000', foreground='black') 

# Create a frame for drag and drop area
frame = tk.Frame(root, width=580, height=180, relief=tk.RAISED, borderwidth=1, bg='black')
frame.pack(pady=10)

# Add a label to the frame
label = tk.Label(frame, text="Drop your .SC2Replay file here", bg="black", fg="green", font=("Helvetica", 12, "bold"))
label.pack(fill=tk.BOTH, expand=True)

# Create a text widget to display the replay data
text_display = tk.Text(root, height=15, width=70, bg='black', fg='green', insertbackground='green')
text_display.pack(pady=10)
text_display.config(insertbackground='green')

# Create a frame for the status and progress bar
status_frame = tk.Frame(root, bg='green')
status_frame.pack(fill=tk.X, padx=10, pady=10)

# Create a status label
status_label = tk.Label(status_frame, text="Ready", anchor="w", bg='black', fg='green')
status_label.pack(side=tk.LEFT)

# Create a progress bar
progress = ttk.Progressbar(status_frame, orient="horizontal", mode="indeterminate", style='green.Horizontal.TProgressbar',)
progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

# Create a "Save Banks" button
save_button = tk.Button(root, text="Save Banks", command=save_banks, bg="green", fg="black")
save_button.pack(pady=10)

# Set up drag-and-drop functionality
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

# Custom styling for the progress bar
style = ttk.Style()
style.theme_use('clam')
style.configure('green.Horizontal.TProgressbar', foreground='green', background='black')

root.mainloop()
