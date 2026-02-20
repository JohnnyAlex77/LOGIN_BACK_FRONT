# LOGIN_BACK_FRONT

Proyecto de autenticación con Django (backend) y React + Vite + Tailwind v4 + shadcn/ui (frontend)

## Tecnologías

### Backend
- Django 5+
- Django REST Framework
- JWT Authentication
- SQLite

### Frontend
- React 18+
- Vite
- Tailwind CSS v4
- shadcn/ui
- React Router DOM
- Axios

## Instalación
### Backend
cd login
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python crear_usuarios_prueba.py
python manage.py runserver
### Frontend
cd frontend
npm install
npm run dev 

Credenciales de prueba
Admin: admin / admin123
Estudiante: estudiante1 / estudiante123
Empresa: empresa1 / empresa123
