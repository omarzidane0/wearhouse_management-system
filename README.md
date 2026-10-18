# 📦 Warehouse Management System

A web-based Warehouse Management System built with **Django** and **Django Templates**, designed to streamline warehouse operations, manage inventory, and organize access for different user roles.

## 📌 About the Project

The Warehouse Management System aims to simplify warehouse operations through a centralized web application with authentication and role-based access for different types of users.

The system is currently in its **final stages of development**, with final improvements and refinements underway.

## ✨ Key Features

- **Authentication System** — A complete login system for authorized users.
- **Role-Based Access Control** — Different access levels for administrators, regular users, drivers, and other supported roles.
- **Admin Management** — Dedicated access for administrators to manage the system.
- **User Management** — Support for different user types and their respective permissions.
- **Warehouse Operations** — A centralized platform for warehouse-related activities.
- **Django Templates** — Server-rendered web pages using Django's template engine.

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Django Templates
- **Database:** Depends on the project's configured database
- **Authentication:** Django authentication and role-based access

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/omarzidane0/wearhouse_management-system.git
```

### 2. Navigate to the Project Directory

```bash
cd wearhouse_management-system
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

If the project includes a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open the following URL in your browser:

```text
http://127.0.0.1:8000/
```

> **Note:** Run the commands from the directory containing `manage.py`. Additional configuration may be required depending on the project's structure and environment variables.

## 👥 User Roles

The system supports different user roles, including:

| Role | Description |
|---|---|
| Admin | Administrative access to the system |
| User | Access to features permitted for regular users |
| Driver | Access to driver-related functionality |

*Specific permissions and available functionality depend on the project's implementation.*

## 🎯 Project Objectives

- Centralize warehouse-related operations.
- Provide secure authentication for different user types.
- Organize access according to user roles.
- Build a maintainable web application using Django.
- Improve the efficiency of warehouse management workflows.

## 🚧 Development Status

**Status:** In Progress — Final Stage

The core application and authentication system have been developed. The project is currently undergoing final improvements and refinements.

## 👨‍💻 Author

**Omar Zeidan**

GitHub: [@omarzidane0](https://github.com/omarzidane0)

