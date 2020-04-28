from swagger_server.config import db


class Email(db.Model):
    app_code = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(255), primary_key=True)
