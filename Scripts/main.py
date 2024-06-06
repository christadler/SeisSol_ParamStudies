from PS_Templates import *
from template_parameters import *
# from PS_SlurmRun import *

pst= PS_Template()
for job_id in slurm_job_list:
    pst.build_all_templates(id=job_id)





