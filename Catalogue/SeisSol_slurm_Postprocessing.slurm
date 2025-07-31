#!/bin/bash
# Job Name and Files (also --job-name)
#SBATCH -J AltoTiberina_postProcessing
#SBATCH -o ./%j.%x.%N.out
#SBATCH -e ./%j.%x.%N.err

# Notification and type
#SBATCH --mail-type=ALL
#SBATCH --mail-user=marchandon@geophysik.uni-muenchen.de

# (Group) Account, (max) Wall clock and Queue:
#SBATCH --account=pn49ha
#SBATCH --time=
#SBATCH --no-requeue
#SBATCH --partition=

# Turn off energy aware runtime
#SBATCH --ear=off

# Setup of execution environment
#SBATCH --export=NONE
# Initial working directory (also --chdir)
#SBATCH -D ./

# Number of nodes and MPI tasks per node:
#SBATCH --nodes=
#SBATCH --ntasks-per-node=1

module load slurm_setup

# Run the program:
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

cd /hppfs/work/pn49ha/ra35zih2/AltoTiberina/outputs; pwd

for i in {0000..0099}; do
do
        echo "ID: $i"
        cd $i; pwd
        myfile=$i-surface.xdmf; ls -al $myfile

#       Step 1:
        echo "Postprocessing Step1: ComputeGroundMotionParameters"
#       srun python -u ~/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py $myfile --MP 
        srun python -u ~/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py $myfile --MP 48

#       Step 2:
        echo "Postprocessing Step2: Visualization"
#       This will create a file named $filenameprefix_final_displacement-surface.xdmf
#       seissol_output_extractor $myfile --var u1 u2 u3 --time "i-1" --add2prefix _final_displacement
        seissol_output_extractor $myfile --var u1 u2 u3 --time "i-1" --add2prefix _final_displacement

        cd ..; pwd
done

