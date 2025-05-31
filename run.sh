#!/bin/bash
#SBATCH --job-name=trans
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --time=1-12:00:00
#SBATCH --mem=6400MB
#SBATCH --cpus-per-task=1
#SBATCH --output=/data2/sonhyelin/logs/sbatch_log/%x_%j.log
#SBATCH --error=/data2/sonhyelin/logs/sbatch_log/%x_%j.log

source /data2/sonhyelin/.bashrc
source /data2/sonhyelin/miniconda3/etc/profile.d/conda.sh
conda activate mqm

echo "[TIME] $(date)"
python a.py
echo "[TIME] $(date)"