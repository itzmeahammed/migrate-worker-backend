from mongoengine import Document, StringField, EmailField
from datetime import datetime

class User(Document):
    username = StringField(required=True)
    role = StringField(choices=['employee','manager'], required=True)
    number = StringField(required=True)
    email = EmailField(unique=True, required=True)
    auth_token = StringField()
    password = StringField(required=True)
    address = StringField()
    location = StringField(required=True)
    zipcode = StringField(required=True)
    
    def update(self, **kwargs):
        self.clean()
        return super().update(**kwargs)
   
    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "number": self.number if self.number else None,
            "email": self.email if self.email else None,
            "role": self.role if self.role else None,
            "address": self.address if self.address else None,
            "location": self.location if self.location else None,
            "zipcode": self.zipcode if self.zipcode else None
        }
    
    def remove_expired_tokens(self):
        current_time = datetime.now()
        valid_tokens = [token for token in self.auth_token if 'exp' in token and token['exp'] > current_time] \
            if isinstance(self.auth_token, list) else []
        self.update(set__auth_token=valid_tokens if valid_tokens else "")
