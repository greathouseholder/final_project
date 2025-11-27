import pandas as pd

websites = pd.read_csv('../data/websites_updated.csv')
websites = websites[websites['text'].notnull()]
