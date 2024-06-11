

"""
    Step 1: Parameters & templates
"""

# the csv file with all parameters and values
# first line: "id" <parameter1_name>  <parameter2_name>  ... <parameterN_name> "run?"
# other lines:<id> <parameter1_value> <parameter2_value> ... <parameterN_value> <True/False>
# stored in dir "../Input/"
parameter_study_csv_file_dir= "../Inputs"
parameter_study_csv_file= "parameter_study_list.csv"

# list of all parameters from the cvs file
# Todo: Generate tp_param_list from input_csv_file some day (all column names wo "id")
#   and check that it is corresponds to the given tp_param_list
# currently xha from AltoTiberina_forced_rupture_time.yaml is not used
tp_param_list = ["nucleation", "d_c", "y", "mu_s", "R"]

# list of all jinja template files (except slurm tmpl for stage 2)
# to be filled by user
# stored in dir "../Input/Templates/*SeisSol_slurm_JobFarm.slurm.jinja"
# "AltoTiberina_forced_rupture_time.yaml" (xha) currently not used
tp_list = ["AltoTiberina_fault.yaml",
           "AltoTiberina_initial_stress.yaml",
           "AltoTiberina_sig_zz.yaml",
           "AltoTiberina_forced_rupture_time.yaml"]

# mapping of parameters to jinja templates
# to be filled by user
# Todo: Add templates for nucleation
# "AltoTiberina_forced_rupture_time.yaml" : ["xha"],
tp_mapping = { "AltoTiberina_fault.yaml" : ["mu_s", "d_c"],
               "AltoTiberina_initial_stress.yaml": ["R"],
               "AltoTiberina_sig_zz.yaml": ["y"],
               "AltoTiberina_forced_rupture_time.yaml": ["xha_x", "xha_y", "xha_z"]
               }

"""
    Step 2: SLURM Submission & Feedback
"""
#  the parameters.par file
tp_parameters= "parameters.par.jinja"

# the slurm template
# stored in dir "../Input/Templates/"
tp_slurm= "SeisSol_slurm_tmpl.jinja"
tp_slurm_jobFarm= "SeisSol_slurm_JobFarm.slurm.jinja"

# parameters for slurm template
tp_job_name = 'MathildeTest'
tp_slurm_group = 'pn49ha'

#  Iris
tp_slurm_account = 'di35ban'
tp_slurm_email = 'christadler@geophysik.uni-muenchen.de'
tp_output_file_dir= '/hppfs/scratch/0A/di35ban/AltoTiberina/outputs'

#  Mathilde
# tp_slurm_account = 'ra35zih2'
# tp_slurm_email = 'marchandon@geophysik.uni-muenchen.de'
#  ... adapt to run in SCRATCH
# tp_output_file_dir= '/hppfs/work/pn49ha/ra35zih2/AltoTiberina/outputs'


# This is not used, since we use jobFarming instead
'''
slurm_runs_csv_file_dir= "../Outputs"
slurm_runs_entries={"scheduled?": "False", 
                    "running?": "False",
                    "finished?": "False",
                    "job_submission_time":"False",
                    "job_start_time": "False",
                    "job_end_time": "False",
                    "job_return_value": "False",
                    "cpu_budget": "NaN",
                    }
'''

# Allow the user to specify in which order the jobs will be submitted
# if this list is empty, it will be filled in class PS_SlurmRun with all ids
# slurm_job_list = [ <id1>, <id2>, ... , <idN>]
# slurm_job_list= [5, 10, 14]
# slurm_job_list=[]
# slurm_job_list= [14,16,18,20,21,23, 24, 25, 26, 27, 30]
# slurm_job_list= [14,16]
slurm_job_list= list(range(100))
# print(f"slurm_job_list: {slurm_job_list}")

# the number of jobs in _one_ jobFarming-Script
# compute this as: max_queue_runtime/(job_runtime+postprocessing_runtime)
slurm_jobfarming_chunks= 10

"""
    Step 3: Data products & verification
"""
#  will be done directly by adjusting the slurm file
#  TODO: add here the two scripts
#        or add a postprocessing bash/phyton script
#        in all directories that is then called
#        that might be difficult since it will be in the wrong place ($WORK not $SCRATCH)
# /SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py
# myfile='outputnew/AltoTiberina_1DLatorre_Ro070_us037_Dc04_nuc2-surface.xdmf'
# srun python -u ~/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py $myfile --MP 48
postprocessing_cmd1= "pwd"
# postprocessing_cmd1= "/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py"
postprocessing_cmd2= "date"
# postprocessing_cmd2= "srun python -u

"""
    Step 4: Upload to SDL
"""