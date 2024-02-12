tp_job_name = 'MathildeTest'

tp_slurm_group = 'pn49ha'
tp_slurm_account = 'ra35zih2'
tp_slurm_email = 'marchandon@geophysik.uni-muenchen.de'

# list of all parameters
# Todo: Generate tp_param_list from input_csv_file some day (all column names wo "id")
tp_param_list = ["nucleation", "d_c", "fluid_pressure", "mu_s", "R"]

# list of all jinja template files
# to be filled by user
tp_list = ["AltoTiberina_fault.yaml.jinja",
           "AltoTiberina_forced_rupture_time.yaml.jinja",
           "SeisSol_slurm_tmpl.jinja"]

# mapping of parameters to jinja templates
# to be filled by user
tp_mapping = { "AltoTiberina_fault.yaml.jinja" : ["mu_s", "d_c"],
               "AltoTiberina_initial_stress.yaml.jinja": ["R"],
               "SeisSol_slurm_tmpl.jinja": []
               }