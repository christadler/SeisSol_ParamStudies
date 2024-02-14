

"""
    Step 1: Parameters & templates
"""

# the csv file with all parameters and values
# first line: "id" <parameter1_name>  <parameter2_name>  ... <parameterN_name> "run?"
# other lines:<id> <parameter1_value> <parameter2_value> ... <parameterN_value> <True/False>
# stored in dir "../Input/"
parameter_study_csv_file= "parameter_study_list.csv"

# list of all parameters from the cvs file
# Todo: Generate tp_param_list from input_csv_file some day (all column names wo "id")
#   and check that it is corresponds to the given tp_param_list
# currently xha from AltoTiberina_forced_rupture_time.yaml is not used
tp_param_list = ["nucleation", "d_c", "y", "mu_s", "R"]

# list of all jinja template files (except slurm tmpl for stage 2)
# to be filled by user
# stored in dir "../Input/Templates/*.jinja"
# "AltoTiberina_forced_rupture_time.yaml" (xha) currently not used
tp_list = ["AltoTiberina_fault.yaml",
           "AltoTiberina_initial_stress.yaml",
           "AltoTiberina_sig_zz.yaml"]

# mapping of parameters to jinja templates
# to be filled by user
# Todo: Add templates for nucleation
# "AltoTiberina_forced_rupture_time.yaml" : ["xha"],
tp_mapping = { "AltoTiberina_fault.yaml" : ["mu_s", "d_c"],
               "AltoTiberina_initial_stress.yaml": ["R"],
               "AltoTiberina_sig_zz.yaml": ["y"]
               }

"""
    Step 2: SLURM Submission & Feedback
"""
# the slurm template
# stored in dir "../Input/Templates/"
tp_slurm= "SeisSol_slurm_tmpl.jinja"

# other parameters for slurm template
tp_job_name = 'MathildeTest'
tp_slurm_group = 'pn49ha'
tp_slurm_account = 'ra35zih2'
tp_slurm_email = 'marchandon@geophysik.uni-muenchen.de'

# Todo: Not sure if this is needed, or should be a mapping instead
#  please note that job_id will be a main parameter for this template
#  but job_id is only known at runtime... (this differentiates the slurm
#  template from others
#tp_slurm_param_list = ["tp_slurm_group", "tp_slurm_account", "tp_slurm_email"]

# Todo: Allow the user to specify in which order the jobs will be submitted
# slurm_job_order = [ <id1>, <id2>, ... , <idN>]

"""
    Step 3: Data products & verification
"""

"""
    Step 4: Upload to SDL
"""