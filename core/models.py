from core import db

class Urls(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    original = db.Column("original", db.String())
    short = db.Column("short", db.String())

    def __init__(self, original, short) -> None:
        self.original = original
        self.short = short