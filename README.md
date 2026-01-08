# 🎓 STUDENTS INTERNSHIP AND ATTACHMENTS PLACEMENT SYSTEM

A full-stack web application that simplifies and automates the process of internship and attachment placements by connecting **students**, **companies**, and **institutions** on a single platform.

---

## 📌 Project Overview

Many students struggle to find internship opportunities, while institutions and companies find it difficult to coordinate and manage placement details. This system solves these problems by providing:

* APIs for managing data (Backend)
* A modern frontend UI for interaction (React)

The system helps:

* Students to view and apply for internships
* Companies to post and manage openings
* Institutions to approve and monitor placements

---

## 👥 Target Users

1. **Students** – Register, view opportunities, apply, and track statuses
2. **Companies/Organizations** – Post opportunities and manage applications
3. **Institution Staff (Admin/Coordinator)** – Approve and manage placements

---

## ⚙️ Core Features

### 👨‍🎓 Student Interface

* Student registration and login
* Profile management
* Browse internship/attachment opportunities
* Apply for placements
* Track application status

### 🏢 Company Interface

* Company login/registration
* Create and manage internship listings
* View and manage applicant lists

### 🏫 Institution Admin Interface

* Admin login
* Approve/decline student and company registrations
* Approve internship placements
* View placement reports

---

## 🛠️ Technology Stack

**Backend**

* Django & Django Rest Framework (DRF)

**Frontend**

* React

**Database**

* SQLite (development) / PostgreSQL (production)

**Version Control & Collaboration**

* Git & GitHub

---

## 🗂️ Project Structure

```
students-internship-placement-system/
│── backend/                     # Django + DRF
│   │── internship_system/
│   │   │── settings.py
│   │   │── urls.py
│   │   │── asgi.py
│   │   │── wsgi.py
│   │
│   │── students/                # Student app
│   │── companies/               # Company app
│   │── institution/             # Institution/Admin app
│   │── api/                     # DRF API modules
│   │
│   │── manage.py
│   │── requirements.txt
│
│── frontend/                    # React app
│   │── public/
│   │── src/
│   │   │── components/
│   │   │── pages/
│   │   │── services/            # API calls
│   │   │── App.js
│   │   │── index.js
│   │
│   │── package.json
│
│── README.md
```

---

## 🚀 Installation & Setup Guide

### Backend (DRF)

1. Clone the repo

```bash
git clone https://github.com/Habrovan004/students-internship-placement-system
cd students-internship-placement-system/backend
```

2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Make and apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

### Frontend (React)

1. Open a new terminal and go to the frontend folder

```bash
cd ../frontend
```

2. Install packages

```bash
npm install
```

3. Start the React app

```bash
npm start
```

The frontend will open at: `http://localhost:3000`

---

## 🤝 Collaboration Workflow (GitHub)

1. Create feature branches
2. Make commits with clear descriptions
3. Push to GitHub
4. Open pull requests (PRs)
5. Team reviews and merges to `main`

---

## 📈 Future Enhancements

* Email/SMS notifications
* Dashboard analytics
* User roles & permissions
* Resume/CV upload
* Deployment (Heroku / Render / Vercel)

---

## 📄 License

This project is developed for **academic purposes** and may be expanded or modified.

---

## 📞 Contact

**Project Team:** STUDENTS INTERNSHIP AND ATTACHMENTS PLACEMENT SYSTEM Team
**Institution:** ARDHI UNIVERCITY
**Course:** INFORMATION SYSTEM MANAGEMENTS
