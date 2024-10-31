import pandas as pd
import unidecode
import sys

def read_and_clean_csv(input_file, output_file):
    """
    Read, clean, and transform a CSV file, then save the cleaned data to a new CSV file.

    This function reads a CSV file, performs several data cleaning steps, and saves the result:
    - Removes accents from string columns.
    - Converts the 'datcde' column to datetime, removing rows with invalid dates.
    - Fills missing values for various columns with specified defaults and casts columns to appropriate data types.
    - Removes duplicate rows.

    Parameters:
    - input_file (str): Path to the input CSV file.
    - output_file (str): Path to the output CSV file to save cleaned data.

    Data Cleaning Steps:
    - Removes accents from text in object columns.
    - Converts 'datcde' to datetime, removing rows with invalid dates.
    - Fills missing values based on data type:
        - For numeric columns, fills with 0.
        - For string columns, fills with an empty string.
        - For boolean columns, fills with `False`.
    - Removes duplicate rows.

    Output:
    - A cleaned CSV file is saved at the specified `output_file` path.
    """
    try:
        # Read CSV file
        df = pd.read_csv(input_file, encoding='utf-8')
        print(f"Initial number of rows: {len(df)}")

        # Remove accents 
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)

        # Convert dates and remove rows with invalid dates
        df['datcde'] = pd.to_datetime(df['datcde'], errors='coerce')
        df = df.dropna(subset=['datcde'])  
        print(f"Number of rows after date conversion: {len(df)}")

        # Replace NaN values 
        df['codcli'] = df['codcli'].fillna(0).astype('int32')
        df['genrecli'] = df['genrecli'].fillna('').astype('string')
        df['nomcli'] = df['nomcli'].fillna('').astype('string')
        df['prenomcli'] = df['prenomcli'].fillna('').astype('string')
        df['cpcli'] = df['cpcli'].fillna('').astype('string').str.zfill(5)
        df['villecli'] = df['villecli'].fillna('').astype('string')
        df['codcde'] = df['codcde'].fillna(0).astype('int32')
        df['timbrecli'] = df['timbrecli'].fillna(0.0).astype(float)
        df['timbrecde'] = df['timbrecde'].fillna(0.0).astype(float)
        df['Nbcolis'] = df['Nbcolis'].fillna(0).astype('int8')
        df['cheqcli'] = df['cheqcli'].fillna(0.0).astype(float)
        df['barchive'] = df['barchive'].fillna(False).astype('bool')
        df['bstock'] = df['bstock'].fillna(False).astype('bool')
        df['codobj'] = df['codobj'].fillna(0).astype('int32')
        df['qte'] = df['qte'].fillna(0).astype('int16')
        df['Colis'] = df['Colis'].fillna(0).astype('int32')
        df['libobj'] = df['libobj'].fillna('').astype('string')
        df['Tailleobj'] = df['Tailleobj'].fillna('').astype('string')
        df['Poidsobj'] = df['Poidsobj'].fillna(0.0).astype(float)
        df['points'] = df['points'].fillna(0).astype('int32')
        df['indispobj'] = df['indispobj'].fillna(False).astype('bool')
        df['libcondit'] = df['libcondit'].fillna('').astype('string')
        df['prixcond'] = df['prixcond'].fillna(0.0).astype(float)
        df['puobj'] = df['puobj'].fillna(0.0).astype(float)
        print(f"Number of rows after filling missing values: {len(df)}")

        # Remove duplicates
        df = df.drop_duplicates()
        print(f"Number of rows after removing duplicates: {len(df)}")

        # Save the cleaned data to a new CSV file
        df.to_csv(output_file, index=False)
        print(f"New file created successfully: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    input_file = './data/dataw_fro03.csv'  
    output_file = './data/cleaned_data.csv'  

    read_and_clean_csv(input_file, output_file)
