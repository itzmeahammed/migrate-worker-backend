from Models.apply_job_model import JobApplication
from Models.jobs_model import Job
from Models.user_model import User
from Utils.CommonExceptions import CommonException
import logging
from flask import request, jsonify

class JobApplicationController:
    def applyJob():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            if not user:
                return CommonException.InvalidIdException()
            data = request.get_json()
            if not data or "job_id" not in data:
                return CommonException.DataRequiredException()
            
            job = Job.objects(id=data.get("job_id")).first()
            if not job:
                return jsonify({"message": "Job not found"}), 404
            
            application = JobApplication(job=job, user=user)
            application.save()
            return jsonify({
                "message": "Job application submitted successfully",
                "application": application.to_json()
            }), 200
        except Exception as e:
            logging.error(f"Error in applyJob: {str(e)}")
            return CommonException.handleException(e)
    
    def cancelApplication():
        try:
            application_id = request.args.get("id")
            if not application_id:
                return CommonException.IdRequiredException()
            
            application = JobApplication.objects(id=application_id).first()
            if not application:
                return jsonify({"message": "Job application not found or unauthorized"}), 404

            token = request.headers.get("Authorization")
            user = User.objects(auth_token=token).first()
            if not user or str(user.id) != str(application.user.id):
                return jsonify({"message": "Unauthorized action"}), 401
            
            application.delete()
            return jsonify({"message": "Job application cancelled successfully"}), 200
        except Exception as e:
            logging.error(f"Error in cancelApplication: {str(e)}")
            return CommonException.handleException(e)
    
    def getApplicationById():
        try:
            application_id = request.args.get("id")
            if not application_id:
                return CommonException.IdRequiredException()
            application = JobApplication.objects(id=application_id).first()
            if not application:
                return jsonify({"message": "Job application not found"}), 404
            return jsonify(application.to_json()), 200
        except Exception as e:
            logging.error(f"Error in getApplicationById: {str(e)}")
            return CommonException.handleException(e)
    
    def getApplicationsByUser():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            if not user:
                return CommonException.InvalidIdException()
            
            applications = JobApplication.objects(user=user.id)
            return jsonify([app.to_json() for app in applications]), 200
        except Exception as e:
            logging.error(f"Error in getApplicationsByUser: {str(e)}")
            return CommonException.handleException(e)
    
    def getApplicationsByJob():
        try:
            job = request.args.get('job')
            if not job:
                return CommonException.IdRequiredException()
            applications = JobApplication.objects(job=job)
            return jsonify([app.to_json() for app in applications]), 200
        except Exception as e:
            logging.error(f"Error in getApplicationsByJob: {str(e)}")
            return CommonException.handleException(e)
