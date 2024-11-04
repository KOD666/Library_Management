import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author, status="Available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = status

class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        return sum(ord(c) for c in key) % self.size
    
    def insert(self, key, value):
        hash_key = self._hash(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                item[1] = value
                return
        self.table[hash_key].append([key, value])
    
    def get(self, key):
        hash_key = self._hash(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                return item[1]
        return None

    def get_all_values(self):
        return [item[1] for bucket in self.table for item in bucket]

class LibraryManagementSystem:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Library System")
        self.books = HashTable()
        
        self.create_gui()
        self.load_sample_data()
    
    def create_gui(self):
       
        self.books_tree = ttk.Treeview(self.window, columns=("ID", "Title", "Author", "Status"), show="headings")
        for col in ["ID", "Title", "Author", "Status"]:
            self.books_tree.heading(col, text=col)
        self.books_tree.pack(pady=10)
        

        ttk.Button(self.window, text="Add Book", command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.window, text="Issue Book", command=self.issue_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.window, text="Return Book", command=self.return_book).pack(side=tk.LEFT, padx=5)
    
    def load_sample_data(self):
        # static entry of books
        sample_books = [
            Book("B001", "Book1", "George"),
            Book("B002", "Book2", "Michael"),
            Book("B003", "Book3", "Sarah")
        ]
        
        for book in sample_books:
            self.books.insert(book.book_id, book)
        self.refresh_books_list()
    
    def refresh_books_list(self):
        # method refreshes the displayed list of books by clearing the old entries and adding the latest ones
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        for book in self.books.get_all_values():
            self.books_tree.insert("", tk.END, values=(book.book_id, book.title, book.author, book.status))
    
    def add_book(self):
        new_book = Book("B004", "New Book", "Author")
        self.books.insert(new_book.book_id, new_book)
        self.refresh_books_list()
        messagebox.showinfo("Success", "Book added!")

    def issue_book(self):
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a book!")
            return
        book_id = self.books_tree.item(selected[0])["values"][0]
        book = self.books.get(book_id)
        if book and book.status == "Available":
            book.status = "Issued"
            self.refresh_books_list()
            messagebox.showinfo("Success", "Book issued!")
    
    def return_book(self):
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a book!")
            return
        book_id = self.books_tree.item(selected[0])["values"][0]
        book = self.books.get(book_id)
        if book and book.status == "Issued":
            book.status = "Available"
            self.refresh_books_list()
            messagebox.showinfo("Success", "Book returned!")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = LibraryManagementSystem()
    app.run()
