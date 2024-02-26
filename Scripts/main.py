from PS_Templates import *
from template_parameters import *
from PS_SlurmRun import *

pst= PS_Template()
for job_id in slurm_job_list:
    pst.build_all_templates(id=job_id)

# psr= PS_SlurmRun()
# next_id= psr.find_next_slurm_id()
# print(psr.is_running(next_id))

#  outdated below
# input_file_path= "../Inputs/parameter_study_list.csv"
# lb= LabBook(input_file_path)
# lb.initialize(input_file_path)

#with open("../Inputs/parameter_study_list.csv") as ps_list:
 #   lines= ps_list.readlines()


# generate lab_book as pandas dataFrame


