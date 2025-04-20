from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Job(Document):
    title = StringField(required=True)
    company = StringField(required=True)
    description = StringField(required=True)
    location = StringField(required=True)
    salary = StringField(required=True)
    requirements = StringField(required=True)
    posted_at = DateTimeField(default=datetime.utcnow)

    def update(self, **kwargs):
        self.clean()
        return super().update(**kwargs)

    def to_json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "location": self.location,
            "salary": self.salary,
            "requirements": self.requirements,
            "posted_at": self.posted_at.isoformat() if self.posted_at else None
        }
