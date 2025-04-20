from Controllers.job_controller import JobController
from flask import Blueprint

job_bp = Blueprint('JobsPosted', __name__)

job_bp.add_url_rule('/getAllJobs', view_func=JobController.getAllJobs, methods=['GET'])
job_bp.add_url_rule('/getJobById', view_func=JobController.getJobById, methods=['GET'])
job_bp.add_url_rule('/createJob', view_func=JobController.createJob, methods=['POST'])
job_bp.add_url_rule('/updateJob', view_func=JobController.updateJob, methods=['PUT'])
job_bp.add_url_rule('/deleteJob', view_func=JobController.deleteJob, methods=['DELETE'])
