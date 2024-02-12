

class LabBook:
    # def __init__(self, file_path)
    def __init__(self, input_file_path):
        experiment_title= "Mathilde's parameter study"
        # test= "iris"
        self.output_file_path= "../Outputs/LabBook.csv"
        self.header_string= ",should_run, queued, slurm_id, submission_date,finish_date,run_time,cpu_hours,stored2sdl,stored2sdl_date,stored2sdl_dataset,stored2sdl_dataproduct\n"
        self.filler_string= ",True,False,NaN, NaN,NaN,NaN,NaN,False,NaN,NaN,NaN,\n"
        #self.filler_string = ",True,False,,,,,False,,,,\n"

        # generate file output_file_path only if it does not exists
        # can you open a file in append mode and keep the "file handle" open?
        # don't fill it with the content
        with open(input_file_path) as ps_file:
            lines = ps_file.readlines()
        #print(lines[0])
        with open(self.output_file_path, mode="w") as lb_file:
            lb_file.write(lines[0].strip() + self.header_string)

        #initialize(input_file_path)


    def initialize(self, file_path):
        # use self.output file for the LAB_Book
        # the input file file_path only specifies the contents that should be added
        # open the input file, read line by line,
        #   if id does already exist in LabBook
        #      end with an error
        #   otherwise add line to LabBook
        with open(file_path) as ps_list:
            # skip header line
            next(ps_list)
            lines = ps_list.readlines()


        with open(self.output_file_path, mode="a") as lb_file:
            for line in lines:
                #print(line.strip() + self.filler_string)
                lb_file.write(line.strip() + self.filler_string)

    def append_lines(self, file_path):
        print("This function is not yet implemented")
        # TODO (for append)
        #  with open(file_path) as ps_list:
        #     lines= ps_list.readlines()
        #     for line in lines:
        #   check if id is already in the lab_book
        #   if id is in the lab_book, check if parameters are the same
        #      if parameters are the same, everything is fine (evtl. output this?)
        #      if parameters are not the same, issue an error (they should not be overwritten, since that this would mean we would have to delete the output files that correspond to this id
        #   if id is not in the lab_book, add line to lab_book

    def find_next_jobid_to_run(self):
        # TODO
        # search through self.output_filepath
        # to find the next id that has (should_run == True) && (queued == False)
        # return id of this line or NaN if that should_run are queued

    def shouldRun_jobid(self, job_id):
        # TODO
        # the following 4 lines should actually become a routine (get_job(self, job_id)
        #   search through self.output_filepath
        #   to find (id == job_id)
        #   if id does not exist exit with Error
        #   if id does exist more than one exit with Error
        # if queued == NaN wait, then re-check
        # return True if ((should_run == True) && (queued == False))
        # otherwise return False

    def run_jobid(self, job_id):
        # TODO
        # replace the following 3 lines by get_job(self, job_id)
        #   search through self.output_filepath
        #   to find (id == job_id)
        #   if id does not exist exit with Error
        # set queued= NaN
        # slurm_job= pst.build_and_submit_job(job_id)
        # set slurm_id= slurm_job.slurm_id
        # set submission_time= slurm.job_submission time
        #
