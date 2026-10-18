# dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
from session import get_current_user, get_current_role, is_admin, can_edit, logout

def open_dashboard():
    root = tk.Tk()
    root.title("SPS Yönetim Sistemi - Ana Pencere")
    root.geometry("1200x700")
    root.state('zoomed')
    
    user = get_current_user()
    role = get_current_role()
    
    # Menü çubuğu
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # Dosya menüsü
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Dosya", menu=file_menu)
    file_menu.add_command(label="Çıkış", command=lambda: logout_and_exit(root))
    
    # Admin menüsü
    if is_admin():
        admin_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yönetim", menu=admin_menu)
        admin_menu.add_command(label="Kullanıcı Yönetimi", command=lambda: show_info("Kullanıcı Yönetimi"))
        admin_menu.add_command(label="Rol Yönetimi", command=lambda: show_info("Rol Yönetimi"))
    
    # İşlemler menüsü
    if can_edit():
        islem_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="İşlemler", menu=islem_menu)
        islem_menu.add_command(label="Yeni Müşteri", command=lambda: show_info("Yeni Müşteri"))
        islem_menu.add_command(label="Yeni Sipariş", command=lambda: show_info("Yeni Sipariş"))
        islem_menu.add_command(label="Yeni Teklif", command=lambda: show_info("Yeni Teklif"))
    
    # Görüntüle menüsü
    view_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Görüntüle", menu=view_menu)
    view_menu.add_command(label="Müşteriler", command=lambda: show_info("Müşteri Listesi"))
    view_menu.add_command(label="Siparişler", command=lambda: show_info("Sipariş Listesi"))
    view_menu.add_command(label="Cihazlar", command=lambda: show_info("Cihaz Listesi"))
    view_menu.add_command(label="Lisanslar", command=lambda: show_info("Lisans Listesi"))
    
    # Raporlar menüsü
    rapor_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Raporlar", menu=rapor_menu)
    rapor_menu.add_command(label="Aylık Satış", command=lambda: show_info("Aylık Satış Raporu"))
    rapor_menu.add_command(label="Lisans Bitecekler", command=lambda: show_info("Lisansı Bitecekler"))
    
    # Üst bilgi çubuğu
    top_frame = tk.Frame(root, bg="lightgray", height=45)
    top_frame.pack(fill=tk.X)
    top_frame.pack_propagate(False)
    
    user_info = f"Hoş Geldiniz: {user.get('ad_soyad', user.get('kullanici_adi', 'Kullanıcı'))} | Rol: {role.upper()}"
    tk.Label(top_frame, text=user_info, bg="lightgray", font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=15, pady=12)
    
    btn_logout = tk.Button(top_frame, text="Çıkış Yap", command=lambda: logout_and_exit(root),
                           bg="red", fg="white", cursor="hand2")
    btn_logout.pack(side=tk.RIGHT, padx=10, pady=8)
    
    # Ana içerik
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    tk.Label(main_frame, text="SPS Yönetim Sistemine Hoş Geldiniz", 
             font=("Arial", 18, "bold"), fg="darkblue").pack(pady=30)
    
    root.mainloop()

def show_info(message):
    messagebox.showinfo("Bilgi", f"{message} ekranı geliştirme aşamasındadır.")

def logout_and_exit(root):
    if messagebox.askyesno("Çıkış", "Oturumu kapatmak istediğinizden emin misiniz?"):
        logout()
        root.destroy()
        from login import LoginScreen
        new_root = tk.Tk()
        LoginScreen(new_root)
        new_root.mainloop()