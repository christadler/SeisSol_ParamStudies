from jinja2 import Template
from pathlib import Path
from template_parameters import *

class ParamStudyTemplate:

    def __init__(self):
        # hand over parameters from parameter file
        self.job_id= '003'
        self.xha= '298075.0,4808050.0,-3039.31'
    def __build_slurm_template(self):
        with (open('../Inputs/Templates/SeisSol_slurm_tmpl.jinja') as f):
            slurm_tmpl = Template(f.read())

        with open(f"../Submissions/{self.job_id}/{tp_job_name}_{self.job_id}.slurm", mode="w") as f:
            f.write(slurm_tmpl.render(job_name = tp_job_name,
                                      job_id= self.job_id,
                                      group= tp_slurm_group,
                                      account= tp_slurm_account,
                                      email= tp_slurm_email))

    def __build_xha_template(self):
        with (open('../Inputs/Templates/AltoTiberina_forced_rupture_time.yaml.jinja') as f):
            xha_tmpl = Template(f.read())

        with open(f"../Submissions/{self.job_id}/AltoTiberina_forced_rupture_time.yaml", mode="w") as f:
            f.write(xha_tmpl.render( xha= self.xha))

    def build_all_templates(self):
        # create a directory under Submission for the jobId
        Path(f"../Submissions/{self.job_id}").mkdir(parents=True, exist_ok=True)
        # copy over all files that need no adjustment
        # build parameter files
        # xha is currently not used
        #self.__build_xha_template()
        # build slurm submission script
        self.__build_slurm_template()

