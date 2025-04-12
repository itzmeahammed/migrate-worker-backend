from mongoengine import Document, ReferenceField
from Models.jobs_model import Job
from Models.user_model import User

class JobApplication(Document):
    job = ReferenceField(Job, required=True, reverse_delete_rule=2)
    user = ReferenceField(User, required=True, reverse_delete_rule=2)

    def to_json(self):
        return {
            "id": str(self.id),
            "job": self.job.to_json() if self.job else None,
            "user": self.user.to_json() if self.user else None,
        }
