#!/bin/bash
# Job Name and Files (also --job-name)

#SBATCH -J FL33_Turquie
#Output and error (also --output, --error):
#SBATCH -o ./%j.%x.out
#SBATCH -e ./%j.%x.err

#Initial working directory:
#SBATCH --chdir=/hppfs/work/pn49ha/ra35zih2/AltoTiberina/dynamic_rupture/test_5

#Notification and type
#SBATCH --mail-type=END
#SBATCH --mail-user=marchandon@geophysik.uni-muenchen.de

# Wall clock limit:
#SBATCH --time=00:30:00
#SBATCH --no-requeue

#Setup of execution environment
#SBATCH --export=ALL
#SBATCH --account=pn49ha
#constraints are optional
#--constraint="scratch&work"
#SBATCH --partition=test

#Number of nodes and MPI tasks per node:
#SBATCH --nodes=16
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
mpiexec -n $SLURM_NTASKS temp_seissol/SeisSol_Release_dskx_4_elastic parameters.par
#mpiexec -n $SLURM_NTASKS /hppfs/work/pr63qo/di52lak2/2021Qinghai/SeisSol_Release_dskx_4_elastic parameters_SFS.par
