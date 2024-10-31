import sys
import csv

# Filter by department number and year
departement_numbers = {'53', '61', '28'}
year_min = 2006
year_max = 2010

def mapper():
    """
    Process each row of a CSV file from standard input and filter data by department number and year.
    
    Reads data from the standard input, expecting CSV format with specific columns related to client orders.
    Each row is filtered based on predefined department numbers and a date range for the year. Rows that
    meet these criteria are output in a specific format suitable for Hadoop processing.
    
    Required columns:
    - 'codcli': client code
    - 'cpcli': postal code of client
    - 'villecli': city of client
    - 'codcde': order code
    - 'timbrecde': order timestamp
    - 'qte': quantity ordered
    - 'datcde': order date in 'YYYY-MM-DD' format

    Output format:
    - Each filtered row is printed in the format: 'villecli;qte;timbrecde;codcde'.

    Filtering criteria:
    - Orders between years `year_min` and `year_max` (inclusive).
    - Postal code starts with one of the specified department numbers.
    """

    # Read from standard input
    reader = csv.DictReader(sys.stdin)
    
    for row in reader:
        try:
            # Check if all required columns are present
            required_columns = ['codcli', 'cpcli', 'villecli', 'codcde', 'timbrecde', 'qte', 'datcde']
            if not all(key in row for key in required_columns):
                print("Missing columns in row: %s" % row, file=sys.stderr)
                continue

            # Extract necessary columns
            cpcli = row['cpcli']
            villecli = row['villecli']
            codcde = row['codcde']
            timbrecde = row['timbrecde']
            qte = row['qte']

            # Filter by year and department number
            year_commande = int(row['datcde'].split('-')[0])
            if year_min <= year_commande <= year_max and cpcli[:2] in departement_numbers:
                # Output format for Hadoop
                print('%s;%s;%s;%s' % (villecli, qte, timbrecde, codcde))

        except (ValueError, IndexError) as e:
            print("Malformed line: %s, Error: %s" % (row, e), file=sys.stderr)

# Run the mapper
if __name__ == "__main__":
    mapper()
