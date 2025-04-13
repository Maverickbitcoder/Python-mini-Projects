# 📇 Contact Manager

A simple Python-based Contact Manager that allows users to **add**, **view**, **search**, **update**, and **delete** contact information using a command-line interface. All contacts are stored persistently in a CSV file.

---

## 🔧 Features

- **Add Contact**: Save new contacts with details like name, phone, and email.
- **View All Contacts**: Display all stored contacts in a neat tabular format.
- **Search Contact**: Find contacts by name (supports partial matches).
- **Update Contact**: Modify phone or email of existing contacts.
- **Delete Contact**: Remove a contact by name.
- **CSV Storage**: Data is stored in a `contacts.csv` file so that contacts persist between sessions.

---

## 📁 Project Structure
📦 Contact Manager Project
┣ 📜 Contact manager.py    ← Main Python script
┗ 📜 contacts.csv           ← Auto-generated CSV file for data storage

---

## ▶️ How It Works

1. When the script starts, it checks for `contacts.csv`. If missing, it creates one with the correct headers.
2. A menu is displayed with options:
   - Add Contact
   - View Contacts
   - Search Contact
   - Update Contact
   - Delete Contact
   - Exit
3. The user selects an action by entering a number.
4. The script reads/writes to the CSV file accordingly using Python's `csv` module.
5. All data is updated in real-time and stored persistently in `contacts.csv`.

---

## 🛠️ Requirements

- Python 3.x
- No external libraries needed

---

## 🚀 How to Run

1. Download or clone this repository.
2. Make sure `Contact manager.py` is in your working directory.
3. Run the script via terminal:

## 💡 Notes
 1. The program is case-insensitive when searching, updating, or deleting.
 2. All contacts are saved as plain text in a CSV file.
 3. Designed for beginners learning Python and file handling.	
	

    
