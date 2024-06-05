import json
import pandas as pd


with open('concept_examples.jsonl', 'r') as file:
    concept_examples = json.load(file)

df = pd.DataFrame(concept_examples)

print(df)
