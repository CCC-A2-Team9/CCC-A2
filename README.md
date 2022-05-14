# Team9 - Data Harvest

## 1. Role
    Used to harvest data from twitter.
    
## 2. Main Components
- Using Tweepy API to harvest data.
- Using NLP to analyze the data and classify.
- Using couchdb to store the data.

## 3. Main Process
First, we use tweepy API to harvest data. Second, we do data preprocess (like removing the stopwords, removing useless url and @XXX). After that, we feed the data into nlp analyzer and get the setiment (pos/neg/neu). Then, we divide them into different suburb according to their coordinates. Finally, we use couchdb to store them.
