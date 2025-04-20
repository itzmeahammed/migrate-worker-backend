from Models.apply_job_model import JobApplication
from Models.jobs_model import Job
from Models.user_model import User
from Utils.CommonExceptions import CommonException
import logging
from flask import request, jsonify
import base64

class JobApplicationController:
    def applyJob():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            if not user:
                return CommonException.InvalidIdException()
            
            job_id = request.form.get("job_id")
            resume_file = request.files.get("resume")

            if not job_id or not resume_file:
                return CommonException.DataRequiredException()
            
            job = Job.objects(id=job_id).first()
            if not job:
                return jsonify({"message": "Job not found"}), 404

            resume_bytes = resume_file.read()
            resume_base64 = base64.b64encode(resume_bytes).decode('utf-8')

            application = JobApplication(
                job=job,
                user=user,
                resume=resume_base64
            )
            application.save()

            return jsonify({
                "message": "Job application submitted successfully",
                "application": str(application.id)
            }), 200
        except Exception as e:
            logging.error(f"Error in applyJob: {str(e)}")
            return CommonException.handleException(e)
    
    def updateJob():
        try:
            application_id = request.args.get("id")
            if not application_id:
                return CommonException.IdRequiredException()
            data = request.get_json()
            resume_file = request.files.get("resume")
            application = JobApplication.objects(id=application_id).first()
            if not application:
                return jsonify({"message": "Not found"}), 401
            if resume_file:
                resume_base64 = base64.b64encode(resume_file.read()).decode('utf-8')
                data['resume'] = resume_base64
            if data:
                application.update(**data)

            return jsonify({"message": "Resume updated successfully"}), 200
        except Exception as e:
            logging.error(f"Error in updateResume: {str(e)}")
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
    
    def getApplicationsByQuery():
        try:
            query = request.args.to_dict()
            if not query:
                applications = JobApplication.objects()
            else:
                applications = JobApplication.objects(**query)
            return jsonify([app.to_json() for app in applications]), 200
        except Exception as e:
            logging.error(f"Error in getApplicationsByJob: {str(e)}")
            return CommonException.handleException(e)
