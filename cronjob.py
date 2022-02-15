import json
from models.jobs.jobs_tasks import Jobs_Task
import pycron
from datetime import datetime
import time
import config
from models.jobs.jobs_model import jobs_model
import os

jobs = Jobs_Task()

def UpdateJobs():
    jobs.clear_jobs()
    with config.engine.connect() as conn:
        result = conn.execute(config.text(f"select * from jobs"))
        rows = result.fetchall()
        for user in rows:
            job = jobs_model()
            job.name = user._mapping['name']
            job.desc = user._mapping['description']
            job.server = user._mapping['server']
            job.expression = user._mapping['expression']
            job.command =  json.loads(user._mapping['command'])
            job.enabled = user._mapping['enabled']
            jobs.add_jobs(job)
            
def Start():
    date_started = datetime.now()
    data_em_texto = date_started.strftime('%d/%m/%Y %H:%M')
    print(f'thread iniciada {data_em_texto}')
    UpdateJobs()
    while True:
        for job in jobs.get_jobs():
            if job.enabled == 1 and pycron.is_now(job.expression):
                data_atual = datetime.now()
                data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M')
                if len(job.command) > 1:
                    for c in job.command:
                        os.system(c)
                        print(f'comando: {job.name} executando "{c}" em {job.server} {data_em_texto}')
                        config.logging.info(f'comando: {job.name} executando "{c}" em {job.server} {data_em_texto}')
                          
                else:         
                    os.system(job.command[0])  
                    print(f'comando: {job.name} executando "{job.command[0]}" em {job.server} {data_em_texto}')
                    config.logging.info(f'comando: {job.name} executando "{job.command[0]}" em {job.server} {data_em_texto}')
                      
        time.sleep(60)
