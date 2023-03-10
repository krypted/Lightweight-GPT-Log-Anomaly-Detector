# Lightweight-GPT-Log-Anomaly-Detector
Python-based anomaly detector that uses the ChatGPT API to look for anomalies in untrained and lightly trained troves of macOS system logs

# Use
A number of options may need to be run in a given environment. To do so, use the following:

## Create a virtual environment
`python3.6 -m virtualenv venv`

## Activate the virtual environment
`source venv/bin/activate`

## Install the requirements
`pip install -r requirements.txt`

## Create the log file
`sudo log show --last 10m > log-info-10m.txt`

## Run the script log-analysis.py to parse log file and generate anomalous logs. Example usage:
`python log-analysis.py --log_filename log-info-10m.txt`
`python log-analysis.py --log_filename log-info-10m.txt --use_error_keywords True --score_threshold 0.5`
`python log-analysis.py --log_filename log-info-10m.txt --use_error_keywords False --score_threshold 0.5`

## Run the script gpt.py to get chatGPT response for any log. Example usage:
`python gpt.py --log "2023-03-06 12:51:55.328197+0530 0x20698c6  Default     0x0                  0      0    kernel: (RTBuddy) RTBuddy(DCP): WARNING: failed to send ping."`

Update: the OPENAI_API_KEY in the file gpt.py with your own key. check line 5 in gpt.py

# Environment: 
## Python version
Python 3.6.6

## Dependencies
appnope==0.1.3

backcall==0.2.0

cachetools==4.2.1

certifi==2022.12.7

charset-normalizer==2.0.12

click==8.0.4

dataclasses==0.8

decorator==5.1.1

drain3==0.9.11

entrypoints==0.4

gensim==4.0.0

idna==3.4

importlib-metadata==4.8.3

importlib-resources==5.4.0

ipykernel==5.5.6

ipython==7.16.3

ipython-genutils==0.2.0

jedi==0.17.2

joblib==1.1.1

jsonpickle==1.5.1

jupyter-client==7.1.2

jupyter-core==4.9.2

Levenshtein==0.20.9

nest-asyncio==1.5.6

nltk==3.5

numpy==1.19.5

pandas==1.1.5

parso==0.7.1

pexpect==4.8.0

pickleshare==0.7.5

prompt-toolkit==3.0.36

ptyprocess==0.7.0

Pygments==2.14.0

python-dateutil==2.8.2

python-Levenshtein==0.20.9

pytz==2022.7.1

pyzmq==25.0.0

rapidfuzz==2.11.1

regex==2022.10.31

requests==2.27.1

scikit-learn==0.23.1

scipy==1.5.4

six==1.16.0

smart-open==6.3.0

threadpoolctl==3.1.0

tornado==6.1

tqdm==4.64.0

traitlets==4.3.3

typing_extensions==4.1.1

urllib3==1.26.14

wcwidth==0.2.6

zipp==3.6.0
