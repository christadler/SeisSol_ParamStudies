"""
    Step 0: Set basic parameters
"""

slurm_modes= ("TEST", "PRODUCTION")
slurm_mode= "PRODUCTION"
user_names= ("IRIS", "MATHILDE")
user_name= "IRIS"

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
# "AltoTiberina_forced_rupture_time.yaml" (xha) is currently not used
tp_list = ["AltoTiberina_fault.yaml",
           "AltoTiberina_initial_stress.yaml",
           "AltoTiberina_sig_zz.yaml",
           "AltoTiberina_forced_rupture_time.yaml"]

# mapping of parameters to jinja templates
# to be filled by user
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
tp_job_name = 'AltoTiberina'
tp_slurm_group = 'pn49ha'

if slurm_mode == "TEST":
    # parameters for TEST runs
    print("Building a slurm script for a TEST run")
    tp_slurm_time = "00:30:00"
    tp_slurm_partition = "test"
    tp_slurm_nodes = "16"
    #  adapt the mesh
    tp_params_mesh= "../../mesh/mesh_topo1km_7_faults_smoothed_v3_smallz"
    tp_params_receiver= "../../mesh/receiver_mesh_topo1km_7_faults_smoothed_v3_smallz"
    tp_params_endTime= "2.0"
    # the number of jobs in _one_ jobFarming-Script
    # compute this as: max_queue_runtime/lower(job_runtime+postprocessing_runtime)
    slurm_jobfarming_chunks = 3
elif slurm_mode == "PRODUCTION":
    print("Building a slurm script for a PRODUCTION run")
    # parameters for GENERAL runs
    tp_slurm_time = "24:00:00"
    tp_slurm_partition = "general"
    tp_slurm_nodes = "48"
    #  adapt the mesh
    tp_params_mesh = "../../mesh/mesh_topo1km_7_faults_smoothed_v3_smallz_1hz"
    tp_params_receiver = "../../mesh/receiver_mesh_topo1km_7_faults_smoothed_v3_smallz_1hz"
    tp_params_endTime= "90.0"
    slurm_jobfarming_chunks = 10
    #  if tp_slurm_nodes= 96, slurm_jobfarming_chunks= 20
else:
    print("No known SLURM mode")

if user_name == "IRIS":
    print("Building a slurm script for Iris")
    tp_slurm_account = 'di35ban'
    tp_slurm_email = 'iris.christadler@lmu.de'
    tp_output_file_dir= '/hppfs/scratch/0A/di35ban/AltoTiberina/outputs2'
elif user_name == "MATHILDE":
    print("Building a slurm script for Mathilde")
    tp_slurm_account = 'ra35zih2'
    tp_slurm_email = 'marchandon@geophysik.uni-muenchen.de'
    #  ... adapt to run in SCRATCH
    tp_output_file_dir= '/hppfs/work/pn49ha/ra35zih2/AltoTiberina/outputs'
else:
    print("No known USER")

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
# slurm_job_list= [2, 12, 22]
# slurm_job_list=[]
slurm_job_list= list(range(100))
# print(f"slurm_job_list: {slurm_job_list}")


"""
    Step 3: Data products & verification
"""
#  will be done directly after the SeisSol run by adjusting the slurm file
# /SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py
# myfile='outputnew/AltoTiberina_1DLatorre_Ro070_us037_Dc04_nuc2-surface.xdmf'
# srun python -u ~/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py $myfile --MP 48
postprocessing_cmd1= 'srun python -u ~/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py $myfile --MP '+tp_slurm_nodes
# postprocessing_cmd1= "/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py"
postprocessing_cmd2= 'python ~/SeisSol/postprocessing/visualization/tools/extractDataFromUnstructuredOutput.py $myfile --Data u1 u2 u3 --time '+str(int(float(tp_params_endTime)))
# postprocessing_cmd2= "srun python -u

"""
    Step 4: Upload to SDL
"""