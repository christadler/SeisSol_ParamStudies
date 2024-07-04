#!/bin/bash
# Job Name and Files (also --job-name)

#SBATCH -J MathildeTest_jobFarm
#Output and error (also --output, --error):
#SBATCH -o ./%j.%x.%N.out
#SBATCH -e ./%j.%x.%N.err

#Initial working directory:
#SBATCH --chdir=/hppfs/work/pn49ha/di35ban/AltoTiberina/test_1/

#Notification and type
#SBATCH --mail-type=END
#SBATCH --mail-user=iris.christadler@lmu.de

# Wall clock limit:
# 6 runs, 40 min each, 240 min = 4h
#SBATCH --time=00:30:00
#SBATCH --no-requeue

#Setup of execution environment
#SBATCH --export=NONE
#--export=ALL
#SBATCH --account=pn49ha
#constraints are optional
#--constraint="scratch&work"
#SBATCH --partition=test

#Number of nodes and MPI tasks per node:
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=1
# no longer necessary
#module load slurm_setup
module load slurm_setup

#SBATCH --ear=off

#Run the program:
export MP_SINGLE_THREAD=no
unset KMP_AFFINITY
export OMP_NUM_THREADS=94
export OMP_PLACES="cores(47)"

export XDMFWRITER_ALIGNMENT=8388608
export XDMFWRITER_BLOCK_SIZE=8388608
export SC_CHECKPOINT_ALIGNMENT=8388608

export SEISSOL_CHECKPOINT_ALIGNMENT=8388608
export SEISSOL_CHECKPOINT_DIRECT=1
export ASYNC_MODE=THREAD
export ASYNC_BUFFER_ALIGNMENT=8388608
export SEISSOL_ASAGI_MPI_MODE=OFF

source /etc/profile.d/modules.sh

echo 'num_nodes:' $SLURM_JOB_NUM_NODES 'ntasks:' $SLURM_NTASKS 'cpus_per_task:' $SLURM_CPUS_PER_TASK
ulimit -Ss 2097152

array=(  0001 0011 0021  )
for i in "${array[@]}"
do
        echo "ID: $i"
        cd $i
        mkdir -p /hppfs/scratch/0A/di35ban/AltoTiberina/outputs/$i/
        srun -n $SLURM_NTASKS ../seissol_bin/SeisSol_Release_dskx_4_elastic parameters.par
        myfile=/hppfs/scratch/0A/di35ban/AltoTiberina/outputs/$i/$i-surface.xdmf
        echo "Myfile: $myfile"
	cd  /hppfs/scratch/0A/di35ban/AltoTiberina/outputs/$i/
#        Step 1:
         srun python -u ~/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py $myfile --MP 48
#        Step 2:
#        This will create a file named $filenameprefix-surface-resampled.xdmf
         python ~/SeisSol/postprocessing/visualization/tools/extractDataFromUnstructuredOutput.py $myfile --Data u1 u2 u3 --time 90
         pwd
         date
        #rm $myfile
	pwd
	echo "cd -"
	cd -
	pwd
	echo "cd .."
        cd ..
	pwd
done

