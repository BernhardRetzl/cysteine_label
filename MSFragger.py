from perseuspy import pd
from Bio import SeqIO
import re
import os
import glob


def get_fasta_file():
    """searches for the FASTA-file in the current working directory"""
    dir_path = os.path.dirname(os.path.abspath(__file__))
    fasta_file = glob.glob(dir_path+r'\*.fasta')
    if len(fasta_file) > 1:
        raise FileExistsError('More than one fasta-file found')
    if len(fasta_file) == 0:
        raise FileNotFoundError('No fasta-file found')
    return fasta_file[0]


def read_FASTA_file(fasta_file):
    """converts FASTA-file to a dictionary termed FASTA_dict"""
    FASTA_dict = dict()
    seq_file = SeqIO.parse(fasta_file, 'fasta')
    for entry in seq_file:
        identifier = entry.id.split('|')[1]
        FASTA_dict[identifier] = str(entry.seq)
    return FASTA_dict


def read_df_and_get_sequnces(FASTA_dict, matrix_file):
    """reads a Perseus matrix file and adds the UniProt sequence based on the Protein.Group column"""
    def get_sequence(item):
        return FASTA_dict.get(item)
    df = pd.read_perseus(matrix_file)
    df['UniProt_sequence'] = df['Protein ID'].apply(get_sequence)
    return df


def find_peptide_in_protein(df):
    """finds the position of the peptide in the protein sequence"""
    for index, row in df.iterrows():
        peptide = row['Peptide Sequence']
        protein = row['UniProt_sequence']
        if protein:
            df.loc[index, 'position_in_protein'] = int(protein.find(peptide))
    return df


def get_mod_position_and_AA_one_item(item, pattern):
    match_positions = list()
    aa_of_interest = list()
    matches = re.finditer(pattern, item)
    total_match_length = 0
    for match in matches:
        match_string = match.group()
        match_position = match.span()[0]
        match_positions.append(match_position - total_match_length)
        aa_of_interest.append(item[match_position-1])
        total_match_length += len(match_string)
    return match_positions, aa_of_interest


def get_mod_position_and_AA_all_items(df):
    for index, row in df.iterrows():
        position_in_protein = row['position_in_protein']
        light_modified_peptide = row['Light Modified Peptide']
        if type(light_modified_peptide) == str and type(row['UniProt_sequence']) == str:
            mod_positions, aa_of_interest = get_mod_position_and_AA_one_item(light_modified_peptide,
                                                                             pattern=r'\[125.(\d+)\]')
            if mod_positions:
                uni_mod_positions = [str(int(position_in_protein + i)) for i in mod_positions]
                uni_mod_positions_text = ';'.join(uni_mod_positions)
                aa_of_interest = ';'.join(aa_of_interest)
                df.loc[index, 'mod_light'] = uni_mod_positions_text
                df.loc[index, 'mod_light_aa'] = aa_of_interest

        heavy_modified_peptide = row['Heavy Modified Peptide']
        if type(heavy_modified_peptide) == str and type(row['UniProt_sequence']) == str:
            mod_positions, aa_of_interest = get_mod_position_and_AA_one_item(heavy_modified_peptide,
                                                                             pattern=r'\[130.(\d+)\]')
            if mod_positions:
                uni_mod_positions = [str(int(position_in_protein + i)) for i in mod_positions]
                uni_mod_positions_text = ';'.join(uni_mod_positions)
                aa_of_interest = ';'.join(aa_of_interest)
                df.loc[index, 'mod_heavy'] = uni_mod_positions_text
                df.loc[index, 'mod_heavy_aa'] = aa_of_interest
    return df


def clean_up_data(df):

    df['mod_light_aa'].replace('n', '', inplace=True)
    df['mod_heavy_aa'].replace('n', '', inplace=True)
    for index, row in df.iterrows():
        mod_light_aa = row['mod_light_aa']
        mod_heavy_aa = row['mod_heavy_aa']
        if mod_light_aa != '' and mod_heavy_aa == '':
            df.loc[index, 'amino_acid'] = mod_light_aa
        elif mod_light_aa == '' and mod_heavy_aa != '':
            df.loc[index, 'amino_acid'] = mod_heavy_aa
        elif mod_light_aa == '' and mod_heavy_aa == '':
            df.loc[index, 'amino_acid'] = mod_light_aa
        else:
            df.loc[index, 'amino_acid'] = mod_light_aa

    df['mod_light'].replace('na', '', inplace=True)
    df['mod_heavy'].replace('nan', '', inplace=True)
    for index, row in df.iterrows():
        mod_light = row['mod_light']
        mod_heavy = row['mod_heavy']
        if mod_light != '' and mod_heavy == '':
            df.loc[index, 'position'] = mod_light
        elif mod_light == '' and mod_heavy != '':
            df.loc[index, 'position'] = mod_heavy
        elif mod_light == '' and mod_heavy == '':
            df.loc[index, 'position'] = mod_light
        else:
            df.loc[index, 'position'] = mod_light

    cols = list(df.columns)
    part_1 = cols[:7]
    part_2 = cols[7:-2]
    part_3 = cols[-2:]
    cols = part_1 + part_3 + part_2
    df = df[cols]

    df.drop(columns=['UniProt_sequence', 'position_in_protein', 'mod_light', 'mod_heavy', 'mod_light_aa',
                     'mod_heavy_aa'], inplace=True)
    return df


def write_output_to_file(df, matrix_file):
    matrix_file = matrix_file.split('.tsv')[0]
    matrix_file = matrix_file + '_p.tsv'
    df.to_csv(matrix_file, sep='\t', index=False)


def standalone_version():
    fasta_file = get_fasta_file()
    FASTA_dict = read_FASTA_file(fasta_file)
    matrix_file = glob.glob('*_label_quant.tsv')[0]
    df = read_df_and_get_sequnces(FASTA_dict, matrix_file)
    df = find_peptide_in_protein(df)
    df = get_mod_position_and_AA_all_items(df)
    df = clean_up_data(df)
    write_output_to_file(df, matrix_file)


standalone_version()
