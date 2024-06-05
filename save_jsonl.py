import pandas as pd

d = {'input':[1, 2], 'output':['a', 'b']}

df = pd.DataFrame(d)
print(df)
df.to_json('dummy_jsonl.jsonl', orient='records', lines=True)