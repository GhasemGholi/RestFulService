from main import db_api

class MessageBuilder:
    class Urls(db_api.Model):
        id = db_api.Column("id", db_api.Integer, primary_key=True)
        original = db_api.Column("original", db_api.String())
        short = db_api.Column("short", db_api.String())
        user = db_api.Column("user", db_api.String())
        
        def __init__(self, original, short, user) -> None:
            self.original = original
            self.short = short
            self.user = user
            
        def displayItems(self):
            return {"id": self.id, "original": self.original, "shortened": self.short, 'user':self.user}