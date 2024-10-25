import json

word_freq = {}

with open("./spider/tables.json", "r") as f:
    tables_data = json.load(f)

# print(len(tables_data))

# count=0
count2 = 0

# for item in tables_data:
#     for table_name in item["table_names_original"]:
#         # if table_name in word_freq: count+=1
#         word_freq[table_name]=1
#         count2+=1

# print(count)
# print(count2)

with open("./spider/train_spider.json") as f:
    spider_train_data = json.load(f)

with open("./spider/dev.json") as f:
    spider_dev_data = json.load(f)

print(len(spider_train_data))
print(len(spider_dev_data))

freq_map = {}

database_id = ["department_management", "farm", "student_assessment", "book_2"]

pruneCount = 0
anomCount = 0

with open("./spider/train_spider_main_data.json", 'w') as f:
    for item in spider_train_data:
        word_freq = {}

        for item2 in tables_data:
            if item2['db_id'] == item['db_id']:
                for table_name in item2["table_names_original"]:
                    word_freq[table_name.lower()] = 1

        interim_map = {}
        f2 = False
        for query_tok in item["query_toks"]:
            if query_tok.lower() in word_freq:
                if query_tok.lower() not in interim_map:
                    interim_map[query_tok.lower()] = 1

        num_tables = len(interim_map)

        if num_tables > 1 or num_tables == 1:
            f2 = True
            if num_tables in freq_map:
                freq_map[num_tables] += 1
            else:
                freq_map[num_tables] = 1

        if num_tables == 1:
            pruneCount += 1

        if num_tables == 0:
            print(item['db_id'])
            print(item['query'])
            print("\n")
            anomCount += 1

        if f2:
            f.write(json.dumps(item))
            f.write("\n")

    for key, val in freq_map.items():
        print(key, "->", val)

print("AnomCount")
print(anomCount)
print("PruneCount")
print(pruneCount)