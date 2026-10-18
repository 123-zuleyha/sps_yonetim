# login.py
import tkinter as tk
from tkinter import messagebox
from database import check_user
from session import set_current_user
import dashboard

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("SPS Yönetim Sistemi - Giriş")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
        # Ortalamak için frame
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True)
        
        # Logo/Başlık
        title_label = tk.Label(main_frame, text="SPS YÖNETİM SİSTEMİ", 
                                font=("Arial", 18, "bold"), fg="darkblue")
        title_label.grid(row=0, column=0, columnspan=2, pady=30)
        
        # Email (kullanıcı adı olarak)
        tk.Label(main_frame, text="E-posta:", font=("Arial", 11)).grid(row=1, column=0, 
                                                                        sticky="e", pady=12, padx=5)
        self.entry_user = tk.Entry(main_frame, width=30, font=("Arial", 11))
        self.entry_user.grid(row=1, column=1, pady=12, padx=5)
        
        # Şifre
        tk.Label(main_frame, text="Şifre:", font=("Arial", 11)).grid(row=2, column=0, 
                                                                      sticky="e", pady=12, padx=5)
        self.entry_pass = tk.Entry(main_frame, width=30, font=("Arial", 11), show="*")
        self.entry_pass.grid(row=2, column=1, pady=12, padx=5)
        
        # Giriş butonu
        self.btn_login = tk.Button(main_frame, text="Giriş Yap", command=self.login,
                                    bg="#2ecc71", fg="white", font=("Arial", 11, "bold"),
                                    width=25, height=1, cursor="hand2")
        self.btn_login.grid(row=3, column=0, columnspan=2, pady=25)
        
        # Hata mesajı
        self.lbl_error = tk.Label(main_frame, text="", fg="red", font=("Arial", 9))
        self.lbl_error.grid(row=4, column=0, columnspan=2)
        
        # Enter tuşu ile giriş
        self.entry_pass.bind("<Return>", lambda event: self.login())
        self.entry_user.bind("<Return>", lambda event: self.login())
        
        # İmleci email alanına odakla
        self.entry_user.focus()
    
    def login(self):
        email = self.entry_user.get().strip()
        password = self.entry_pass.get()
        
        if not email or not password:
            self.lbl_error.config(text="E-posta ve şifre giriniz!")
            return
        
        self.btn_login.config(state="disabled", text="Giriş yapılıyor...")
        
        user = check_user(email, password)
        
        if user:
            set_current_user(user)
            self.root.destroy()
            dashboard.open_dashboard()
        else:
            self.lbl_error.config(text="Hatalı e-posta veya şifre!")
            self.entry_pass.delete(0, tk.END)
            self.entry_user.focus()
            self.btn_login.config(state="normal", text="Giriş Yap")