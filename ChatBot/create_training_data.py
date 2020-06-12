#### Sequence to Sequences 

import sqlite3
import pandas as pd

timeframes = ["2011-08"]

for timeframe in timeframes:
    connection = sqlite3.connect(f"{timeframe}.db")
    c = connection.cursor()
    limit = 5000 # her seferinde ne kadar çekip dataframe ekliyeceğiz
    last_unix = 0 # buffer işlemini yapabilmek için last_unix timestamp i tutarız
    cur_length = limit
    counter = 0
    test_done = False

    while cur_length == limit:
        df = pd.read_sql(f"SELECT * FROM parent_reply WHERE unix > {last_unix} AND parent NOT NULL AND score>0 ORDER BY unix ASC LIMIT {limit}",connection)
        last_unix = df.tail(1)["unix"].values[0]
        cur_length = len(df)

        if not test_done:
            with open("test.from","a",encoding="utf8") as f:
                for content in df["parent"].values:
                    f.write(content+"\n")

            with open("test.to","a",encoding="utf8") as f:
                for content in df["comment"].values:
                    f.write(content+"\n")
            
            test_done = True

        else :
            with open("train.from","a",encoding="utf8") as f:
                for content in df["parent"].values:
                    f.write(content+"\n")

            with open("train.to","a",encoding="utf8") as f:
                for content in df["comment"].values:
                    f.write(content+"\n")
        
        counter +=1

        if counter%20 == 0:
            print(counter*limit,"rows completed so far.")


