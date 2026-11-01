# Personal Finance & Habit Dashboard

A Flask-based web application that helps users manage their personal finances, track daily habits, and monitor their progress through data analytics and visual reports.

**Live Demo:** https://finance-dashboard-fwiz.onrender.com

## Features

### User Authentication
- User registration and login.
- Secure password hashing.
- Session-based authentication.
- User-specific data access.

### Expense Tracking
- Add and record expenses.
- Categorize expenses.
- View expense history.
- Delete expense records.
- Generate spending summaries by category.

### Habit Tracking
- Create daily habits.
- Mark habits as completed.
- View habit completion history.
- Track habit streaks.
- Generate weekly habit reports.

### Data Analytics
- Calculate total spending.
- Analyze expenses by category using Pandas.
- Monitor weekly spending trends.
- Visualize spending patterns with Matplotlib charts.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application framework |
| SQLite | Local development database |
| PostgreSQL (Neon) | Production database |
| Pandas | Data analysis |
| Matplotlib | Data visualization |
| HTML & CSS | Frontend |
| Pytest | Automated testing |
| Git & GitHub | Version control |
| Render | Application deployment |

## Project Structure

```text
finance-dashboard/
│
├── app.py
├── database.py
├── models.py
├── tracker.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
├── static/
│   ├── css/
│   └── images/
│
└── tests/
```

*The structure above is representative. Adjust it to match your actual folders and filenames.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd finance-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Set the required environment variables before running the application.

On Windows PowerShell:

```powershell
$env:SECRET_KEY="your-secret-key"
```

For local SQLite development, you can leave `DATABASE_URL` unset if your application is configured to use SQLite by default.

For PostgreSQL, set:

```powershell
$env:DATABASE_URL="your-neon-database-connection-string"
```

Use your own values. Never commit real credentials or secret keys to GitHub.

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## Running Tests

Run the automated test suite with:

```bash
python -m pytest
```

## Deployment

The application is deployed using **Render**, with **Neon PostgreSQL** as its production database.

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

The production environment requires the `SECRET_KEY` and `DATABASE_URL` environment variables to be configured in Render.

## Security

- Passwords are hashed before being stored.
- Login sessions protect authenticated routes.
- User data is separated by account.
- Environment variables are used for sensitive configuration.
- Database files and secret credentials should not be committed to the repository.

## Future Improvements

- Budget planning and spending limits.
- Downloadable monthly financial reports.
- More detailed habit analytics.
- Improved mobile dashboard experience.
- Notifications and reminders.

## Author

Developed as a Python and Flask capstone project to demonstrate practical skills in backend development, database management, authentication, data analysis, testing, and deployment.
