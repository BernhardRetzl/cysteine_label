## System Requirements

### Hardware Requirements
- **General:** No special hardware requirements. The software is designed to run on standard consumer hardware with enough RAM to load the data.

### Software Requirements
- **Operating System:** The software was tested on Windows 11, but it should be compatible with any operating system that supports Anaconda (conda), including macOS and Linux distributions.

### Python Dependencies
The script mainly depends on the scientific packages:
```
numpy
pandas
biopython
```


To run the script:
 1. Install conda (e.g. miniconda https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html)
 2. Optional: Install libmamba solver (https://www.anaconda.com/blog/a-faster-conda-for-a-growing-community)
 3. Install git
 4. Clone this repository
 5. Create a new environment in conda (conda env create -f environment.yml)
 6. Run the scripts in the new created environment with python MSFragger.py and afterwards python calculate_median.py
Make sure to run the script in the same folder where exactely one file named *_label_quant.tsv (* any character) and exectly one FASTA file *.fasta (* any character) is located.
