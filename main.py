# main.py
import tkinter as tk
from login import LoginScreen
from database import test_connection

if __name__ == "__main__":
    if not test_connection():
        print("Veritabanı bağlantısı kurulamadı!")
        input("Devam etmek için Enter'a basın...")
        exit()
    
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()