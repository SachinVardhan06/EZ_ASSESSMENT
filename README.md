# Secure File Sharing System

This project is a secure file sharing system built with Django and Django REST Framework. It allows Operations Users to upload files and Client Users to securely access them. All file transfers are protected with secure tokens and role-based access control.

## Features

- **Role-based access:** Operations (OPS) and Client users
- **File upload:** OPS users can upload PPTX, DOCX, XLSX files
- **Secure download:** Clients can access files via time-limited, single-use download tokens
- **Email verification:** Clients must verify their email before downloading files
- **JWT authentication:** Secure login for both user types
- **Admin panel:** Manage users and files

## Demo Credentials

| Role            | Username        | Password    |
| --------------- | --------------- | ----------- |
| Client User     | sachinvardhan06 | sachin1234  |
| Operations User | ops1            | testpass123 |
| Admin User      | sachin          | 123         |

Admin panel: [https://ez-assessment.onrender.com/admin/](https://ez-assessment.onrender.com/admin/)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```
2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
6. **Access the frontend:**
   - Visit [http://localhost:8000/api/frontend/](http://localhost:8000/api/frontend/) for the demo UI.

## API Endpoints

| Endpoint                            | Method | Description                      |
| ----------------------------------- | ------ | -------------------------------- |
| `/api/ops/login/`                   | POST   | OPS user login (JWT)             |
| `/api/client/signup/`               | POST   | Client user signup               |
| `/api/client/login/`                | POST   | Client user login (JWT)          |
| `/api/client/verify-email/`         | GET    | Email verification               |
| `/api/ops/upload/`                  | POST   | OPS file upload                  |
| `/api/client/files/`                | GET    | List files (client)              |
| `/api/generate-token/<file_id>/`    | GET    | Generate download token (client) |
| `/api/download-file/token/<token>/` | GET    | Download file with token         |
| `/api/frontend/`                    | GET    | Frontend demo page               |

## User Roles

- **OPS (Operations):** Can upload files
- **CLIENT:** Can sign up, verify email, view and download files
- **Admin:** Full access via Django admin panel

## File Types Supported

- `.pptx`, `.docx`, `.xlsx`

## Development Notes

- Default database: SQLite (see `EZ/EZ/settings.py`)
- For production, configure PostgreSQL and SMTP email
- Email verification uses console backend by default

## Dependencies

See `requirements.txt` for full list. Key packages:

- Django
- djangorestframework
- djangorestframework-simplejwt
- django-cors-headers
- gunicorn
- whitenoise

## License

MIT (add your license here)
