#!/bin/bash
# Job Name and Files (also --job-name)
#SBATCH -J AltoTiberina_0009
#SBATCH -o ./%j.%x.%N.out
#SBATCH -e ./%j.%x.%N.err

# Notification and type
#SBATCH --mail-type=ALL
#SBATCH --mail-user=iris.christadler@lmu.de

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

# TODO: Copy file ../Outputs/job_name_job_id.par to the right directory
# TODO: Or maybe better: set working_dir in the beginning to something useful
mkdir -p /hppfs/scratch/0A/di35ban/AltoTiberina/outputs/0009/
srun -n $SLURM_NTASKS ../seissol_bin/SeisSol_Release_dskx_4_elastic parameters.par
#mpiexec -n $SLURM_NTASKS ../seissol_bin/SeisSol_Release_dskx_4_elastic parameters.par