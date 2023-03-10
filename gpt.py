import uuid
import json
import requests

OPENAI_API_KEY = "OPENAI_API_KEY"

LOG_PROMPT = """Is this log abnormal, answer in 1 word (YES/NO/MAYBE) and give the reason behind it

2023-02-09 14:18:44.244335+0000 0xc08 Default 0x0 210 30 templateMigrator: (SystemMigrationUtils) [com.apple.mac.install:SystemMigration] Considering Migration of Bundle ID "com.adobe.AdobeCrashReporter" Location "/Library/Application Support/Adobe/Adobe Desktop Common/HDBox/AdobeCrashReporter.framework": Migrating since no bundle exists at that local path.
<START>
Abnormal: NO
Reason: The log is a normal system log that describes the migration of a bundle from a specific location to another.
<STOP>

----------
Is this log abnormal, answer in 1 word (YES/NO) and give the reason behind it

{}
<START>"""

# parse the command line arguments
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--log', type=str)

# parse the arguments
args = parser.parse_args()
log_message = args.log

# example usage:
# python gpt.py --log "2023-03-06 12:51:55.328197+0530 0x20698c6  Default     0x0                  0      0    kernel: (RTBuddy) RTBuddy(DCP): WARNING: failed to send ping."

import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

ref_id = str(uuid.uuid4())
logging.info(f"Getting response from OpenAI: {log_message}")

url = 'https://api.openai.com/v1/chat/completions'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {OPENAI_API_KEY}'
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You can understand macOS system logs and are able to flag abnormal logs with reason."},
        {"role": "user", "content": LOG_PROMPT.format(log_message)},
    ],
    "max_tokens": 100
}

response = requests.post(url, headers=headers, data=json.dumps(data)).json()
response = response['choices'][0]['message']['content'].strip()
logging.info(f"Response from OpenAI: {response}")

# save the response to output directory
logging.info(f"Saving response to output/{ref_id}.json")
with open(f"output/{ref_id}.json", "w") as f:
    output = {"log": log_message, "response": response}
    out = f.write(json.dumps(output, indent=4))
