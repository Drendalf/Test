from ..extensions import db


class Itcompanies(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_company = db.Column(db.String)
    code_okved = db.Column(db.String)
    inn = db.Column(db.Integer, nullable=False)
    kpp = db.Column(db.Integer, nullable=False)
    place_of_registration = db.Column(db.String)