# Quick Mart — Local Setup & Execution Guide

This guide provides end-to-end instructions for setting up and running **Quick Mart** locally on Windows, macOS, or Linux.

---

## 1. Prerequisites

Ensure you have the following installed on your machine:
* **Python**: Version 3.10, 3.11, 3.12, 3.13, or 3.14 (Verified on Python 3.14 & Django 6.1)
* **Git**: Version 2.20 or newer
* **Web Browser**: Chrome, Edge, Firefox, or Safari

---

## 2. Installation Steps (Windows PowerShell)

### Step 1: Clone the Repository
```powershell
git clone https://github.com/vedant24628/quickmart-pos-system.git
cd quickmart-pos-system
```

### Step 2: Create and Activate a Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1
```
*(If you encounter execution policy restrictions on PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### Step 3: Install Required Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy the example environment configuration:
```powershell
Copy-Item .env.example .env
```
*(The default configuration includes fallback development settings so the project runs immediately without manual edits).*

### Step 5: Initialize the Database (Optional / Reset)
The repository includes a pre-seeded `quickmart.db` SQLite database with 86 sample products, 15 bills, and staff demo accounts.

If you ever wish to reset the database to a clean seed state, run:
```powershell
python database/init_db.py
```

### Step 6: Verify System Health
Run Django's built-in system check:
```powershell
python manage.py check
```
*Expected output: `System check identified no issues (0 silenced).`*

### Step 7: Launch the Development Server
```powershell
python manage.py runserver 127.0.0.1:8000
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 3. Demo Staff Credentials

| Role | Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@quickmart.com` | `admin123` | Full Administrative & System Access |
| **Cashier** | `cashier@quickmart.com` | `cashier123` | POS Terminal, Invoicing, Billing History |

---

## 4. Verification Checklist

1. **Login Test**: Sign in using `admin@quickmart.com` / `admin123`.
2. **Dashboard**: Verify that today's revenue, low-stock count, and Chart.js graphs render.
3. **POS Checkout**:
   - Go to **New Bill** (`/billing/new`).
   - Add items to the cart, enter customer name and phone number.
   - Click **Complete Order & Print Bill**.
   - Verify that stock decreases in **Inventory** and the receipt displays.
4. **PDF Invoice**: Click **Download PDF** on any receipt to download the ReportLab vector invoice.

---

## 5. Troubleshooting & FAQ

* **Port 8000 in use**:
  ```powershell
  python manage.py runserver 127.0.0.1:8080
  ```
* **Database Reset**:
  If `quickmart.db` becomes locked or corrupted during testing, run `python database/init_db.py` to restore the original 3NF schema and seed data.
