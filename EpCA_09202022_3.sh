#!/bin/bash 
#SBATCH --job-name=nxtflwhd
#SBATCH --time=96:00:00
#SBATCH -p ellenyeh
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --output=/scratch/groups/ellenyeh/epithemia_assembly_runs/EpCA_09202022_3/slurm_logs/nextflow-head-%j.out
#SBATCH --mem=8G

source ~/.bashrc
conda activate env/
# export NXF_OPTS="-Xmx30g"
output_dir=/scratch/groups/ellenyeh/epithemia_assembly_runs/EpCA_09202022_3/
nextflow run_all2.nx -c ./run_configs/EpCA_09202022_3.config -with-report ${output_dir}/reports/report.html -w $GROUP_SCRATCH/epithemia_assembly_runs_work/EpCA_09202022_3 -resume 02f8f35b-8b9d-43c6-bc7d-aa10a2ef34e4
