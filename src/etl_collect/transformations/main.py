
import pandas as pd
import sqlite3
from datetime import datetime

# Read data into dataframe
df = pd.read_json('src/data/data.json', lines = True)

# Show all columns
pd.options.display.max_columns = None

# Add colmun _source with fixed value as source
df['_source'] = "https://lista.mercadolivre.com.br/notebook"

# Add datetime column with actual datetime for analysis
df['_datetime'] = datetime.now()

# Filter nulls and clean str
df['old_money'] = df['old_money'].fillna('0')
df['new_money'] = df['new_money'].fillna('0')
df['reviews_rating_number'] = df['reviews_rating_number'].fillna('0')
df['reviews_amount'] = df['reviews_amount'].fillna('(0)')
df['old_money'] = df['old_money'].astype(str).str.replace('.', '', regex=False)
df['new_money'] = df['new_money'].astype(str).str.replace('.', '', regex=False)
df['reviews_amount'] = df['reviews_amount'].astype(str).str.replace('[\(\)]', '', regex=True)

# Convert to numbers(float/integer)
df['old_money'] = df['old_money'].astype(float)
df['new_money'] = df['new_money'].astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].astype(float)
df['reviews_amount'] = df['reviews_amount'].astype(int)

# Show only the rows with value range between 1k and 10k
df = df[
    (df['old_money'] >= 1000) & (df['old_money'] <= 10000) &
    (df['new_money'] >= 1000) & (df['new_money'] <= 10000)
]

# Create and/or connect with SQlite database
conn = sqlite3.connect('data/mercadolivre.db')

# Save dataframe into database
df.to_sql('notebook', conn, if_exists='replace', index=False)

# Close connection
conn.close()