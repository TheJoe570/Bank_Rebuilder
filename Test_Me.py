import os
import logging
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import re
import threading

# Set up logging
logging.basicConfig(filename='sc2_replay_bank_rebuilder.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

dropped_replay_file_path = None  # Initialize dropped_replay_file_path globally

def process_file(file_path):
    global dropped_replay_file_path  # Declare dropped_replay_file_path as global
    try:
        update_status("Processing...")
        start_progress()
        
        dropped_replay_file_path = file_path
        logging.info(f"Processing file: {file_path}")
        
        replay_data = extract_players_and_banks(file_path)
        update_display(replay_data)
        
        rebuild_bank(file_path)
        
        update_status("Success")
        messagebox.showinfo("Success", "Bank data rebuilt successfully.")
    except Exception as e:
        logging.error(f"Error processing file: {file_path}", exc_info=True)
        messagebox.showerror("Error", str(e))
        update_status("Error")
    finally:
        stop_progress()

def extract_players_and_banks(replay_file_path):
    try:
        command = f"s2repdump -d players -d banks {replay_file_path}"
        logging.info(f"Running command: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        replay_data = parse_s2repdump_output(result.stdout)
        return replay_data
    except subprocess.CalledProcessError as e:
        logging.error("s2repdump command failed", exc_info=True)
        raise
    except Exception as e:
        logging.error("Unexpected error in extract_players_and_banks", exc_info=True)
        raise

def parse_s2repdump_output(output):
    try:
        replay_data = {
            'players': [],
            'banks': []
        }
        
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
    except Exception as e:
        logging.error("Error parsing s2repdump output", exc_info=True)
        raise

def rebuild_bank(replay_file_path):
    try:
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        
        if not output_dir:
            logging.info("Output directory selection cancelled.")
            return
        
        command = f"s2repdump --bank-rebuild --out {output_dir} {replay_file_path}"
        logging.info(f"Running command: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error("s2repdump command failed", exc_info=True)
        raise
    except Exception as e:
        logging.error("Unexpected error in rebuild_bank", exc_info=True)
        raise

def update_display(replay_data):
    try:
        text_display.delete(1.0, tk.END)
        
        if 'players' in replay_data:
            text_display.insert(tk.END, "## PLAYERS\n\n")
            for player in replay_data['players']:
                text_display.insert(tk.END, f"Name: {player.get('name')}, Handle: {player.get('handle')}\n")
            text_display.insert(tk.END, "\n")
        
        if 'banks' in replay_data:
            text_display.insert(tk.END, "## BANKS\n\n")
            for bank in replay_data['banks']:
                text_display.insert(tk.END, f"Player: {bank.get('player')}, Name: {bank.get('name')}, UID: {bank.get('uid')}\n")
            text_display.insert(tk.END, "\n")
    except Exception as e:
        logging.error("Error updating display", exc_info=True)
        raise

def drop(event):
    file_path = event.data
    logging.info(f"File dropped: {file_path}")
    threading.Thread(target=process_file, args=(file_path,)).start()

def start_progress():
    progress.start()
    logging.info("Progress bar started.")

def stop_progress():
    progress.stop()
    logging.info("Progress bar stopped.")

def update_status(message):
    status_label.config(text=message)
    logging.info(f"Status updated: {message}")

def rebuild_bank_with_output_dir(output_dir, replay_file_path):
    try:
        command = f"s2repdump --bank-rebuild --out {output_dir} {replay_file_path}"
        logging.info(f"Running command: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error("s2repdump command failed", exc_info=True)
        raise
    except Exception as e:
        logging.error("Unexpected error in rebuild_bank_with_output_dir", exc_info=True)
        raise

def save_banks():
    try:
        if not dropped_replay_file_path:
            messagebox.showwarning("No Replay File", "Please drop a .SC2Replay file first.")
            logging.warning("No replay file dropped.")
            return
        
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        
        if not output_dir:
            logging.info("Output directory selection cancelled.")
            return
        
        rebuild_bank_with_output_dir(output_dir, dropped_replay_file_path)
        messagebox.showinfo("Success", "Banks saved successfully.")
    except Exception as e:
        logging.error("Error saving banks", exc_info=True)
        messagebox.showerror("Error", str(e))

root = TkinterDnD.Tk()
root.geometry('600x400')
root.configure(bg='black')
root.wm_title("SC2 Replay Bank Rebuilder")
root.wm_attributes("-topmost", 1)

root.tk_setPalette(background='#008000', foreground='black')

frame = tk.Frame(root, width=580, height=180, relief=tk.RAISED, borderwidth=1, bg='black')
frame.pack(pady=10)

label = tk.Label(frame, text="Drop your .SC2Replay file here", bg="black", fg="green", font=("Helvetica", 12, "bold"))
label.pack(fill=tk.BOTH, expand=True)

text_display = tk.Text(root, height=15, width=70, bg='black', fg='green', insertbackground='green')
text_display.pack(pady=10)
text_display.config(insertbackground='green')

status_frame = tk.Frame(root, bg='green')
status_frame.pack(fill=tk.X, padx=10, pady=10)

status_label = tk.Label(status_frame, text="Ready", anchor="w", bg='black', fg='green')
status_label.pack(side=tk.LEFT)

progress = ttk.Progressbar(status_frame, orient="horizontal", mode="indeterminate", style='green.Horizontal.TProgressbar',)
progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

save_button = tk.Button(root, text="Save Banks", command=save_banks, bg="green", fg="black")
save_button.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

style = ttk.Style()
style.theme_use('clam')
style.configure('green.Horizontal.TProgressbar', foreground='green', background='black')

root.mainloop()
