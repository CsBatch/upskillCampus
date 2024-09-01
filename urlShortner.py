import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import random
import string
import pyperclip

def generate_short_url(length=6):
    """Generates a random string of specified length"""
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def shorten_url(original_url):
    """Shortens a URL and stores it in the database"""
    
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="urlshortner"
    )
    mycursor = mydb.cursor()

    # Check if original URL already exists (optional)
    sql = "SELECT * FROM accounts WHERE original_url = %s"
    val = (original_url,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        # Return existing short URL if found (optional)
        return result[2]

    # Generate a short URL
    short_url = generate_short_url()

    # Check if short URL already exists
    sql = "SELECT * FROM accounts WHERE short_url = %s"
    val = (short_url,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    # Regenerate short URL if necessary
    while result:
        short_url = generate_short_url()
        sql = "SELECT * FROM accounts WHERE short_url = %s"
        val = (short_url,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()

    # Insert the URL and short URL into the database
    sql = "INSERT INTO accounts (original_url, short_url) VALUES (%s, %s)"
    val = (original_url, short_url)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print("Original Url = ", original_url)
        print("Short Url = ", short_url)
    except mysql.connector.Error as err:
        print("Error inserting data:", err)

    mydb.close()
    return short_url

def expand_url(short_url):
    """Expands a shortened URL"""
    # Connect to the database
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="urlshortner"
    )
    mycursor = mydb.cursor()

    sql = "SELECT original_url FROM accounts WHERE short_url = %s"
    val = (short_url,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return result[0]
    else:
        return "URL not found"

def create_gui():
    root = tk.Tk()
    root.title("URL Shortener")

    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Tab for shortening URL
    shorten_tab = ttk.Frame(notebook)
    notebook.add(shorten_tab, text="Shorten URL")

    # Tab for history
    history_tab = ttk.Frame(notebook)
    notebook.add(history_tab, text="History")
    
    def shorten_button_click():
        original_url = original_url_entry.get()
        if original_url != "":
            short_url = shorten_url(original_url)
            shortened_url_label.config(text=f"Shortened URL: {short_url}")
        
    def copy_url():
        print("In Copy url")
        selected_index = history_listbox.curselection()
        if selected_index:
            short_url = url_history[selected_index[0]]
            try:
                pyperclip.copy(short_url)
                messagebox.showinfo("Copied", "Short URL copied to clipboard")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy to clipboard: {e}")

    # Populate shorten_tab with content
    original_url_label = ttk.Label(shorten_tab, text="Your URL:")
    original_url_entry = ttk.Entry(shorten_tab, width=50)
    shorten_button = ttk.Button(shorten_tab, text="Shorten", command=shorten_button_click)
    shortened_url_label = ttk.Label(shorten_tab, text="")
    copy_button = ttk.Button(shorten_tab, text="Copy", command=copy_url)

    # Grid layout within shorten_tab
    original_url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    original_url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    shorten_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")
    shortened_url_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")
    copy_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    # Populate find_tab with content
    # ... (code for find tab)

    # Populate history_tab with content
    url_history = []
    history_listbox = tk.Listbox(history_tab)
    history_listbox.pack(expand=True, fill="both", padx=5, pady=5)

    # def expand_button_click():
    #     short_url = short_url_entry.get()
    #     original_url = expand_url(short_url)
    #     original_url_label.config(text=f"Original URL: {original_url}")

    def load_history():
        # Fetch data from database
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="password",
            database="urlshortner")
        mycursor = mydb.cursor()
        sql = "SELECT original_url, short_url FROM accounts"  # Adjust columns as needed
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mydb.close()

        # Populate url_history list
        url_history.clear()
        for row in results:
            url_history.append((row[0], row[1]))

        # Update listbox
        history_listbox.delete(0, tk.END)
        for url_data in url_history:
            history_listbox.insert(tk.END, f"{url_data[1]} -> {url_data[0]}")

    # Call load_history initially
    load_history()

    

    root.mainloop()

if __name__ == "__main__":
    create_gui()