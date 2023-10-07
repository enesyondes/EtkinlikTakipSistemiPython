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
        self.uye_ekle_btn = tk.Button(self.pencere, text="Üye Ekle", command=self.uye_ekle_sayfasi, font=("Arial", 18), width=20, background="green")
        self.rozet_sirala_btn = tk.Button(self.pencere, text="Rozet İşlemleri", command=self.rozet_siralama_sayfasi, font=("Arial", 18), width=20, background="green")
        self.cikis_btn = tk.Button(self.pencere, text="Çıkış", command=self.pencere.quit, font=("Arial", 18), width=20, background="red")
        
        self.uye_ekle_btn.pack(pady=20)
        self.rozet_sirala_btn.pack(pady=20)
        self.cikis_btn.pack(pady=20)

    def temizle(self):
        for widget in self.pencere.winfo_children():
            widget.destroy()
            
    def uye_ekle_sayfasi(self):
        self.temizle()
        
        # Üye Ekle sayfa başlık
        baslik = tk.Label(self.pencere, text="Üye Ekle", font=("Arial", 24), fg="green")
        baslik.pack(pady=10)
        
        # Geri Dön butonu
        geri_btn = tk.Button(self.pencere, text="Ana Sayfa", command=self.ana_sayfa, font=("Arial", 14))
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

        self.arama_btn = tk.Button(self.pencere, text="Ara", command=self.arama_yap, font=("Arial", 16))
        self.arama_btn.pack(pady=10)
        
        self.rozet_arttir_btn = tk.Button(self.pencere, text="Seçilen Üyenin Rozetini Arttır", command=self.rozet_arttir, font=("Arial", 16))
        self.rozet_arttir_btn.pack(pady=5)

        self.rozet_azalt_btn = tk.Button(self.pencere, text="Seçilen Üyenin Rozetini Azalt", command=self.rozet_azalt, font=("Arial", 16))
        self.rozet_azalt_btn.pack(pady=5)

        sil_btn = tk.Button(self.pencere, text="Seçilen Üyeyi Sil", command=self.sil_uye, font=("Arial", 16))
        sil_btn.pack(pady=5)  # Ana Sayfa butonunun altına

        self.guncelle_liste()

    def rozet_arttir(self):
        secili_uye = self.siralama_listesi.get(tk.ACTIVE)
        tam_isim = secili_uye.split('-')[0].split('.')[-1][1:].split()
        
        isim = " ".join(tam_isim[:-1])
        soyisim =tam_isim[-1]

        ##isim ve soyisimi kullanarak sql_query ile uyeler tablosunda rozet arttirma islemi yapilir
        sql_query = """
            UPDATE uyeler
            SET rozet = rozet + 1
            WHERE (isim = ?)
            AND (soyisim = ?);
        """
        self.cursor.execute(sql_query, (isim,soyisim))
        self.baglanti.commit()
        self.guncelle_liste()
    
    def rozet_azalt(self):
        secili_uye = self.siralama_listesi.get(tk.ACTIVE)
        tam_isim = secili_uye.split('-')[0].split('.')[-1][1:].split()
        
        isim = " ".join(tam_isim[:-1])
        soyisim =tam_isim[-1]

        ##isim ve soyisimi kullanarak sql_query ile uyeler tablosunda rozet arttirma islemi yapilir
        sql_query = """
            UPDATE uyeler
            SET rozet = rozet - 1
            WHERE (isim = ?)
            AND (soyisim = ?);
        """
        self.cursor.execute(sql_query, (isim,soyisim))
        self.baglanti.commit()
        self.guncelle_liste()

    def sil_uye(self):
        secili_uye = self.siralama_listesi.get(tk.ACTIVE)
        tam_isim = secili_uye.split('-')[0].split('.')[-1][1:].split()
        
        isim = " ".join(tam_isim[:-1])
        soyisim =tam_isim[-1]

        ##isim ve soyisimi kullanarak sql_query ile uyeler tablosundan silme islemi yapilir
        sql_query = """
            DELETE FROM uyeler
            WHERE (isim = ?)
            AND (soyisim = ?);
        """
        self.cursor.execute(sql_query, (isim,soyisim))
        self.baglanti.commit()
        self.guncelle_liste()
        return
    def arama_yap(self):
        tam_isim = (self.arama_isim_entry.get()).split()
        
        if len(tam_isim) == 0:
            self.guncelle_liste()
            return

        isim = tam_isim[0]
        soyisim = "" if len(tam_isim) == 1 else " ".join(tam_isim[1:])  # Yalnizca isim olma durumunda soyisim empty string olarak birakilir

        if soyisim == "":
        
            # soyisimin olmamasi durumunda yalnizca isim arayacak olan sql sorgusu
            sql_query = """
                SELECT isim, soyisim, rozet FROM uyeler
                WHERE (isim LIKE ?)
            """
            self.cursor.execute(sql_query, ("%"+isim+"%",))
        
        else:
            # isim ve soyisimi arayacak olan sql sorgusu
            sql_query = """
                SELECT isim, soyisim, rozet FROM uyeler
                WHERE (isim LIKE ? OR soyisim LIKE ?);
            """
            
            self.cursor.execute(sql_query, ("%"+isim+"%", "%"+soyisim+"%"))

        results = self.cursor.fetchall()
        self.siralama_listesi.delete(0, tk.END)

        if results:
            for sira, (isim, soyisim, rozet) in enumerate(results, start=1):
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
                
                #uye olusturduktan sonra girdileri temizle
                self.isim_entry.delete(0, tk.END)
                self.soyisim_entry.delete(0, tk.END)
                self.okul_no_entry.delete(0, tk.END)
                self.sinif_entry.delete(0, tk.END)

if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = Uygulama(pencere)
    pencere.geometry("700x700")
    # Pencereyi resizable (yeniden boyutlandırılabilir) yapmayın
    pencere.resizable(False, False)
    pencere.mainloop()