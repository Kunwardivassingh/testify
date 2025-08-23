# Testify Project

 # Testify: Test Data Analysis & Visualization Platform -->live--> https://testify-tgbi.onrender.com/

**Testify** is a powerful, web-based platform designed for QA engineers, developers, and data analysts to upload, analyze, and visualize test data. It provides a comprehensive suite of tools for both real-time monitoring and in-depth analysis of historical test results, helping teams optimize performance and ensure product quality.

---

## ✨ Core Features

* **Dual Data Modes**: Seamlessly switch between two analysis modes:
    * **Manual Upload**: Upload test data from `.csv` or `.xlsx` files for detailed historical analysis. Each new upload for a user replaces their previous data, keeping the dataset clean.
    * **Real-Time Fetching**: Connect to a live data source (like a published Google Sheet CSV) for continuous, real-time dashboard updates.
* **Interactive Dashboards**: A rich, interactive dashboard built with Plotly and Dash, featuring:
    * Key Performance Indicators (KPIs) for total, passed, failed, and pending tests.
    * Multiple chart types: line charts, pie charts, bar charts, box plots, heatmaps, and more.
    * Dynamic filtering by product, test type, status, and date range, which works in both manual and real-time modes.
* **User Authentication & Management**: A complete user management system with Flask-Login, including:
    * User registration and login.
    * Secure password handling.
    * A functional user profile page to manage personal information and dashboard preferences.
* **Report Management**: A dedicated reports page that lists all uploaded files, showing metadata like upload time, file size, and status, with the ability to delete old reports.
* **Professional UI/UX**: A modern, responsive, dark-themed user interface designed for clarity and ease of use.

---

## 📸 Screenshots

| Dashboard | Reports Page | Profile Settings |
| :---: | :---: | :---: |
| ![Dashboard Screenshot](https://i.imgur.com/your-dashboard-image-url.png) | ![Reports Screenshot](https://i.imgur.com/r6o6i1h.png) | ![Profile Screenshot](https://i.imgur.com/0.jpg) |

---

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Dashboarding**: Plotly, Dash
* **Database**: MySQL
* **ORM**: SQLAlchemy
* **Authentication**: Flask-Login
* **Frontend**: HTML, CSS, JavaScript

---

## 📂 Project Structure

The project follows a modular structure for better organization and scalability.

testify/
├── dashboard/         # Dash app layout and callbacks
│   ├── callbacks.py
│   └── layout.py
├── database/          # Database schema
│   └── schema.sql
├── models/            # SQLAlchemy database models
│   ├── test_data.py
│   ├── test_report.py
│   └── user.py
├── routes/            # Flask blueprints for different routes
│   ├── auth.py
│   ├── reports.py
│   ├── upload.py
│   └── ...
├── static/            # CSS, JS, and image assets
│   └── assets/
├── templates/         # HTML templates
│   ├── dashboard.html
│   ├── reports.html
│   └── ...
├── .env               # Environment variables
├── app.py             # Main Flask application factory
├── config.py          # Application configuration
├── extensions.py      # Flask extension initializations (e.g., db)
└── requirements.txt   # Python dependencies


---

## 🚀 Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Prerequisites

* Python 3.9+
* MySQL Server
* Git

### 2. Clone the Repository

``bash
git clone [https://github.com/your-username/testify.git](https://github.com/your-username/testify.git)
cd testify


3. Set Up a Virtual Environment
It's highly recommended to use a virtual environment.

Bash

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
#  Install Dependencies
Bash

pip install -r requirements.txt
#  Configure the Database
Run the Schema: Use a MySQL client or the command line to execute the schema.sql file. This will create the database and all the necessary tables.

Bash

# For PowerShell
Get-Content database\schema.sql | mysql -u root -p

# For other terminals (Git Bash, macOS, Linux)
mysql -u root -p < database/schema.sql
# Configure Environment Variables
Create a .env file in the root directory of the project.

Copy the contents of .env.example (if provided) or add the following:

SECRET_KEY=your_strong_random_secret_key
DATABASE_URL=mysql+pymysql://root:your_mysql_password@localhost/test_report_db
Replace your_mysql_password with your actual MySQL root password.

# Run the Application
Bash

python app.py
The application will be available at http://127.0.0.1:5000.

# 📖 Usage
Navigate to http://127.0.0.1:5000.

Sign up for a new account.

Log in with your credentials.

You will be directed to the Mode Selection page.

Choose Manual to upload a .csv or .xlsx file.

Choose Real-Time to connect to a live data URL.

Explore the Dashboard, Reports, and Settings pages.

# 🤝 Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

# Fork the repository.

Create your feature branch (git checkout -b feature/amazing-feature).

Commit your changes (git commit -m 'Add some amazing feature').

Push to the branch (git push origin feature/amazing-feature).

Open a Pull Request.

# 📜 License
This project is licensed under the MIT License.

# 📧 Contact
Your Name – kunwardivasingh@gmail.com

Project Link: https://github.com/kunwardivassingh/testify



