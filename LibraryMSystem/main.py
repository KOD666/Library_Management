import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author, status="Available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = status
        self.borrower = None
        self.due_date = None

class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    # Simple hash function for string/integer keys converts string keys to sum of ASCII values or uses numeric keys directly, then applies modulo with table size
    def _hash(self, key):
        if isinstance(key, str):
            return sum(ord(c) for c in key) % self.size
        return key % self.size
    # Insert data into hash table in key value pair
    def insert(self, key, value):
        hash_key = self._hash(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                item[1] = value
                return
        self.table[hash_key].append([key, value])
    # Get data from hash table using key
    def get(self, key):
        hash_key = self._hash(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                return item[1]
        return None
    # Delete data from hash table using key
    def delete(self, key):
        hash_key = self._hash(key)
        for i, item in enumerate(self.table[hash_key]):
            if item[0] == key:
                del self.table[hash_key][i]
                return True
        return False
    # Get all values from hash table
    def get_all_values(self):
        all_values = []
        for bucket in self.table:
            for item in bucket:
                all_values.append(item[1])
        return all_values

class LibraryManagementSystem:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Library Management System")
        self.window.geometry("800x600")
        
        # Initialize hash tables for books and members
        self.books = HashTable()
        self.members = HashTable()
        
        self.create_gui()
        self.load_sample_data()
    
    def create_gui(self):
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(pady=10, expand=True)
        
        
        books_frame = ttk.Frame(notebook)
        notebook.add(books_frame, text="Books")
        
        
        search_frame = ttk.Frame(books_frame)
        search_frame.pack(pady=10, padx=10)
        
        ttk.Label(search_frame, text="Search Book ID:").pack(side=tk.LEFT)
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        def search_book():
            book_id = search_entry.get()
            book = self.books.get(book_id)
            if book:
                messagebox.showinfo("Search Result", f"Book Found: {book.title} by {book.author}")
            else:
                messagebox.showerror("Search Result", "No book found with that ID.")
        
        ttk.Button(search_frame, text="Search", command=search_book).pack(side=tk.LEFT)
        
        
        self.books_tree = ttk.Treeview(books_frame, columns=("ID", "Title", "Author", "Status", "Borrower", "Due Date"), show="headings")
        self.books_tree.heading("ID", text="ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("Status", text="Status")
        self.books_tree.heading("Borrower", text="Borrower")
        self.books_tree.heading("Due Date", text="Due Date")
        self.books_tree.pack(pady=10, padx=10)
        
        # Book management buttons
        btn_frame = ttk.Frame(books_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add Book", command=self.show_add_book_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Issue Book", command=self.show_issue_book_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Return Book", command=self.show_return_book_dialog).pack(side=tk.LEFT, padx=5)
        
    def load_sample_data(self):
        # Adding sample books
        sample_books = [
            Book("B001", "Book 1", "Author 1"),
            Book("B002", "Book 2", "Author 2"), 
            Book("B003", "Book 3", "Author 3")
        ]
        
        for book in sample_books:
            self.books.insert(book.book_id, book)
        
        self.refresh_books_list()
    
    def refresh_books_list(self):
        # Clear current items
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        # Add all books to the treeview
        for book in self.books.get_all_values():
            due_date = book.due_date.strftime("%Y-%m-%d") if book.due_date else ""
            self.books_tree.insert("", tk.END, values=(
                book.book_id,
                book.title,
                book.author,
                book.status,
                book.borrower or "",
                due_date
            ))
    
    def show_add_book_dialog(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Add New Book")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Book ID:").pack(pady=5)
        book_id_entry = ttk.Entry(dialog)
        book_id_entry.pack()
        
        ttk.Label(dialog, text="Title:").pack(pady=5)
        title_entry = ttk.Entry(dialog)
        title_entry.pack()
        
        ttk.Label(dialog, text="Author:").pack(pady=5)
        author_entry = ttk.Entry(dialog)
        author_entry.pack()
        
        def add_book():
            book_id = book_id_entry.get()
            title = title_entry.get()
            author = author_entry.get()
            
            if book_id and title and author:
                new_book = Book(book_id, title, author)
                self.books.insert(book_id, new_book)
                self.refresh_books_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Book added successfully!")
            else:
                messagebox.showerror("Error", "Please fill in all fields!")
        
        ttk.Button(dialog, text="Add Book", command=add_book).pack(pady=20)
    
    def show_issue_book_dialog(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to issue!")
            return
        
        book_id = self.books_tree.item(selected_item[0])["values"][0]
        book = self.books.get(book_id)
        
        if book.status != "Available":
            messagebox.showerror("Error", "Book is not available!")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Issue Book")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Member ID:").pack(pady=5)
        member_id_entry = ttk.Entry(dialog)
        member_id_entry.pack()
        
        def issue_book():
            member_id = member_id_entry.get()
            if member_id:
                book.status = "Issued"
                book.borrower = member_id
                book.due_date = datetime.now() + timedelta(days=14)
                self.refresh_books_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Book issued successfully!")
            else:
                messagebox.showerror("Error", "Please enter member ID!")
        
        ttk.Button(dialog, text="Issue Book", command=issue_book).pack(pady=20)
    
    def show_return_book_dialog(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to return!")
            return
        
        book_id = self.books_tree.item(selected_item[0])["values"][0]
        book = self.books.get(book_id)
        
        if book.status != "Issued":
            messagebox.showerror("Error", "Book is not issued!")
            return
        
        book.status = "Available"
        book.borrower = None
        book.due_date = None
        self.refresh_books_list()
        messagebox.showinfo("Success", "Book returned successfully!")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = LibraryManagementSystem()
    app.run()

# If You Want You Can Use Either Of The Codes Both are Working Above One Is More Simplified ....

# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import datetime, timedelta

# class Book:
#     def __init__(self, book_id, title, author, status="Available"):
#         self.book_id = book_id
#         self.title = title
#         self.author = author
#         self.status = status

# class HashTable:
#     def __init__(self, size=100):
#         self.size = size
#         self.table = [[] for _ in range(size)]
    
#     def _hash(self, key):
#         return sum(ord(c) for c in key) % self.size
    
#     def insert(self, key, value):
#         hash_key = self._hash(key)
#         for item in self.table[hash_key]:
#             if item[0] == key:
#                 item[1] = value
#                 return
#         self.table[hash_key].append([key, value])
    
#     def get(self, key):
#         hash_key = self._hash(key)
#         for item in self.table[hash_key]:
#             if item[0] == key:
#                 return item[1]
#         return None

#     def get_all_values(self):
#         return [item[1] for bucket in self.table for item in bucket]

# class LibraryManagementSystem:
#     def __init__(self):
#         self.window = tk.Tk()
#         self.window.title("Library System")
#         self.books = HashTable()
        
#         self.create_gui()
#         self.load_sample_data()
    
#     def create_gui(self):
       
#         self.books_tree = ttk.Treeview(self.window, columns=("ID", "Title", "Author", "Status"), show="headings")
#         for col in ["ID", "Title", "Author", "Status"]:
#             self.books_tree.heading(col, text=col)
#         self.books_tree.pack(pady=10)
        

#         ttk.Button(self.window, text="Add Book", command=self.add_book).pack(side=tk.LEFT, padx=5)
#         ttk.Button(self.window, text="Issue Book", command=self.issue_book).pack(side=tk.LEFT, padx=5)
#         ttk.Button(self.window, text="Return Book", command=self.return_book).pack(side=tk.LEFT, padx=5)
    
#     def load_sample_data(self):
#         # static entry of books
#         sample_books = [
#             Book("B001", "Book1", "George"),
#             Book("B002", "Book2", "Michael"),
#             Book("B003", "Book3", "Sarah")
#         ]
        
#         for book in sample_books:
#             self.books.insert(book.book_id, book)
#         self.refresh_books_list()
    
#     def refresh_books_list(self):
#         # method refreshes the displayed list of books by clearing the old entries and adding the latest ones
#         for item in self.books_tree.get_children():
#             self.books_tree.delete(item)
#         for book in self.books.get_all_values():
#             self.books_tree.insert("", tk.END, values=(book.book_id, book.title, book.author, book.status))
    
#     def add_book(self):
#         new_book = Book("B004", "New Book", "Author")
#         self.books.insert(new_book.book_id, new_book)
#         self.refresh_books_list()
#         messagebox.showinfo("Success", "Book added!")

#     def issue_book(self):
#         selected = self.books_tree.selection()
#         if not selected:
#             messagebox.showerror("Error", "Select a book!")
#             return
#         book_id = self.books_tree.item(selected[0])["values"][0]
#         book = self.books.get(book_id)
#         if book and book.status == "Available":
#             book.status = "Issued"
#             self.refresh_books_list()
#             messagebox.showinfo("Success", "Book issued!")
    
#     def return_book(self):
#         selected = self.books_tree.selection()
#         if not selected:
#             messagebox.showerror("Error", "Select a book!")
#             return
#         book_id = self.books_tree.item(selected[0])["values"][0]
#         book = self.books.get(book_id)
#         if book and book.status == "Issued":
#             book.status = "Available"
#             self.refresh_books_list()
#             messagebox.showinfo("Success", "Book returned!")
    
#     def run(self):
#         self.window.mainloop()

# if __name__ == "__main__":
#     app = LibraryManagementSystem()
#     app.run()
