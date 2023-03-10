import os
import re

# get stop_words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.remove('no')
stop_words.remove('not')

ERROR_KEYWORDS = ['destroyed', 'error', 'exception', 'fail', 'failed', 'fatal', 'invalid', 'missing', 
                  'not found', 'unable', 'unexpected', 'unable', 'crash']

# function to tokenize string, remove punctuation, and return list of tokens
def log_tokenizer(text):
    def split_word(text):
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        text = re.sub(" +", " ", text)
        return text.strip()    
    text = split_word(text)
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    # remove digits
    text = re.sub(r'\d+', '', text)
    tokens = [token.strip() for token in text.split() if(token.strip() and len(token.strip()) > 1)]
    # remove stop words
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

# function to parse log line
def parse_log_line(log_line):
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}\+\d{4})\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(.+?):\s+(.*)$'
    match = re.search(pattern, log_line)
    if(match):
        timestamp = match.group(1)
        pid = match.group(2)
        log_type = match.group(3)
        address = match.group(4)
        thread_id = match.group(5)
        event_id = match.group(6)
        kernel = match.group(7)
        message = match.group(8)
        d = {"timestamp": timestamp, 
            "pid": pid, 
            "log_type": log_type, 
            "address": address, 
            "thread_id": thread_id, 
            "event_id": event_id, 
            "kernel": kernel, 
            "message": message}
    else:
        d = dict()
    return d