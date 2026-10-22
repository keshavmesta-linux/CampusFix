CampusFix 🏫

A Flask-based campus issue reporting and management system.

CampusFix is a web application designed to help students report campus-related issues and track their status. It provides an organized platform for reporting problems and helps administrators manage and respond to submitted reports.

✨ Features

- User Authentication — Registration and login.
- Issue Reporting — Submit campus-related problems.
- Report Management — View and track submitted reports.
- Admin Dashboard — Manage reports and monitor activity.
- Notifications — Keep users informed about updates.
- Database Integration — Store application data.
- Responsive Interface — Web interface for convenient access.

🛠️ Technologies Used

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Templating: Jinja2
- Version Control: Git and GitHub

📁 Project Structure

CampusFix/
├── app/
│   ├── templates/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── __init__.py
│   ├── auth.py
│   ├── reports.py
│   ├── admin.py
│   └── db.py
├── instance/
├── uploads/
├── make_admin.py
├── requirements.txt
├── run.py
└── README.md

🚀 Getting Started

Prerequisites

- Python 3
- pip

Installation

1. Clone the repository:
   
   git clone https://github.com/keshavmesta-linux/CampusFix.git
cd CampusFix

2. Create a virtual environment:
   
   python -m venv .venv

3. Activate it:
   
   Linux / Termux
   
   source .venv/bin/activate

4. Install dependencies:
   
   pip install -r requirements.txt

5. Start the application:
   
   python run.py

Follow the address printed in your terminal to open the application in your browser.

🔐 Security Notes

- Do not commit passwords, secret keys, ".env" files, or private user data.
- Keep local databases and uploaded user files out of public repositories.
- Configure secure session keys and appropriate access controls before deployment.

🎯 Project Objective

The objective of CampusFix is to simplify campus issue reporting, improve communication between students and administrators, and organize issue tracking through a centralized web application.

👨‍💻 Author

Keshav Nagaraj Mesta

GitHub: "@keshavmesta-linux" (https://github.com/keshavmesta-linux)

📄 License

Add a license file if you intend to distribute this project under a specific open-source license.
