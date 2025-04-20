from Models.jobs_model import Job
from Utils.CommonExceptions import CommonException
import logging
from flask import request, jsonify

class JobController:
    def getAllJobs():
        try:
            query = request.args.to_dict()
            if query:
                jobs = Job.objects(**query)
            else:
                jobs = Job.objects()
            return jsonify([job.to_json() for job in jobs]), 200
        except Exception as e:
            logging.error(f"Error in getAllJobs: {str(e)}")
            return CommonException.handleException(e)

    def getJobById():
        try:
            job_id = request.args.get('id')
            if not job_id:
                return CommonException.IdRequiredException()
            job = Job.objects(id=job_id).first()
            if job:
                return jsonify(job.to_json()), 200
            return jsonify({"message": "Job not found"}), 404
        except Exception as e:
            logging.error(f"Error in getJobById: {str(e)}")
            return CommonException.handleException(e)

    def createJob():
        try:
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            # Create a new Job instance using the provided data
            job = Job(**data)
            job.save()
            return jsonify({"message": "Job created successfully", "job": job.to_json()}), 201
        except Exception as e:
            logging.error(f"Error in createJob: {str(e)}")
            return CommonException.handleException(e)

    def updateJob():
        try:
            job_id = request.args.get('id')
            if not job_id:
                return CommonException.IdRequiredException()
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()

            job = Job.objects(id=job_id).first()
            if not job:
                return jsonify({"message": "Job not found or unauthorized"}), 404

            job.update(**data)
            return jsonify({"message": "Job updated successfully"}), 200
        except Exception as e:
            logging.error(f"Error in updateJob: {str(e)}")
            return CommonException.handleException(e)

    def deleteJob():
        try:
            job_id = request.args.get('id')
            if not job_id:
                return CommonException.IdRequiredException()

            job = Job.objects(id=job_id).first()
            if not job:
                return jsonify({"message": "Job not found or unauthorized"}), 404

            job.delete()
            return jsonify({"message": "Job deleted successfully"}), 200
        except Exception as e:
            logging.error(f"Error in deleteJob: {str(e)}")
            return CommonException.handleException(e)
