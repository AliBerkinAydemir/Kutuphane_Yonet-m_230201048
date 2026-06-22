import sqlite3
from datetime import datetime

# Veritabanı ve tabloların Oluşturulma Kısmı
def db_baslat():
    db = sqlite3.connect("library.db")
    isaret = db.cursor()  # Noktadan sonrası orijinal kütüphane fonksiyonu olmalı
    
    # Kitaplar Tablosu
    isaret.execute("create table if not exists books (id integer primary key autoincrement, kitap_adı text not null, yazar text not null, kitap_no text unique not null, is_available integer default 1)")
    
    # Üye Tabloları
    isaret.execute("create table if not exists members (id integer primary key autoincrement, name text not null, email text unique not null)")
    
    # Ödünç Alma Tablosu
    isaret.execute("create table if not exists transactions (id integer primary key autoincrement, book_id integer, member_id integer, borrow_date text not null, return_date text, foreign key (book_id) references books (id), foreign key (member_id) references members (id))")
    
    db.commit()
    db.close()

# *** KİTAP İŞLEMLERİ ***
def kitap_ekle(kitap_adı, yazar, kitap_no):
    try:
        db = sqlite3.connect("library.db")
        isaret = db.cursor()
        isaret.execute("INSERT INTO books (kitap_adı, yazar, kitap_no) VALUES (?, ?, ?)", (kitap_adı, yazar, kitap_no))
        db.commit()
        print(f"\n[BAŞARILI] '{kitap_adı}' kitabı başarıyla eklendi :) ")
    except sqlite3.IntegrityError:
        print("\n[HATA] Bu KITAP_NO numarasıyla zaten bir kitap kayıtlı :( )")
    finally:
        db.close()

def kitaplari_listele():
    db = sqlite3.connect("library.db")
    isaret = db.cursor()
    isaret.execute("SELECT id, kitap_adı, yazar, kitap_no, is_available FROM books")
    books = isaret.fetchall()
    db.close()
    
    if not books:
        print("\nKütüphanede henüz kitap yok :( )")
        return
    
    print("\n*** KITAP LISTESI ***")
    for b in books:
        durum = "Mevcut" if b[4] == 1 else "Ödünç Verildi :)"
        print(f"ID: {b[0]} | İsim: {b[1]} | Yazar: {b[2]} | KITAP_NO: {b[3]} | Durum: {durum}")

def kitap_sil(book_id):
    db = sqlite3.connect("library.db")
    isaret = db.cursor()
    isaret.execute("DELETE FROM books WHERE id = ?", (book_id,))
    if isaret.rowcount > 0:
        print(f"\n[BAŞARILI] ID'si {book_id} olan kitap silindi :) ")
    else:
        print("\n[HATA] Bu ID'ye sahip bir kitap bulunamadı :( )")
    db.commit()
    db.close()

# *** ÜYE İŞLEMLERİ ***
def uye_ekle(name, email):
    try:
        db = sqlite3.connect("library.db")
        isaret = db.cursor()
        isaret.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
        db.commit()
        print(f"\n[BAŞARILI] '{name}' isimli üye başarıyla kaydedildi :) ")
    except sqlite3.IntegrityError:
        print("\n[HATA] Bu e-posta adresiyle zaten bir üye kayıtlı!")
    finally:
        db.close()

def uyeleri_goster():
    db = sqlite3.connect("library.db")
    isaret = db.cursor()
    isaret.execute("SELECT id, name, email FROM members")
    members = isaret.fetchall()
    db.close()
    
    if not members:
        print("\nSistemde kayıtlı üye yok :( )")
        return
    
    print("\n*** UYE LISTESI ***")
    for m in members:
        print(f"ID: {m[0]} | İsim: {m[1]} | E-posta: {m[2]}")

# *** ÖDÜNÇ ALMA & İADE İSLEMLERİ ***
def odunc_ver(book_id, member_id):
    db = sqlite3.connect("library.db")
    isaret = db.cursor()
    
    # Kitap kontrolü
    isaret.execute("SELECT is_available FROM books WHERE id = ?", (book_id,))
    res = isaret.fetchone()
    
    if res is None:
        print("\n[HATA] Kitap bulunamadı :( )")
        db.close()
        return
    if res[0] == 0:
        print("\n[HATA] Bu kitap zaten ödünç verilmiş :( )")
        db.close()
        return
        
    # İşlemi kaydet
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    isaret.execute("INSERT INTO transactions (book_id, member_id, borrow_date) VALUES (?, ?, ?)", (book_id, member_id, tarih))
    isaret.execute("UPDATE books SET is_available = 0 WHERE id = ?", (book_id,))
    
    db.commit()
    db.close()
    print("\n[BAŞARILI] Kitap başarıyla ödünç verildi :)")

def iade_al(book_id):
    db = sqlite3.connect("library.db")
    isaret = db.cursor()
    
    isaret.execute("SELECT id FROM transactions WHERE book_id = ? AND return_date IS NULL", (book_id,))
    t_id = isaret.fetchone()
    
    if t_id is None:
        print("\n[HATA] Bu kitaba ait aktif bir ödünç alma işlemi bulunamadı :( )")
        db.close()
        return
        
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    isaret.execute("UPDATE transactions SET return_date = ? WHERE id = ?", (tarih, t_id[0]))
    isaret.execute("UPDATE books SET is_available = 1 WHERE id = ?", (book_id,))
    
    db.commit()
    db.close()
    print("\n[BAŞARILI] Kitap başarıyla iade alındı :)")
