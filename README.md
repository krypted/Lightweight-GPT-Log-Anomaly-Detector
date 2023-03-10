# Lightweight-GPT-Log-Anomaly-Detector
Python-based anomaly detector that uses the ChatGPT API to look for anomalies in untrained and lightly trained troves of macOS system logs

# Environment: Python 3.6.6

# Create a virtual environment
python3.6 -m virtualenv venv

# Activate the virtual environment
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt

## Create the log file
sudo log show --last 10m > log-info-10m.txt

## Run the script log-analysis.py to parse log file and generate anomalous logs
# example usage:
python log-analysis.py --log_filename log-info-10m.txt
python log-analysis.py --log_filename log-info-10m.txt --use_error_keywords True --score_threshold 0.5
python log-analysis.py --log_filename log-info-10m.txt --use_error_keywords False --score_threshold 0.5

# Run the script gpt.py to get chatGPT response for any log
# example usage:
python gpt.py --log "2023-03-06 12:51:55.328197+0530 0x20698c6  Default     0x0                  0      0    kernel: (RTBuddy) RTBuddy(DCP): WARNING: failed to send ping."

# Update the OPENAI_API_KEY in the file gpt.py with your own key
# check line 5 in gpt.py
