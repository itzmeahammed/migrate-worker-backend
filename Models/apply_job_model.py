from mongoengine import Document, ReferenceField, StringField
from Models.jobs_model import Job
from Models.user_model import User

class JobApplication(Document):
    job = ReferenceField(Job, required=True, reverse_delete_rule=2)
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    resume = StringField()
    selected = StringField(choices=['selected', 'rejected'])

    def to_json(self):
        return {
            "id": str(self.id),
            "job": self.job.to_json() if self.job else None,
            "user": self.user.to_json() if self.user else None,
            "resume": self.resume if self.resume else None,
            "selected": self.selected if self.selected else None,
        }
