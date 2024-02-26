import sys
import PS_SlurmRun
from datetime import datetime

if __name__ == '__main__':
    # uncomment if finished
    # if len(sys.argv) != 3:
    #     sys.exit("register_job_and_start_next.py job_id slurm_job_id")
    #
    # job_id= sys.argv[1]
    # slurm_job_id= sys.argv[2]
    job_id = 9
    slurm_job_id = 11111

    PS_SlurmRun.finished(job_id= job_id, slurm_job_id= slurm_job_id, timestamp= datetime.now())

    next_job_id= PS_SlurmRun.find_next()

    # try
    PS_SlurmRun.submit(next_job_id)
