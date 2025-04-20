from Controllers.apply_controller import JobApplicationController
from flask import Blueprint

job_application_bp = Blueprint('JobApplication', __name__)

job_application_bp.add_url_rule('/applyJob', view_func=JobApplicationController.applyJob, methods=['POST'])
job_application_bp.add_url_rule('/updateJob', view_func=JobApplicationController.updateJob, methods=['PUT'])
job_application_bp.add_url_rule('/cancelApplication', view_func=JobApplicationController.cancelApplication, methods=['DELETE'])
job_application_bp.add_url_rule('/getApplicationById', view_func=JobApplicationController.getApplicationById, methods=['GET'])
job_application_bp.add_url_rule('/getApplicationsByUser', view_func=JobApplicationController.getApplicationsByUser, methods=['GET'])
job_application_bp.add_url_rule('/getApplicationsByJob', view_func=JobApplicationController.getApplicationsByJob, methods=['GET'])
job_application_bp.add_url_rule('/getApplicationsByQuery', view_func=JobApplicationController.getApplicationsByQuery, methods=['GET'])
