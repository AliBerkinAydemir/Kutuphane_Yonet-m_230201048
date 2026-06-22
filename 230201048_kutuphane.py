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
