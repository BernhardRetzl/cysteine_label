import pandas as pd
import glob


file = glob.glob('*_p.tsv')[0]
a = pd.read_csv(file, sep='\t')

for index, row in a.iterrows():
    amino_acid = row['amino_acid']
    if type(amino_acid) != str:
        continue
    position = row['position']
    protein_id = row['Protein ID']
    a.loc[index, 'combined'] = '_'.join([amino_acid, str(position), protein_id])

cols = a.columns[9:-8]
b = a.groupby(['combined'])[cols].median()

a.set_index('combined', inplace=True)

a.update(b)


grouped_df = a.reset_index()
unique_df = grouped_df[~grouped_df['combined'].duplicated()]


unique_df.set_index('combined', inplace=True)


file = file.split('_p.tsv')[0]
file = file + '_p_mu.tsv'
unique_df.to_csv(file, sep='\t', index=False)
