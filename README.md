# CCC-A2

## Team Members

Zhaoxiang Ning 1261076  
Xinyi Zhou 1281911  
Haochu Wang 1281962  
Gengchang Xu 1214774  
Shiming Zheng 1149897 

## End user usage
### frontend:
 http://172.26.132.76:3000/
### backend:
 http://172.26.132.76:5000/
### CouchDB:
 http://172.26.132.76:5984/_utils/#/


## Video links
https://www.youtube.com/playlist?list=PLDm_bwsWBEbNV_cvU9CaZkuFJHa5UGKUH

## Report
https://github.com/CCC-A2-Team9/CCC-A2/blob/main/Team9%20COMP90024%20Project2%20report.pdf

## Demo
https://github.com/CCC-A2-Team9/CCC-A2/blob/main/Team9_COMP90024_Project2_pre.pdf

## System Architecture
![system-ar](https://user-images.githubusercontent.com/71579588/167285200-a6da1de9-a03c-4ff9-8803-277a008fae11.png)

## Deployment
    1. cd /Ansible_playbook_files 
    2. ./nectar.sh  
       Enter the OpenStack Password  
    3. ./set-env.sh  
        Enter the OpenStack Password  
    4. ./deploy-application.sh  
        Enter the OpenStack Password 
    5. ./deploy-crawler.sh  
        Enter the OpenStack Password 
        
## Instance
    Instance1: 172.26.133.196    worker
    Instance2: 172.26.134.151    worker
    Instance3: 172.26.132.82     worker
    Instance4: 172.26.132.76     master
