import pandas as pd
from jinja2 import Template
from pathlib import Path
import shutil
import os

from template_parameters import *


"""
 This class reads from the csv file 
 and builds all templates for one id
 
"""
class PS_Template:

    def __init__(self):
        self.params_csv_fn= f"{parameter_study_csv_file_dir}/{parameter_study_csv_file}"
        self.pst_df= pd.read_csv(self.params_csv_fn)
        self.digits="04d"
        # TODO: check data for consistency
        # e.g. are all parameters available in the csv file?
        # it would also be possible to just go through the template folder
        # and automatically build the dir's (but this could be done later)
        # either for all templates or for all templates from a list
        shutil.rmtree("../Outputs/")
        os.mkdir("../Outputs/")


    def build_new_slurm_templates(self, job_list):
        # pre-build the jobFarming.slurm scripts in the output directory
        # for all jobs in job_list (separated in slurm_jobfarming_chunks)

        print("build_new_slurm_templates")
        with (open(f"../Inputs/Templates/{tp_slurm_jobFarm}") as f):
            slurm_tmpl = Template(f.read())

        # compute num of job scripts that you need
        # slurm_jobfarming_num from template_parameters.py
        #    is the number of jobs in one jobFarming-Script
        num_jobs= len(job_list)
        num_jobs_jobfarming= num_jobs // slurm_jobfarming_chunks
        num_jobs_rest= num_jobs % slurm_jobfarming_chunks
        #  if there is a rest you need one more jobFarming script
        if num_jobs_rest>0:
            num_jobs_jobfarming+= 1
        print(f"num_jobs: {num_jobs} num_jobs_jobfarming: {num_jobs_jobfarming} num_jobs_rest {num_jobs_rest}")

        for id in range(num_jobs_jobfarming):
            index= id * slurm_jobfarming_chunks
            curr_job_list = ""
            for i in range(slurm_jobfarming_chunks):
                if index + i < len(job_list):
                    curr_job_list += f"{job_list[index + i]:{self.digits}} "
            print(f" id: {id} curr_job_list: {curr_job_list}")
            with open(f"../Outputs/{tp_job_name}_{id:{self.digits}}.slurm", mode="w") as f:
                f.write(slurm_tmpl.render(job_name = tp_job_name,
                                          job_list= curr_job_list,
                                          group= tp_slurm_group,
                                          account= tp_slurm_account,
                                          email= tp_slurm_email,
                                          tp_output_file_dir= tp_output_file_dir,
                                          postprocessing_cmd1= postprocessing_cmd1,
                                          postprocessing_cmd2= postprocessing_cmd2))


    def __build_slurmNparameters_template(self, id):
        #  generate one slurm file in each directory to run this manually
        with (open(f"../Inputs/Templates/{tp_slurm}") as f):
            slurm_tmpl = Template(f.read())

        with open(f"../Outputs/{id:{self.digits}}/{tp_job_name}_{id:{self.digits}}.slurm", mode="w") as f:
            f.write(slurm_tmpl.render(job_name = tp_job_name,
                                      job_id= f"{id:{self.digits}}",
                                      group= tp_slurm_group,
                                      account= tp_slurm_account,
                                      email= tp_slurm_email,
                                      tp_output_file_dir= tp_output_file_dir))

        #  generate the parameters.par file with the correct output dir
        with (open(f"../Inputs/Templates/{tp_parameters}") as f):
            slurm_tmpl = Template(f.read())

        with open(f"../Outputs/{id:{self.digits}}/parameters.par", mode="w") as f:
            f.write(slurm_tmpl.render(id = f"{id:{self.digits}}",
                                      tp_output_file_dir= tp_output_file_dir
                                      ))


    def build_all_templates(self, id):
        # create a directory for the jobId in folder "Outputs"
        Path(f"../Outputs/{id:{self.digits}}").mkdir(parents=True, exist_ok=True)

        # copy over all files that need no adjustment
        #  from ../Inputs/Files to ../Outputs/{id}
        src_dir  = "../Inputs/Files/"
        dest_dir = f"../Outputs/{id:{self.digits}}"
        # files = os.listdir(src_dir)
        shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)


        # build parameter files
        for tmpl_name in tp_list:
            print(f"processing template: {tmpl_name}")

            #  setup dictionary to be passed to jinja template
            tmpl_parameters= tp_mapping[tmpl_name]
            kwargs= dict.fromkeys(tmpl_parameters)
            #  get values for all parameters
            for param in tmpl_parameters:
                value= self.pst_df.loc[id,param]
                kwargs[param]= value
            print(f"with arguments: {kwargs}")

            # build each template
            with (open(f'../Inputs/Templates/{tmpl_name}.jinja') as f):
                tmpl = Template(f.read())

            with open(f"../Outputs/{id:{self.digits}}/{tmpl_name}", mode="w") as f:
                f.write(tmpl.render(**kwargs))

        # build slurm submission script
        self.__build_slurmNparameters_template(id)
