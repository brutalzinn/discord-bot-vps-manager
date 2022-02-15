from models.jobs.jobs_model import jobs_model

class Jobs_Task:
    
    def __init__(self):
        self.jobs = []
    def clear_jobs(self):
        self.jobs = []
    def add_jobs(self, job : jobs_model):
        self.jobs.append(job)
    def get_jobs(self):
        return self.jobs