import pandas as pd
import pathlib

from template_parameters import *

class PS_SlurmRun:
    def __init__(self):
        print("Constructor PS_SlurmRun Class")
        # get a list of all jobs that need to be submitted
        self.slurm_job_list= self.__fill_slurm_job_list()
        print(f"self.slurm_job_list= {self.slurm_job_list}")

        # check if some jobs have been submitted

        self.slurm_csv_fn= f"{slurm_runs_csv_file_dir}/{slurm_runs_csv_file}"
        #  check if the csv slurm file already exists
        #  if not, generate the file
        if not pathlib.Path(self.slurm_csv_fn).is_file():
            print("slurm file needs to be generated")
            self.__generate_slurm_file()
        print("slurm file now definitely exists")

        # read out the information of already submitted and running jobs (all ids)
        self.psr_df = pd.read_csv(self.slurm_csv_fn)


    def __generate_slurm_file(self):
        print("PS_SlurmRun: generate slurm file")

        # generate slurm_file/df from content of parameter_study_list_file
        params_csv_fn = f"{parameter_study_csv_file_dir}/{parameter_study_csv_file}"
        ps_params_df = pd.read_csv(params_csv_fn)
        ps_slurm_df = ps_params_df[["id", "run?"]]

        # add all missing columns to df and write to file
        for key in slurm_runs_entries.keys():
            ps_slurm_df[f"{key}"] = slurm_runs_entries[key]
        ps_slurm_df.to_csv(self.slurm_csv_fn, index= False)
        print(ps_slurm_df)

    def __fill_slurm_job_list(self):
        # if list is empty it will be filled with all jobs where "run?" is "True"
        # Todo: Not sure if this is filled correctly
        if not slurm_job_list:
            print("Empty slurm_job_list...")
            psr_df = pd.read_csv(f"../Inputs/{parameter_study_csv_file}")
            rows= psr_df.loc[psr_df["run?"]]
            slurm_list= rows["id"].to_list
            print(slurm_list)
            print("... has been filled")
            return(slurm_list)
        else:
            return(slurm_job_list)


    # check in csv parameter file which jobs should run (pd.df)
    # compare with csv slurm file which have not yet run
    def find_next_slurm_id(self):
        id= self.slurm_job_list[0]
        print(f"PS_SlurmRun find_next with id= {id}")
        #  return id and delete it from the list
        #  (or move it to the list of scheduled runs?)
        return(id)

    # start the run for id
    # 1. create templates
    # 2. submit job to slurm queue
    #  either return job info, or directly add it to csv slurm file
    def run(self, id):
        print("run is not implemented yet")

