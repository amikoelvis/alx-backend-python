# 📦 Python Generators: Streaming SQL Data

## 🧠 Objective

Build a Python script that:

- Connects to a MySQL server
- Creates a database `ALX_prodev` and a table `user_data` if they don't exist
- Inserts data from a CSV file (`user_data.csv`)
- Prepares for generator-based streaming of rows

This is **Project 0** in the advanced Python generators series.

---

## 📁 Project Structure

.
├── 0-main.py # Test script to drive seeding logic
├── seed.py # Main logic for DB creation and data seeding
├── user_data.csv # Input data (name, email, age)
└── README.md # This documentation

---

## 🛠️ Setup Instructions

1. **Install MySQL** if not already installed.

2. **Install Python MySQL Connector:**

```bash
pip install mysql-connector-python
```

3. Update **seed.py** Credentials:
   Modify:

```python
user="root",
password="your_password"
```

to match your local MySQL configuration.

4. Prepare **user_data.csv:**

Ensure it follows this format:

```csv
name,email,age
Alice Smith,alice@example.com,28
Bob Johnson,bob@example.com,32
```

5. **Run Main Script:**

```bash
chmod +x seed.py
./seed.py
```

**You should see:**

```css
connection successful
Table user_data created successfully
Database ALX_prodev is present
[('uuid1', 'Alice Smith', 'alice@example.com', 28), ...]
```

---

## 🧪 Functions Overview

**connect_db()**
Connects to the MySQL server (no database selected).

**create_database(connection)**
Creates the ALX_prodev database if not present.

**connect_to_prodev()**
Connects to the ALX_prodev database.

**create_table(connection)**
Creates user_data table if it doesn’t exist.

**insert_data(connection, data)**
Inserts rows from CSV into the table (avoids duplicates).
