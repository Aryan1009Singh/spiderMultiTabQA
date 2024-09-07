import json
train_file_path = "F:/OneDrive/Desktop/Study/NLP_ResearchProject/Project/spider/train_spider.json"
dev_file_path = "F:/OneDrive/Desktop/Study/NLP_ResearchProject/Project/spider/dev.json"
tables_file_path = "F:/OneDrive/Desktop/Study/NLP_ResearchProject/Project/spider/tables.json"
load_file_path = "F:/OneDrive/Desktop/Study/NLP_ResearchProject/Project/spider/train_spider_main_data.json"

with open(train_file_path) as f:
    spider_train_data=json.load(f)

with open(dev_file_path) as f:
    spider_dev_data=json.load(f)

with open(tables_file_path,"r") as f:
    tables_data=json.load(f)

freq_map={}
db_freq_map={}
og_db_freq_map={}

#databases u want to prune
database_id = ["academic","activity_1","aircraft","allergy_1","apartment_rentals","store_1"]
dbFilterOn=0

pruneCount=0
anomCount=0
total=0
with open(load_file_path, 'w') as f:
    for item in spider_train_data:
        if item['db_id'] in og_db_freq_map: og_db_freq_map[item['db_id']]+=1
        else: og_db_freq_map[item['db_id']]=1
        
        if (item['db_id'] in database_id and dbFilterOn==1) or dbFilterOn==0:
        # if (item['db_id']==database_id[2] and dbFilterOn==1) or dbFilterOn==0:    
            word_freq={}        
            total+=1
            for item2 in tables_data:
                if item2['db_id']==item['db_id']:
                    for table_name in item2["table_names_original"]:
                        word_freq[table_name.lower()]=1

            interim_map={}
            flag = False
            for query_tok in item["query_toks"]:
                if query_tok.lower() in word_freq:
                    if query_tok.lower() not in interim_map:
                        interim_map[query_tok.lower()]=1

            num_tables=len(interim_map)

            if (num_tables>1):
                if item['db_id'] in db_freq_map: db_freq_map[item['db_id']]+=1
                else: db_freq_map[item['db_id']]=1 
                flag = True
                if num_tables in freq_map: freq_map[num_tables]+=1
                else: freq_map[num_tables]=1

            #finding high number of table databases
            # if (num_tables>3):
            #     print(item['db_id'])

            if (num_tables==1):
                pruneCount+=1

            # debugging: finding queries using 0 tables
            if (num_tables==0):
                # print(item['db_id'])
                # print(item['query'])
                # print("\n")
                anomCount+=1

            if flag==True:
                f.write(json.dumps(item))
                f.write("\n")

freq_map={key: freq_map[key] for key in sorted(freq_map)}

# print(db_freq_map)

#data logging
print(f"multitab databases: {len(db_freq_map)}")
print(f"total databases: {len(og_db_freq_map)}")
print(f"#anomalies: {anomCount}")
print(f"Total queries: {total}")
print(f"#queries with 1 table: {pruneCount}")
for key, val in freq_map.items():
    print(f"#tables:{key} #queries:{val}")