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
## Installation and preparation
1.  **Install conda or miniconda if not present**
  - Miniconda can be installed from [Miniconda Installation Guide](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html).
  - Optional: Install the libmamba solver for a faster package resolution. [Learn more about libmamba](https://www.anaconda.com/blog/a-faster-conda-for-a-growing-community).
2. **Install Git (if not present):**
   - Download and install from [Git SCM](https://git-scm.com/).
3. **Clone the repository:**
```
git clone https://github.com/BernhardRetzl/cysteine_label
cd cysteine_label
```
- create a new conda environment using the environment.yml file and activate the environment
```
conda env create -f environment.yml
conda activate posttranslational
```
- copy exactly one file named \*_label_quant.tsv (\* any character) and exactely one FASTA-file named \*.fasta (\* any character) into the same folder where the script is located

## Running of the scripts
```
python MSFragger.py
python calculate_median.py
```
