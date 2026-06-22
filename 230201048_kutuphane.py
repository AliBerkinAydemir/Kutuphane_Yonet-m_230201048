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
