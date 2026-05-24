Dwello is a desktop real estate application built with Python, PostgreSQL, and Tkinter. The application allows users to create accounts, explore Lagos properties based on region and budget, save properties to their cart, and manage their personalized property selections.

---

# Features

- User Registration & Login
- Secure Password Hashing
- Persistent User Sessions
- Lagos Mainland & Island Filtering
- Budget-Based Property Search
- Dynamic Property Marketplace
- Property Image Display
- Saved Properties Cart System
- PostgreSQL Database Integration
- Modern CustomTkinter Interface

---

# Technologies Used

- Python
- PostgreSQL
- Tkinter
- Psycopg2
- Pillow
- Bcrypt

---

# Project Structure

```text
dwello/
│
├── main.py
│
├── database/
│   ├── db_connection.py
│   ├── db_auth.py
│   ├── db_properties.py
│   ├── schema.sql
│
├── controllers/
│   ├── auth_controller.py
│   ├── property_controller.py
│   ├── cart_controller.py
│
├── ui/
│   ├── auth_screen.py
│   ├── preference_screen.py
│   ├── marketplace_screen.py
│   ├── property_card.py
│   ├── components.py
│
├── utils/
│   ├── validators.py
│   ├── session_manager.py
│   ├── helpers.py
│
├── assets/
│   ├── images/
│   ├── icons/
│
└── requirements.txt
```

---

# Installation Guide

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/dwello.git
```

---

## 2. Navigate Into the Project Folder

```bash
cd dwello
```

---

## 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

---

# Required Libraries

```text
tkinter
psycopg2
pillow
bcrypt
```

---

# PostgreSQL Setup

## 1. Create Database

Open PostgreSQL SQL Shell and run:

```sql
CREATE DATABASE dwello;
```

---

## 2. Connect to Database

```sql
\c dwello
```

---

## 3. Run schema.sql

```sql
\i 'FULL_PATH_TO_PROJECT/database/schema.sql'
```

Example:

```sql
\i 'C:/Projects/dwello/database/schema.sql'
```

---

# Database Tables

## users

Stores:
- user accounts
- emails
- password hashes

---

## properties

Stores:
- property listings
- region information
- prices
- image paths

---

## saved_properties

Stores:
- user saved properties
- cart persistence

---

## sessions

Stores:
- active user sessions
- login activity

---

# Application Workflow

```text
Launch App
    ↓
Authentication Screen
    ↓
User Login / Signup
    ↓
Preference Selection
    ↓
Property Marketplace
    ↓
Save Properties
    ↓
Persistent User Cart
```

---

# Authentication System

The authentication system uses:

- bcrypt password hashing
- PostgreSQL user verification
- session tracking

---

# Property Filtering

Users can filter properties based on:

- Lagos Mainland
- Lagos Island
- Budget range

---

# Cart System

Users can:

- Save properties
- Load saved properties after login
- Remove saved properties

All cart data persists inside PostgreSQL.

---

# Running the Application

Run the application with:

```bash
python main.py
```

---

# Sample Lagos Locations

## Mainland
- Ikeja
- Yaba
- Surulere
- Maryland
- Gbagada

## Island
- Lekki
- Ikoyi
- Victoria Island
- Ajah
- Chevron

---

# Future Improvements

- Property Details Screen
- Advanced Property Search
- Favorite Properties
- Mortgage Calculator
- Admin Dashboard
- Dark Mode
- Property Upload System
- Real-Time Notifications

---

# Team Responsibilities

| Role | Responsibility |
|------|----------------|
| UI/UX Designer | Figma layouts and app design |
| Backend Developer | Database and authentication |
| Frontend Developer | CustomTkinter screens |
| Integration Engineer | UI + database connection |
| Database Engineer | PostgreSQL setup and queries |
| QA Tester | Debugging and testing |

---

# Author

Dwello Development Team, Group 8, COS 102 100 Level CSC.
