# 🎓 Step-by-Step Project Setup Guide

This guide assumes you have **Git**, **Python**, **Node.js**, and **MySQL** already installed on your computer.

---

## 🛑 Step 1: Database Setup (Most Critical Step!)
*Before running any code, we need to set up the database.*

1.  **Open your MySQL Workbench** (or Command Prompt).
2.  Run this exact SQL command to create the empty database:
    ```sql
    CREATE DATABASE el_management_system;
    ```
3.  **Configure the Code to talk to your Database**:
    - Go to the folder: `el_project_backend`
    - Open the file named: `config.py`
    - Look for line 4:
      ```python
      MYSQL_PASSWORD = 'keerthimanne999000@' 
      ```
    - **CHANGE THIS** to **YOUR** actual MySQL password that you set when you installed MySQL.
    - *Save the file.*

---

## 🐍 Step 2: Backend Server Setup (Python)
*This runs the logic and connects to the database.*

1.  Open a **Terminal** (Command Prompt or PowerShell).
2.  Navigate to the backend folder:
    ```bash
    cd el_project_backend
    ```
3.  **Install the required libraries** (copy-paste this):
    ```bash
    pip install -r requirements.txt
    ```
    *(If that fails, try `pip3 install -r requirements.txt`)*

4.  **Populate the Database with Data**:
    *Run this once to fill your empty database with tables and users.*
    ```bash
    python populate_test_data.py
    ```

5.  **Start the Server**:
    ```bash
    python run.py
    ```
    ✅ **Success?** You should see a message saying `Running on http://127.0.0.1:5000`.
    *Leave this terminal window OPEN.*

---

## ⚛️ Step 3: Frontend Setup (React Website)
*This runs the visual website you interact with.*

1.  Open a **NEW SECOND Terminal** window.
2.  Navigate to the frontend folder:
    ```bash
    cd el-management-frontend
    ```
3.  **Install the libraries** (this might take a few minutes):
    ```bash
    npm install
    ```
4.  **Start the Website**:
    ```bash
    npm start
    ```
    ✅ **Success?** A browser window should automatically open at `http://localhost:3000`.

---

## 🔑 Login Credentials (for Testing)
Once everything is running, use these details to log in:

- **Admin Login**:
  - Email: `admin@rvce.edu.in`
  - Password: `123456`

- **Student Login (Example)**:
  - Email: `keerthii.is23@rvce.edu.in`
  - Password: `123456`
