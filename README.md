# SeisSol_ParamStudies

This is a bunch of generic scripts and templates 
that allows you to use SeisSol (https://github.com/SeisSol/SeisSol) for parameter studies. 
It was developed for DT-Geo (DTC-E4, Block 3) to generate 
a catalogue for AltoTiberina. It can be used as is for DT-Geo or easily be adapted for arbitrary problems.

# Requirements

## Python libraries

```bash
python -m pip install -r requirements.txt
```

## Run main.py
The setup currently uses SuperMUC-NG (LRZ, Munich, Germany). 
Please refer to the manual or get in touch with us if you would like to use different hardware.
Otherwise just run 
```bash
python3 Scripts/main.py
```
to generate a 'Catalogue' directory with all input files and slurm scripts.

## SeisSol 

SeisSol needs to be available on the target machine (installed at ~/SeisSol). Make binaries available in 'Catalogue/seissol_bin/'

## Input Mesh and asagi_file

The input mesh and the asagi file are available via the Geo-INQUIRE Simulation Data Lake (SDL):
https://doi.org/10.82554/sdl-48 
Download them to 'Catalogue/mesh/' and 'Catalogue/asagi_file' respectively.


# Submit Slurm jobs
Simply submit the generated slurm scripts with 'sbatch AltoTiberina*slurm'.

# Manual 

A Manual to adapt the workflow to *arbitrary parameter studies*
can be found in the README directory. It will also be useful to move the workflow to different hardware.