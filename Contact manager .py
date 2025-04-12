import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager Pro")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # Initialize variables
        self.current_contact = None
        self.search_text = tk.StringVar()

        # Setup UI
        self.create_widgets()
        self.init_db()
        self.load_contacts()

        # Bind search
        self.search_text.trace_add("write", self.search_contacts)

    def configure_styles(self):
        self.style.configure("TButton", padding=6, font=('Arial', 10))
        self.style.configure("Header.TLabel", font=('Arial', 16, 'bold'), foreground='#2c3e50')
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        self.style.map("Treeview", background=[('selected', '#3498db')])

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search bar
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search:", style="Header.TLabel").pack(side=tk.LEFT)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_text, width=40)
        search_entry.pack(side=tk.LEFT, padx=10)
        search_entry.focus()
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Add Contact", command=self.show_add_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        self.tree = ttk.Treeview(main_frame, columns=("ID", "First", "Last", "Gender", "Age", "Phone", "Email"),
                                 show='headings', selectmode='browse')
        columns = [
            ("ID", 50), ("First", 120), ("Last", 120),
            ("Gender", 80), ("Age", 60), ("Phone", 120), ("Email", 200)
        ]
        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.W)

        # Add scrollbars
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind double click
        self.tree.bind("<Double-1>", self.show_edit_form)

    def init_db(self):
        with sqlite3.connect("contacts.db") as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first TEXT NOT NULL,
                last TEXT NOT NULL,
                gender TEXT,
                age INTEGER,
                phone TEXT,
                email TEXT)""")

    def load_contacts(self, query=None):
        self.tree.delete(*self.tree.get_children())
        with sqlite3.connect("contacts.db") as conn:
            cursor = conn.cursor()
            base_query = "SELECT id, first, last, gender, age, phone, email FROM contacts"
            params = ()

            if query:
                base_query += " WHERE first LIKE ? OR last LIKE ? OR phone LIKE ?"
                params = (f"%{query}%", f"%{query}%", f"%{query}%")

            cursor.execute(base_query + " ORDER BY last, first", params)
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)

    def search_contacts(self, *args):
        query = self.search_text.get().strip()
        self.load_contacts(query if len(query) > 1 else None)

    def validate_contact(self, data):
        errors = []
        if not data['first']:
            errors.append("First name is required")
        if not data['last']:
            errors.append("Last name is required")
        if data['age'] and not data['age'].isdigit():
            errors.append("Age must be a number")
        if data['phone'] and (not data['phone'].isdigit() or len(data['phone']) < 10):
            errors.append("Invalid phone number")
        return errors

    def save_contact(self, form, data, is_edit=False):
        errors = self.validate_contact(data)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        with sqlite3.connect("contacts.db") as conn:
            cursor = conn.cursor()
            contact_data = (
                data['first'], data['last'], data['gender'],
                int(data['age']) if data['age'] else None,
                data['phone'], data['email']
            )

            if is_edit:
                cursor.execute("""UPDATE contacts SET 
                    first=?, last=?, gender=?, age=?, phone=?, email=?
                    WHERE id=?""", contact_data + (self.current_contact,))
            else:
                cursor.execute("""INSERT INTO contacts 
                    (first, last, gender, age, phone, email)
                    VALUES (?, ?, ?, ?, ?, ?)""", contact_data)

        form.destroy()
        self.load_contacts()
        messagebox.showinfo("Success", "Contact saved successfully!")

    def show_contact_form(self, title, data=None):
        # Initialize empty dict if no data provided
        data = data or {}

        form = tk.Toplevel(self.root)
        form.title(title)
        form.geometry("400x450")
        form.grab_set()

        fields = [
            ('first', 'First Name:', True),
            ('last', 'Last Name:', True),
            ('gender', 'Gender:', False),
            ('age', 'Age:', False),
            ('phone', 'Phone:', False),
            ('email', 'Email:', False)
        ]

        entries = {}
        for idx, (field, label, required) in enumerate(fields):
            frame = ttk.Frame(form)
            frame.pack(fill=tk.X, padx=10, pady=5)

            lbl = ttk.Label(frame, text=label, width=12, anchor=tk.W)
            lbl.pack(side=tk.LEFT)

            if field == 'gender':
                var = tk.StringVar(value=data.get('gender', ''))
                male = ttk.Radiobutton(frame, text="Male", variable=var, value="Male")
                female = ttk.Radiobutton(frame, text="Female", variable=var, value="Female")
                male.pack(side=tk.LEFT)
                female.pack(side=tk.LEFT)
            else:
                var = tk.StringVar(value=data.get(field, ''))
                entry = ttk.Entry(frame, textvariable=var)
                entry.pack(fill=tk.X, expand=True)

            entries[field] = var

        btn_frame = ttk.Frame(form)
        btn_frame.pack(fill=tk.X, pady=10)

        save_text = "Save Changes" if data else "Add Contact"
        save_cmd = lambda: self.save_contact(form, {k: v.get().strip() for k, v in entries.items()}, is_edit=bool(data))
        ttk.Button(btn_frame, text=save_text, command=save_cmd).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=form.destroy).pack(side=tk.RIGHT)

    def show_add_form(self):
        self.current_contact = None
        self.show_contact_form("Add New Contact")

    def show_edit_form(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        contact_id = self.tree.item(selected[0])['values'][0]
        with sqlite3.connect("contacts.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
            result = cursor.fetchone()

        if result:
            self.current_contact = contact_id
            data = {
                'first': result[1],
                'last': result[2],
                'gender': result[3],
                'age': str(result[4]) if result[4] else '',
                'phone': result[5],
                'email': result[6]
            }
            self.show_contact_form("Edit Contact", data)

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Delete selected contact permanently?"):
            contact_id = self.tree.item(selected[0])['values'][0]
            with sqlite3.connect("contacts.db") as conn:
                conn.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            self.load_contacts()
            messagebox.showinfo("Success", "Contact deleted successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()