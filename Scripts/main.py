from paramStudyTemplate import ParamStudyTemplate
from LabBook import LabBook
import pandas as pd

#pst= ParamStudyTemplate()
#pst.build_all_templates()

input_file_path= "../Inputs/parameter_study_list.csv"
lb= LabBook(input_file_path)
lb.initialize(input_file_path)

#with open("../Inputs/parameter_study_list.csv") as ps_list:
 #   lines= ps_list.readlines()


# generate lab_book as pandas dataFrame


