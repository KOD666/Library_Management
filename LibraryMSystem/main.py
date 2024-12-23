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
    
    # def _hash(self, key):
    #     return hash(key) % self.size
    
    def _hash(self, key):
        if isinstance(key, str):
            return sum(ord(c) for c in key) % self.size
        return key % self.size
    
    # Insert data into hash table in key value pair
    def insert(self, key, value):
        Count_Key = self._hash(key)
        for item in self.table[Count_Key]:
            if item[0] == key:
                messagebox.showerror("Error", "Book ID already exists!")
                return
        self.table[Count_Key].append([key, value])
    # Get data from hash table using key
    def get(self, key):
        Count_Key = self._hash(key)
        for item in self.table[Count_Key]:
            if item[0] == key:
                return item[1]
        messagebox.showerror("Error", "Book not found!")
        return None
    # Delete data from hash table using key
    def delete(self, key):
        Count_Key = self._hash(key)
        table_list = self.table[Count_Key]
        for i in range(len(table_list)):
            if table_list[i][0] == key:
                del table_list[i]
                return True
        return False
    # Get all values from hash table
    def get_all_values(self):
        all_values = []
        for table_list in self.table:
            for item in table_list:
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
        
        ttk.Button(btn_frame, text="Add Book", command=self.show_add_book_dialog_box).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Issue Book", command=self.show_issue_book_dialog_box).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Return Book", command=self.show_return_book_dialog_box).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Book", command=self.show_delete_book_dialog_box).pack(side=tk.LEFT, padx=5)
        
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
    
    def show_add_book_dialog_box(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Add New Book")
        dialog.geometry("300x250")
        
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Book ID:").pack(pady=5)
        book_id_entry = ttk.Entry(main_frame)
        book_id_entry.pack(fill=tk.X)
        
        ttk.Label(main_frame, text="Title:").pack(pady=5)
        title_entry = ttk.Entry(main_frame)
        title_entry.pack(fill=tk.X)
        
        ttk.Label(main_frame, text="Author:").pack(pady=5)
        author_entry = ttk.Entry(main_frame)
        author_entry.pack(fill=tk.X)
        
        def add_book():
            book_id = book_id_entry.get()
            title = title_entry.get()
            author = author_entry.get()
            
            if not book_id or not title or not author:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            
            new_book = Book(book_id, title, author)
            self.books.insert(book_id, new_book)
            self.refresh_books_list()
            dialog.destroy()
            messagebox.showinfo("Success", "Book added successfully!")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20, fill=tk.X)
        
        add_button = ttk.Button(button_frame, text="Add Book", command=add_book)
        add_button.pack(expand=True)
    
    def show_issue_book_dialog_box(self):
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
        
        # When You Issue A Book Then it auto sets the due date after 14 days to just display
        def issue_book():
            member_id = member_id_entry.get()
            if not member_id:
                messagebox.showerror("Error", "Please enter member ID!")
                return
            
            book.status = "Issued"
            book.borrower = member_id
            book.due_date = datetime.now() + timedelta(days=14)
            self.refresh_books_list()
            dialog.destroy()
            messagebox.showinfo("Success", "Book issued successfully!")
        
        ttk.Button(dialog, text="Issue Book", command=issue_book).pack(pady=20)
    
    def show_return_book_dialog_box(self):
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
    
    def show_delete_book_dialog_box(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Delete Book")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Book ID:").pack(pady=5)
        book_id_entry = ttk.Entry(dialog)
        book_id_entry.pack()
        
        def delete_book():
            book_id = book_id_entry.get()
            if not book_id:
                messagebox.showerror("Error", "Please enter book ID!")
                return
            
            if self.books.delete(book_id):
                self.refresh_books_list()
                messagebox.showinfo("Success", "Book deleted successfully!")
            else:
                messagebox.showerror("Error", "Book not found!")
            dialog.destroy()
        
        ttk.Button(dialog, text="Delete Book", command=delete_book).pack(pady=20)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = LibraryManagementSystem()
    app.run()