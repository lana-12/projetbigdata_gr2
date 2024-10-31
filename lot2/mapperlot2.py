import sys
import csv

# Departments and year range
departments_number = {'22', '49', '53'}
year_min = 2011
year_max = 2016

def mapper():
    reader = csv.DictReader(sys.stdin)

    for row in reader:
        try:
            # Check for necessary columns
            if not all(key in row for key in ['codcli', 'cpcli', 'villecli', 'codcde', 'timbrecli', 'qte', 'datcde']):
                print("missing columns: %s" % str(row), file=sys.stderr)
                continue

            # Extract columns
            cpcli = row['cpcli']
            villecli = row['villecli']
            codcde = row['codcde']
            timbrecli = row['timbrecli']
            qte = int(row['qte'])
            year_commande = int(row['datcde'].split('-')[0])

            # Filter by year and department number
            if year_min <= year_commande <= year_max and cpcli[:2] in departments_number:
                # Filter orders without specified timbrecli or zero
                if not timbrecli or float(timbrecli) == 0:
                    print("%s\t%s\t%d\t%s" % (codcde, villecli, qte, timbrecli))  # Format expected by the reducer

        except (ValueError, IndexError) as e:
            print("Malformed line: %s, Error: %s" % (row, e), file=sys.stderr)


if __name__ == "__main__":
    mapper()
