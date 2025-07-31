#!/bin/bash
# Job Name and Files (also --job-name)
#SBATCH -J AltoTiberina_jobFarm
#SBATCH -o ./%j.%x.%N.out
#SBATCH -e ./%j.%x.%N.err

# Notification and type
#SBATCH --mail-type=ALL
#SBATCH --mail-user=marchandon@geophysik.uni-muenchen.de

# (Group) Account, (max) Wall clock and Queue:
#SBATCH --account=pn49ha
#SBATCH --time=24:00:00
#SBATCH --no-requeue
#SBATCH --partition=general

# Turn off energy aware runtime
#SBATCH --ear=off

# Setup of execution environment
#SBATCH --export=NONE
# Initial working directory (also --chdir)
#SBATCH -D ./

# Number of nodes and MPI tasks per node:
#SBATCH --nodes=48
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

array=(  0000 0001 0002 0003 0004 0005 0006 0007 0008 0009  )
for i in "${array[@]}"
do
        echo "ID: $i"
        cd $i
        mkdir -p /hppfs/work/pn49ha/ra35zih2/AltoTiberina/outputs/$i/
        srun -n $SLURM_NTASKS ../seissol_bin/SeisSol_Release_dskx_4_elastic parameters.par
        myfile=/hppfs/work/pn49ha/ra35zih2/AltoTiberina/outputs/$i/$i-surface.xdmf
        echo "Myfile: $myfile"
        cd /hppfs/work/pn49ha/ra35zih2/AltoTiberina/outputs/$i/
#       Step 1:
#       srun python -u ~/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py $myfile --MP 48
        srun python -u ~/SeisSol/postprocessing/science/GroundMotionParametersMaps/ComputeGroundMotionParametersFromSurfaceOutput_Hybrid.py $myfile --MP 48

#       Step 2:
#       This will create a file named $filenameprefix_final_displacement-surface.xdmf
#       python ~/SeisSol/postprocessing/visualization/tools/extractDataFromUnstructuredOutput.py $myfile --Data u1 u2 u3 --time 90
#       seissol_output_extractor $myfile --var u1 u2 u3 --time "i-1" --add2prefix _final_displacement
        seissol_output_extractor $myfile --var u1 u2 u3 --time "i-1" --add2prefix _final_displacement

        pwd
        echo "cd -"
        cd -
        pwd
        echo "cd .."
        cd ..
        pwd
done

