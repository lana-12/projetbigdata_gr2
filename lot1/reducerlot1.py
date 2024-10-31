import os
import sys
import csv
import pandas as pd

def reducer():
    """
    Process CSV input data from standard input, aggregate by order code, and export the top 100 results to Excel.

    This function reads semi-colon delimited data from the standard input, with each line containing:
    - 'ville' (city of the order)
    - 'qte' (quantity ordered)
    - 'timbrecde' (order timestamp as a float)
    - 'codcde' (order code)
    
    The reducer aggregates total quantities and timestamp sums for each unique order code (`codcde`). The top 100
    entries by total quantity and timestamp are saved in descending order in an Excel file.

    Data Processing:
    - For each line, the function extracts the relevant columns and aggregates `quantity_totale` and `timbrecde_total` 
      for each unique `codcde`.
    - Malformed lines or rows with conversion errors are logged to standard error.

    Output:
    - Top 100 entries (by total quantity and timbrecde) are saved to an Excel file at the path:
      `'/datavolume1/results_lot1.xlsx'`.
    - The resulting DataFrame contains columns: 'Ville', 'Code Commande', 'Quantité Totale', 'Timbrecde Total'.
    """

    results = {}

    for line in sys.stdin: 
        line = line.strip()
        if not line:  
            continue

        parts = line.split(';')
        if len(parts) < 4:  
            print("Malformed line: %s" % line, file=sys.stderr)
            continue
        
        # Data extraction from lines and parts
        try:
            ville = parts[0]  
            qte = int(parts[1]) 
            timbrecde = float(parts[2])  
            codcde = parts[3]  

            if codcde not in results:
                results[codcde] = {'ville': ville, 'quantity_totale': 0, 'timbrecde_total': 0.0}
                
            results[codcde]['quantity_totale'] += qte
            results[codcde]['timbrecde_total'] += timbrecde

        except ValueError as e:
            print("Malformed line: %s, Error: %s" % (line, e), file=sys.stderr)
            
    # Sort results by total quantity and total timbre in descending order
    top_100_results = sorted(results.items(), key=lambda x: (x[1]['quantity_totale'], x[1]['timbrecde_total']), reverse=True)[:100]
    print("Top 100 results: {}".format(top_100_results))
   
    # Prepare data for DataFrame
    # Create DataFrame
    df = pd.DataFrame([(data['ville'], codcde, data['quantity_totale'], data['timbrecde_total']) for codcde, data in top_100_results],
                      columns=['Ville', 'Code Commande', 'Quantité Totale', 'Timbrecde Total'])

    # Specify the output file path
    xlsx_file_path =xlsx_file_path = '/datavolume1/results_lot1.xlsx'

    # Export to Excel
    df.to_excel(xlsx_file_path, index=False)

    print("Saved results in '%s'." % xlsx_file_path)

if __name__ == "__main__":
    reducer()
