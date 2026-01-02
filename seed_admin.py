import os
from bolprex_app import create_app, db
from bolprex_app.models import User

app = create_app()
with app.app_context():
    email = os.getenv('ADMIN_EMAIL')
    name = os.getenv('ADMIN_NAME', 'admin')
    pw = os.getenv('ADMIN_PASSWORD')
    if not email or not pw:
        print('No ADMIN_EMAIL or ADMIN_PASSWORD in .env. Use interactive mode.')
        # interactive fallback
        email = input('Email del admin: ')
        name = input('Nombre del admin: ')
        pw = input('Contraseña: ')
    if User.query.filter_by(email=email).first():
        print('Ya existe un usuario con ese email.')
    else:
        u = User(email=email, name=name, role='admin')
        u.set_password(pw)
        db.session.add(u)
        db.session.commit()
        print('Admin creado:', email)
