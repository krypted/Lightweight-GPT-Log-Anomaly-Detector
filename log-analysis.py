import json
import gensim
import pickle
import pandas as pd
import numpy as np
from tqdm import tqdm

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

from drain3 import TemplateMiner
template_miner = TemplateMiner()

from utils import *

# parse the command line arguments
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--log_filename', type=str, default='log-info-10m.txt')
parser.add_argument('--use_error_keywords', type=bool, default=True)
parser.add_argument('--score_threshold', type=float, default=0.5)

# parse the arguments
args = parser.parse_args()
log_filename = args.log_filename
use_error_keywords = args.use_error_keywords
score_threshold = args.score_threshold

# example usage:
# python log-analysis.py --log_filename log-info-10m.txt
# python log-analysis.py --log_filename log-info-10m.txt --use_error_keywords True --score_threshold 0.5
# python log-analysis.py --log_filename log-info-10m.txt --use_error_keywords False --score_threshold 0.5

# Parse Logs
logging.info("Parsing logs...")
log_data = list()
new_line = list()
for line in open(log_filename).read().strip().split("\n")[1:]:
    if(re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)):
        if(new_line):
            log_data.append(" ".join(new_line))
            new_line = list()
        new_line.append(line)
    else:
        new_line.append(line)

parsed_log_data = list()
for log_line in log_data:
    d = parse_log_line(log_line)
    if(d):
        d['raw'] = log_line
        parsed_log_data.append(d)

# Use Drain3 to mine templates and cluster logs
logging.info("Mining templates...")
message_list = dict()
for i, d in tqdm(enumerate(parsed_log_data)):
    log_message = d['message']
    template_info = template_miner.add_log_message(log_message.strip())
    template_message = template_info['template_mined']
    # remove <*> from template_message and replace extra spaces with single space
    template_message = re.sub(r'\s+', ' ', re.sub(r'<\*>', '', template_message)).strip()
    template_message = " ".join(log_tokenizer(template_message))
    if(template_message not in message_list and template_message):
        message_list[template_message] = list()
    if(template_message):
        message_list[template_message].append(i)

message_l = list(message_list.keys())
clean_message_l = message_l

# Create a TFIDF vectorizer
logging.info("Creating TFIDF vectorizer...")
tfidf_vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(" "), dtype=np.float32)
tfidf_matrix = tfidf_vectorizer.fit_transform(clean_message_l)

def get_log_vectors(message_l):
    clean_message_l = [" ".join(log_tokenizer(message)) for message in message_l]
    tfidf_matrix = tfidf_vectorizer.transform(clean_message_l)
    return tfidf_matrix

input_log_vectors = get_log_vectors(clean_message_l)

# Create a kmeans object with 10 clusters
logging.info("Clustering logs...")
kmeans = KMeans(n_clusters=10, random_state=0)
# Fit the kmeans object to the tfidf_word_vectors
kmeans = kmeans.fit(input_log_vectors)

# Get the cluster centroids and calculate scores
kmeans_scores = list()
for i in tqdm(range(input_log_vectors.shape[0])):
    ss = float(cosine_similarity(input_log_vectors[i:i+1], kmeans.cluster_centers_[kmeans.labels_[i:i+1]])[0][0])
    kmeans_scores.append(ss)

# anomaly_df = pd.DataFrame(parsed_log_data)
anomaly_df = list()
for msg, idx in list(message_list.items()):
    anomaly_df.append({"message": msg, 'idx_list': str(idx), 'count': len(idx)})
anomaly_df = pd.DataFrame(anomaly_df)

anomaly_df['cluster'] = kmeans.labels_
anomaly_df['score'] = kmeans_scores
# sort by score
anomaly_df = anomaly_df.sort_values(by=['score'], ascending=True)

anomaly_logs = list()
for cluster in anomaly_df['cluster'].unique().tolist():
    for i, row in anomaly_df[(anomaly_df['cluster'] == cluster) & (anomaly_df['score'] < score_threshold)].iterrows():
        message = row['message']
        if(use_error_keywords):
            # check if any error keyword is present in the message
            if(any([keyword in message.lower() for keyword in ERROR_KEYWORDS])):
                anomaly_logs.append(dict(row))
        else:
            anomaly_logs.append(dict(row))

anomaly_logs_df = pd.DataFrame(anomaly_logs)
# get where count < 10
anomaly_logs_df = anomaly_logs_df[anomaly_logs_df['count'] < 10]
idx_dict = dict()
anomaly_logs_data = list()
for i, row in anomaly_logs_df.iterrows():
    for idx in json.loads(row['idx_list']):
        idx_dict[idx] = row['score']
for idx in idx_dict:
    d = parsed_log_data[idx]
    d['score'] = idx_dict[idx]
    anomaly_logs_data.append(d)

anomaly_logs_df = pd.DataFrame(anomaly_logs_data)
parsed_log_df = pd.DataFrame(parsed_log_data)

# save the dataframes
logging.info("Saving Anomaly Logs and Parsed Logs")
# create output directory if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')
anomaly_logs_df.to_csv("output/anomaly_logs.csv", index=False)
parsed_log_df.to_csv("output/parsed_log.csv", index=False)