import pandas as pd
import numpy as np

# Importing both parts, concat them and remove duplicates
df1 = pd.read_csv('quintoandar_data_pt1.csv')
df2 = pd.read_csv('quintoandar_data_pt2.csv')
df = pd.concat([df1, df2], ignore_index=True)
df = df.drop_duplicates(ignore_index=True)

# Removing some nulls
df = df.dropna(subset=['Total']).reset_index(drop=True)

# Parsing house type from title
df['house_type'] = df['Title'].apply(lambda x: x.split()[0])
df.drop(axis=1, columns='Title', inplace=True)

# Parsing district out of address
#df['district'] = df['Address'].apply(lambda x: x.split(',')[1].strip())
df['district'] = df['Text'].apply(lambda x: x.split('\n')[-4].split(',')[0].strip())
df.drop(axis=1, columns=['Address', 'Text'], inplace=True)

# Removing text from area
df['area'] = df['Area'].apply(lambda x: x.replace('m²', '').strip())
df.drop(axis=1, columns='Area', inplace=True)

# Spliting into bedrooms and suites 
df['bedroom'] = df['Bedroom'].apply(lambda x: x.split('quarto')[0].strip())
df['suite'] = df['Bedroom'].apply(lambda x: x.split('(')[1].split()[0] if '(' in x else 0 )
df.drop(axis=1, columns='Bedroom', inplace=True)

# Removing text from garage capacity
df['garage'] = df['Garage'].apply(lambda x: 0 if 'Sem' in x else x.split()[0])
df.drop(axis=1, columns='Garage', inplace=True)

# Removing text from floor location
df['floor'] = df['Floor'].apply(lambda x: x.split('º')[0] if 'º' in x else np.nan )
df.drop(axis=1, columns='Floor', inplace=True)

# Parsing numbers from price infos
df['rent'] = df['Rent'].apply(lambda x: x.split('R$')[1].replace('.','').strip())
df['condominium'] = df['Condominium'].apply(lambda x: x.split('R$')[1].replace('.','').strip() if 'R$' in x else np.nan)
df['is_condominium_included'] = df['Condominium'].apply(lambda x: 1 if 'Incluso' in x else 0)
df['taxes'] = df['Taxes'].apply(lambda x: x.split('R$')[1].replace('.','').strip() if 'R$' in x else np.nan)
df['is_taxes_included'] = df['Taxes'].apply(lambda x: 1 if 'Incluso' in x else 0)
df['fire_insurance'] = df['Fire Insurance'].apply(lambda x: x.split('R$')[1].replace('.','').strip())
df['service'] = df['Services'].apply(lambda x: str(x).split('R$')[1].replace('.','').strip() if 'R$' in str(x) else np.nan)
df['total'] = df['Total'].apply(lambda x: x.split('R$')[1].replace('.','').strip())
df.drop(axis=1, columns=['Rent', 'Condominium', 'Taxes', 'Fire Insurance', 'Services', 'Total'], inplace=True)

df.to_csv('quintoandar_cleaned_data.csv', index=False)