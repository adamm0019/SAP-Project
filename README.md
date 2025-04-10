# SAP-Project – Secure & Insecure Web Application

- `main`: Contains the secure implementation.
- `insecure`: Includes vulnerabilities.

---

## Branches Overview

| Branch     | Description                                               |
|------------|-----------------------------------------------------------|
| `main`     | Secure implementation of the application                  |
| `insecure` | Contains security vulnerabilities                         |

---

## Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML, Bootstrap
- **Database**: SQLite

---

## Cloning the Repository

```bash
git clone https://github.com/adamm0019/SAP-Project.git
cd SAP-Project
```

## To view the vulnerable application

```bash
git checkout insecure
```

## To view the secure application

```
git checkout main
```

---

# Windows setup:

## Create a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

## Install dependencies:

```
pip install -r requirements.txt
```

---

# Running the webapp:

```
python app.py
```

The app will be accessible at http://localhost:5000/

Insecure Branch – Testing:

The insecure branch includes implementations of:

SQL Injection

Cross-Site Scripting (XSS): Reflected, Stored, DOM-Based

Data Exposure

You can test these by:

Enter values like  `' OR '1'='1` in login fields or `<script>alert('XSS')</script>` in comments.
