from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    #app.config.from_object('config.Config')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://avnadmin:AVNS_M4XPUGHtiJz3RctIKmo@mirzaahmergull-aiven-mysql-test-project-bunnybeans.k.aivencloud.com:10555/defaultdb'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from routes import bp as main_bp

    app.register_blueprint(main_bp)

    return app