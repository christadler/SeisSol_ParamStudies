import pandas as pd
from jinja2 import Template
from pathlib import Path
import shutil
import os

from template_parameters import *


"""
 This class reads from the csv file 
 and builds all templates for one id
 
 The slurm class will search for the next id that needs to run
 asks PSTemplate to generate everything for the id
 run and add information about the run after the run
 
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

    def __build_slurm_template(self, id):
        with (open(f"../Inputs/Templates/{tp_slurm}") as f):
            slurm_tmpl = Template(f.read())

        with open(f"../Outputs/{id:{self.digits}}/{tp_job_name}_{id:{self.digits}}.slurm", mode="w") as f:
            f.write(slurm_tmpl.render(job_name = tp_job_name,
                                      job_id= f"{id:{self.digits}}",
                                      group= tp_slurm_group,
                                      account= tp_slurm_account,
                                      email= tp_slurm_email))

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
        self.__build_slurm_template(id)
