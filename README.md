# data-vis-kakenhi
search keyword using NLP, then count frequencies of university

## How to run
You can use Anaconda/Miniconda or use your own python virtual environment and install by pip

### Use Anaconda/Miniconda

1. Install anaconda/miniconda by following the instruction here [anaconda/miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

2. The conda environment is provided as `env.yml`. This environment is used for all testing by Github Actions and can be setup by:
- `conda env create -f env.yml`
- `conda activate kobe-u`

### Use your own python environment
1. Create and activate your python virtual environment by following the instruction here [python venv](https://docs.python.org/3/library/venv.html)

2. Install the requirements by run the following command in your terminal:
```bash
pip install -r requirements.txt
```

## Run fastapi local server
```bash
uvicorn main:app
```