import pandas as pd
import pathlib

from template_parameters import *

class PS_SlurmRun:
    def __init__(self):
        print("PS_SlurmRun: Constructor")

        #  Check if the csv slurm file already exists
        self.slurm_csv_fn= f"{slurm_runs_csv_file_dir}/{slurm_runs_csv_file}"
        if not pathlib.Path(self.slurm_csv_fn).is_file():
            print("PS_SlurmRun: slurm file needs to be generated")
            #  ... if not, generate the file
            self.__generate_slurm_csv_file()
        print("PS_SlurmRun: slurm file now definitely exists")

        #  Generate dataframe from slurm csv file
        self.slurm_df= pd.read_csv(self.slurm_csv_fn)

        # Get a list of all jobs that need to be submitted
        #   either from slurm_job_list (in template_parameters.py)
        #   or from all entries in parameter_study_list.csv where "run?" is True
        self.slurm_job_list= self.__fill_slurm_job_list()
        print(f"PSS_SlurmRun: self.slurm_job_list= {self.slurm_job_list}")

        # read out the information of already submitted and running jobs (all ids)

    def is_running(self, job_id):
        ret= False
        s= self.slurm_df['running?']
        print(s)
        print(f"is_running: {job_id} {ret}")
        return(ret)
    def __generate_slurm_csv_file(self):
        print("PS_SlurmRun: generate slurm file")

        # generate slurm_file/df from content of parameter_study_list_file
        params_csv_fn = f"{parameter_study_csv_file_dir}/{parameter_study_csv_file}"
        ps_params_df = pd.read_csv(params_csv_fn)
        ps_slurm_df = ps_params_df[["id", "run?"]]

        # add all missing columns to df and write to file
        for key in slurm_runs_entries.keys():
            ps_slurm_df[f"{key}"] = slurm_runs_entries[key]

        ps_slurm_df.to_csv(self.slurm_csv_fn, index= False)
        # print(ps_slurm_df)

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
        #  as long as list has entries,
        #  take and eliminate first element of list
        if not self.slurm_job_list:
            job_id= self.slurm_job_list.pop()
            print(f"PS_SlurmRun find_next with id= {job_id}")
            return(job_id)
        return(False)

    # start the run for id
    # 1. create templates
    # 2. submit job to slurm queue
    #  either return job info, or directly add it to csv slurm file
    def run(self, id):
        print("run is not implemented yet")

    def finished(self, job_id, timestamp, slurm_job_id):
        # if slurm_job_id != self.check_slurm_job_id(job_id):
        #     warning("slurm Job ID doesn't match!")
        self.register(job_id, "finished?", timestamp, slurm_job_id)

    def register(self, job_id, field, timestamp, slurm_job_id):
        print(self.slurm_df[field])
        # change entry in Pandas DF and CVS file
