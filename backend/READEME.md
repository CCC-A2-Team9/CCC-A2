# Team9 - Backend

## 1. How to run
    cd Backend/ docker-compose up


## 2. Role
Handle ajax data requests from the front-end and use MapReduce to process data from the database to the front-end.

## 3. Main logic
MapReduce is used to remove duplicate data (based on user ID and Twitter text). If two Documents have the same user ID and Twitter text, they are regarded as duplicate.
In addition, MapReduce is used to calculate the proportion of positive sentiment tweets in scenario 1, 2 and 3, so as to infer the sentiment tendency of each scenario in each suburb.
If MapReduce encounters an error, errorHandle captures the error in time to prevent backend crashes.

