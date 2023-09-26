import tkinter as tk
import sqlite3
from tkinter import messagebox

class Uygulama:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Rozet Sistemi Uygulaması")
        self.pencere.geometry("800x600")
        
        self.baglanti = sqlite3.connect("rozetler.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS uyeler (
                id INTEGER PRIMARY KEY,
                isim TEXT,
                soyisim TEXT,
                okul_no TEXT,
                sinif TEXT,
                rozet INTEGER DEFAULT 0
            )
        """)
        self.baglanti.commit()

        self.ana_sayfa()

    def ana_sayfa(self):
        self.temizle()
        
        # Ana sayfa başlık
        baslik = tk.Label(self.pencere, text="Rozet Sistemi", font=("Arial", 36), fg="black")
        baslik.pack(pady=20)
        
        # Üye İşlemleri, Rozet İşlemleri ve Rozet Sıralaması butonları
        self.uye_islemleri_btn = tk.Button(self.pencere, text="Üye İşlemleri", command=self.uye_islemleri_sayfasi, font=("Arial", 18), width=20, background="green")
        self.rozet_islemleri_btn = tk.Button(self.pencere, text="Rozet İşlemleri", command=self.rozet_islemleri_sayfasi, font=("Arial", 18), width=20, background="green")
        self.rozet_sirala_btn = tk.Button(self.pencere, text="Rozet Sıralaması", command=self.rozet_siralama_sayfasi, font=("Arial", 18), width=20, background="yellow")
        self.cikis_btn = tk.Button(self.pencere, text="Çıkış", command=self.pencere.quit, font=("Arial", 18), width=20, background="red")
        
        self.uye_islemleri_btn.pack(pady=20)
        self.rozet_islemleri_btn.pack(pady=20)
        self.rozet_sirala_btn.pack(pady=20)
        self.cikis_btn.pack(pady=20)

    def temizle(self):
        for widget in self.pencere.winfo_children():
            widget.destroy()

    def uye_islemleri_sayfasi(self):
        self.temizle()
        
        # Üye İşlemleri sayfa başlık
        baslik = tk.Label(self.pencere, text="Üye İşlemleri", font=("Arial", 24), fg="green")
        baslik.pack(pady=10)
        
        # Geri Dön butonu
        geri_btn = tk.Button(self.pencere, text="Ana Sayfa", command=self.ana_sayfa, font=("Arial", 14))
        geri_btn.pack(anchor="nw", padx=10, pady=10)
        
        uye_ekle_btn = tk.Button(self.pencere, text="Üye Ekle", command=self.uye_ekle_sayfasi, font=("Arial", 18), width=20)
        uye_sil_btn = tk.Button(self.pencere, text="Üye Sil", command=self.uye_sil_sayfasi, font=("Arial", 18), width=20)
        
        uye_ekle_btn.pack(pady=20)
        uye_sil_btn.pack(pady=20)

    def rozet_islemleri_sayfasi(self):
        self.temizle()
        
        # Rozet İşlemleri sayfa başlık
        baslik = tk.Label(self.pencere, text="Rozet İşlemleri", font=("Arial", 24), fg="black")
        baslik.pack(pady=10)
        
        # Geri Dön butonu
        geri_btn = tk.Button(self.pencere, text="Ana Sayfa", command=self.ana_sayfa, font=("Arial", 14))
        geri_btn.pack(anchor="nw", padx=10, pady=10)
        
        rozet_sayfasi = RozetIslemleriSayfasi(self.pencere, self.baglanti, self.cursor)
        rozet_sayfasi.olustur()

    def uye_ekle_sayfasi(self):
        self.temizle()
        
        # Üye Ekle sayfa başlık
        baslik = tk.Label(self.pencere, text="Üye Ekle", font=("Arial", 24), fg="green")
        baslik.pack(pady=10)
        
        # Geri Dön butonu
        geri_btn = tk.Button(self.pencere, text="Üye İşlemleri", command=self.uye_islemleri_sayfasi, font=("Arial", 14))
        geri_btn.pack(anchor="nw", padx=10, pady=10)
        
        uye_ekleme_formu = UyeEklemeFormu(self.pencere, self.baglanti, self.cursor)

    def uye_sil_sayfasi(self):
        self.temizle()
        
        # Üye Sil sayfa başlık
        baslik = tk.Label(self.pencere, text="Üye Sil", font=("Arial", 24), fg="green")
        baslik.pack(pady=10)
        
        # Geri Dön butonu
        geri_btn = tk.Button(self.pencere, text="Üye İşlemleri", command=self.uye_islemleri_sayfasi, font=("Arial", 14))
        geri_btn.pack(anchor="nw", padx=10, pady=10)
        
        uye_silme_formu = UyeSilmeFormu(self.pencere, self.baglanti, self.cursor)

    def rozet_siralama_sayfasi(self):
        self.temizle()

        # Rozet Sıralama sayfa başlık
        baslik = tk.Label(self.pencere, text="Rozet Sıralaması", font=("Arial", 24), fg="black")
        baslik.pack(pady=10)

        # Geri Dön butonu
        geri_btn = tk.Button(self.pencere, text="Ana Sayfa", command=self.ana_sayfa, font=("Arial", 14))
        geri_btn.pack(anchor="nw", padx=10, pady=10)

        # Rozet Sıralama işlemleri
        self.siralama_listesi = tk.Listbox(self.pencere, height=15, width=50, font=("Arial", 12))
        self.siralama_listesi.pack()

        self.arama_isim_label = tk.Label(self.pencere, text="İsim:", font=("Arial", 16))
        self.arama_isim_label.pack()
        self.arama_isim_entry = tk.Entry(self.pencere, font=("Arial", 16))
        self.arama_isim_entry.pack()
        self.arama_soyisim_label = tk.Label(self.pencere, text="Soyisim:", font=("Arial", 16))
        self.arama_soyisim_label.pack()
        self.arama_soyisim_entry = tk.Entry(self.pencere, font=("Arial", 16))
        self.arama_soyisim_entry.pack()
        self.arama_btn = tk.Button(self.pencere, text="Ara", command=self.arama_yap, font=("Arial", 16))
        self.arama_btn.pack()

        self.guncelle_liste()

    def arama_yap(self):
        isim = self.arama_isim_entry.get()
        soyisim = self.arama_soyisim_entry.get()

        self.cursor.execute("SELECT isim, soyisim, rozet FROM uyeler WHERE isim = ? AND soyisim = ?", (isim, soyisim))
        sonuc = self.cursor.fetchall()
        self.siralama_listesi.delete(0, tk.END)

        if sonuc:
            for sira, (isim, soyisim, rozet) in enumerate(sonuc, start=1):
                self.siralama_listesi.insert(tk.END, f"{sira}. {isim} {soyisim} - Rozet: {rozet}")
        else:
            self.siralama_listesi.insert(tk.END, "Üye bulunamadı.")

    def guncelle_liste(self):
        sira_liste = self.rozet_sirala()
        self.siralama_listesi.delete(0, tk.END)

        for sira, (isim, soyisim, rozet) in enumerate(sira_liste, start=1):
            self.siralama_listesi.insert(tk.END, f"{sira}. {isim} {soyisim} - Rozet: {rozet}")

    def rozet_sirala(self):
        # Rozet sıralamasını almak için bir sorgu çalıştırın
        self.cursor.execute("SELECT isim, soyisim, rozet FROM uyeler ORDER BY rozet DESC")
        sira_liste = self.cursor.fetchall()
        return sira_liste

class UyeEklemeFormu:
    def __init__(self, pencere, baglanti, cursor):
        self.pencere = pencere
        self.baglanti = baglanti
        self.cursor = cursor
        self.olustur()

    def olustur(self):
        self.isim_label = tk.Label(self.pencere, text="İsim:", font=("Arial", 18))
        self.isim_entry = tk.Entry(self.pencere, font=("Arial", 18))
        self.soyisim_label = tk.Label(self.pencere, text="Soyisim:", font=("Arial", 18))
        self.soyisim_entry = tk.Entry(self.pencere, font=("Arial", 18))
        self.okul_no_label = tk.Label(self.pencere, text="Okul Numarası:", font=("Arial", 18))
        self.okul_no_entry = tk.Entry(self.pencere, font=("Arial", 18))
        self.sinif_label = tk.Label(self.pencere, text="Sınıf:", font=("Arial", 18))
        self.sinif_entry = tk.Entry(self.pencere, font=("Arial", 18))
        self.kaydet_btn = tk.Button(self.pencere, text="Kaydet", command=self.uye_kaydet, font=("Arial", 18), width=20)

        self.isim_label.pack()
        self.isim_entry.pack()
        self.soyisim_label.pack()
        self.soyisim_entry.pack()
        self.okul_no_label.pack()
        self.okul_no_entry.pack()
        self.sinif_label.pack()
        self.sinif_entry.pack()
        self.kaydet_btn.pack()

    def uye_kaydet(self):
        isim = self.isim_entry.get()
        soyisim = self.soyisim_entry.get()
        okul_no = self.okul_no_entry.get()
        sinif = self.sinif_entry.get()

        # Boş alan kontrolü
        if not isim or not soyisim or not okul_no or not sinif:
            messagebox.showwarning("Boş Alanlar", "Lütfen tüm alanları doldurun.")
        else:
            # Aynı okul numarasına sahip üyenin olup olmadığını kontrol et
            self.cursor.execute("SELECT * FROM uyeler WHERE okul_no = ?", (okul_no,))
            existing_member = self.cursor.fetchone()
            if existing_member:
                messagebox.showerror("Hata", "Bu okul numarasına sahip bir üye zaten var.")
            else:
                self.cursor.execute("INSERT INTO uyeler (isim, soyisim, okul_no, sinif) VALUES (?, ?, ?, ?)",
                                    (isim, soyisim, okul_no, sinif))
                self.baglanti.commit()
                self.pencere.title("Üye Kaydedildi")

class UyeSilmeFormu:
    def __init__(self, pencere, baglanti, cursor):
        self.pencere = pencere
        self.baglanti = baglanti
        self.cursor = cursor
        self.olustur()

    def olustur(self):
        self.isim_label = tk.Label(self.pencere, text="İsim:", font=("Arial", 18))
        self.isim_entry = tk.Entry(self.pencere, font=("Arial", 18))
        self.soyisim_label = tk.Label(self.pencere, text="Soyisim:", font=("Arial", 18))
        self.soyisim_entry = tk.Entry(self.pencere, font=("Arial", 18))
        self.ara_btn = tk.Button(self.pencere, text="Ara", command=self.uye_ara, font=("Arial", 18), width=20)

        self.bilgi_label = tk.Label(self.pencere, text="Üye Bilgileri:", font=("Arial", 18))
        self.bilgi_text = tk.Text(self.pencere, height=5, width=40, state="disabled", font=("Arial", 14))

        self.sil_btn = tk.Button(self.pencere, text="Üye Sil", command=self.uye_sil, font=("Arial", 18), width=20)

        self.isim_label.pack()
        self.isim_entry.pack()
        self.soyisim_label.pack()
        self.soyisim_entry.pack()
        self.ara_btn.pack()
        self.bilgi_label.pack()
        self.bilgi_text.pack()
        self.sil_btn.pack()

    def uye_ara(self):
        isim = self.isim_entry.get()
        soyisim = self.soyisim_entry.get()

        self.cursor.execute("SELECT * FROM uyeler WHERE isim = ? AND soyisim = ?", (isim, soyisim))
        sonuc = self.cursor.fetchone()

        if sonuc:
            id, isim, soyisim, okul_numarasi, sinif, rozet = sonuc
            bilgi = f"ID: {id}\nİsim: {isim}\nSoyisim: {soyisim}\nOkul Numarası: {okul_numarasi}\nSınıf: {sinif}\nRozet: {rozet}"
            self.bilgi_text.config(state="normal")
            self.bilgi_text.delete(1.0, "end")
            self.bilgi_text.insert("insert", bilgi)
            self.bilgi_text.config(state="disabled")
        else:
            self.bilgi_text.config(state="normal")
            self.bilgi_text.delete(1.0, "end")
            self.bilgi_text.insert("insert", "Üye bulunamadı.")
            self.bilgi_text.config(state="disabled")

    def uye_sil(self):
        isim = self.isim_entry.get()
        soyisim = self.soyisim_entry.get()

        self.cursor.execute("DELETE FROM uyeler WHERE isim = ? AND soyisim = ?", (isim, soyisim))
        self.baglanti.commit()
        self.pencere.title("Üye Silindi")

class RozetIslemleriSayfasi:
    def __init__(self, pencere, baglanti, cursor):
        self.pencere = pencere
        self.baglanti = baglanti
        self.cursor = cursor

    def olustur(self):
        self.okul_no_label = tk.Label(self.pencere, text="Okul Numarası:", font=("Arial", 18))
        self.okul_no_kutusu = tk.Entry(self.pencere, font=("Arial", 18))
        self.bilgi_goster_btn = tk.Button(self.pencere, text="Bilgi Göster", command=self.bilgi_goster, font=("Arial", 18), width=20)
        self.rozet_artir_btn = tk.Button(self.pencere, text="Rozet Artır", command=self.rozet_artir, font=("Arial", 18), width=20)
        self.rozet_azalt_btn = tk.Button(self.pencere, text="Rozet Azalt", command=self.rozet_azalt, font=("Arial", 18), width=20)
        self.bilgi_label = tk.Label(self.pencere, text="", font=("Arial", 18))

        self.okul_no_label.pack()
        self.okul_no_kutusu.pack()
        self.bilgi_goster_btn.pack()
        self.rozet_artir_btn.pack()
        self.rozet_azalt_btn.pack()
        self.bilgi_label.pack()

    def bilgi_goster(self):
        okul_no = self.okul_no_kutusu.get()

        self.cursor.execute("SELECT isim, soyisim, okul_no, sinif, rozet FROM uyeler WHERE okul_no = ?", (okul_no,))
        sonuc = self.cursor.fetchone()

        if sonuc:
            isim, soyisim, okul_numarasi, sinif, rozet = sonuc
            bilgi = f"İsim: {isim}\nSoyisim: {soyisim}\nOkul Numarası: {okul_numarasi}\nSınıf: {sinif}\nRozet: {rozet}"
            self.bilgi_label.config(text=bilgi)
        else:
            self.bilgi_label.config(text="Kişi bulunamadı.")


    def rozet_artir(self):
        okul_no = self.okul_no_kutusu.get()

        self.cursor.execute("UPDATE uyeler SET rozet = rozet + 1 WHERE okul_no = ?", (okul_no,))
        self.baglanti.commit()
        self.bilgi_goster()

    def rozet_azalt(self):
        okul_no = self.okul_no_kutusu.get()

        self.cursor.execute("UPDATE uyeler SET rozet = rozet - 1 WHERE okul_no = ?", (okul_no,))
        self.baglanti.commit()
        self.bilgi_goster()


if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = Uygulama(pencere)
    pencere.mainloop()
