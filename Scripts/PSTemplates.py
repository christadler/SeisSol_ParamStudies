from jinja2 import Template
import pandas as pd
from pathlib import Path
from template_parameters import *

"""
 This class reads from the csv file 
 and builds all templates for one id
 
 The slurm class will search for the next id that needs to run
 asks PSTemplate to generate everything for the id
 run and add information about the run after the run
 
"""
class PSTemplate:

    def __init__(self):
        self.pst_df= pd.read_csv(f"../Inputs/{parameter_study_csv_file}")
        self.digits="04d"
        # # hand over parameters from parameter file
        # self.job_id= '003'
        # self.xha= '298075.0,4808050.0,-3039.31'

    def __build_slurm_template(self, id):
        with (open(f"../Inputs/Templates/{tp_slurm}") as f):
            slurm_tmpl = Template(f.read())

        with open(f"../Outputs/{id:{self.digits}}/{tp_job_name}_{id:{self.digits}}.slurm", mode="w") as f:
            f.write(slurm_tmpl.render(job_name = tp_job_name,
                                      job_id= f"{id:{self.digits}}",
                                      group= tp_slurm_group,
                                      account= tp_slurm_account,
                                      email= tp_slurm_email))

    #  This function is currently not used
    # def __build_template(self, id, tmpl_name, parameters):
    #     with (open(f'../Inputs/Templates/{tmpl_name}.jinja') as f):
    #         tmpl = Template(f.read())
    #
    #     with open(f"../Outputs/{id:{self.digits}}/{tmpl_name}", mode="w") as f:
    #         f.write(tmpl.render(parameters))

    def build_all_templates(self, id):
        # create a directory for the jobId in folder "Outputs"
        Path(f"../Outputs/{id:{self.digits}}").mkdir(parents=True, exist_ok=True)
        # copy over all files that need no adjustment
        #  for file in ../Inputs/Files
        #     cp file to ../Outputs/{id}

        # build parameter files
        for tmpl_name in tp_list:
            print(f"processing template: {tmpl_name}")
            tmpl_parameters= tp_mapping[tmpl_name]
            kwargs= dict.fromkeys(tmpl_parameters)
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
