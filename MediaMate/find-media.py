#!/Users/izno/.pyenv/shims/python3
import tkinter as tk
from tkinter import scrolledtext
import subprocess

def search_media():
    media_name = entry.get()
    if media_name.strip():  # Check if the input is not just spaces
        # Construct the grep command to search the cache file without filename prefix
        command = f"grep --no-filename -i -h '{media_name.strip()}' $HOME/.medias_cache"
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        # Display the results in the scrolled text area
        text_area.delete(1.0, tk.END)  # Clear previous results
        text_area.insert(tk.END, result.stdout if result.stdout else "No results found.")

def on_enter(event):
    search_media()

# Create the main window
root = tk.Tk()
root.title("Media Finder")

# Create a label
label = tk.Label(root, text="Enter the name of the media folder:")
label.pack(pady=10)

# Create an entry widget
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Bind the Enter key to the search function
entry.bind('<Return>', on_enter)

# Create a search button
search_button = tk.Button(root, text="Search", command=search_media)
search_button.pack(pady=10)

# Create a scrolled text area
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
text_area.pack(pady=10)

# Start the GUI event loop
root.mainloop()
