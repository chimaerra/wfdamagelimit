import os
import time
import tkinter as tk
from tkinter import scrolledtext
import threading
import tailer
import re

LOG_FOLDER = os.path.join(os.getenv('localappdata'), "Warframe")
LOG_FILE = "EE.log"
SEARCH_STRING = "Damage too high:"
IGNORE_STRINGS = ["after illumination", "(was:"]
THRESHOLD = 230_472_904_798_633_984

def extract_number(line):
    match = re.search(r'Damage too high: ([\d,]+)', line)
    if match:
        # Remove commas and convert to integer
        return int(match.group(1).replace(',', ''))
    return None

def follow_file(file_path, text_widget):
    for line in tailer.follow(open(file_path)):
        if SEARCH_STRING in line and all(ignore_str not in line for ignore_str in IGNORE_STRINGS):
            number = extract_number(line)
            if number and number > THRESHOLD:
                text_widget.insert(tk.END, f"Damage: {number:,}\n")
                text_widget.see(tk.END)

def main():
    file_path = os.path.join(LOG_FOLDER, LOG_FILE)
    
    root = tk.Tk()
    root.title("High Damage Monitor")
    root.attributes('-topmost', True)

    text_widget = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10)

    follow_file_thread = threading.Thread(target=follow_file, args=(file_path, text_widget), daemon=True)
    follow_file_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()