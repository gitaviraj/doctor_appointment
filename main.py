from app_config import app, db
from models import Doctor, User, Appointment
from auth import auth
from user_auth import user


if __name__ == '__main__':
    db.create_all()
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(user, rl_prefix='/user')
#    app.run(host='0.0.0.0', port=7000, debug=True)
    app.run(debug=True)
