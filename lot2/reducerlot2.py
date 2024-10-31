import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd


def reducer():
    """
    Aggregate and analyze order data from standard input, producing summary statistics and saving results in Excel and PDF.

    This function reads tab-separated data from standard input, where each line represents an order with:
    - 'codcde' (order code),
    - 'villecli' (city),
    - 'qte' (quantity),
    - 'timbrecli' (timestamp, optional, defaulting to 0 if missing).

    Data Aggregation:
    - Each order code is used to aggregate total quantities and compute the mean quantity per order code.
    - The resulting data is sorted in descending order by total quantity and mean quantity.

    Output:
    - An Excel file with 5% of the top 100 orders chosen randomly.
    - A pie chart in PDF format showing the distribution of total quantities among selected cities.

    Processing steps:
    - Aggregates total quantities (`total_quantity`) per order code.
    - Calculates the mean quantity (`moyenne_qte`) per order code based on the total orders for each code.
    - Filters the top 100 orders by `total_quantity` and `moyenne_qte` in descending order.
    - Selects a random 5% sample of the top 100 orders and creates a pie chart visualization.

    Files generated:
    - Excel file (`/datavolume1/results_lot02.xlsx`) with selected sample data.
    - PDF file (`/datavolume1/repartition_par_ville.pdf`) with the pie chart.
    """

    results = {}
    counts = {}

    # Reading input data
    for line in sys.stdin:
        try:
            codcde, villecli, qte, timbrecli = line.strip().split('\t')
            qte = float(qte)
            timbrecli = float(timbrecli) if timbrecli else 0.0

            if codcde not in results:
                results[codcde] = {
                    "ville": villecli,
                    "total_quantity": 0,
                }
                counts[codcde] = 0
            
            # Adding quantity to the order
            results[codcde]["total_quantity"] += qte
            counts[codcde] += 1 
                
        except ValueError:
            continue 

    for codcde in results:
        count = counts[codcde]
        results[codcde]["menne_qte"] = results[codcde]["total_quantity"] / count if count > 0 else 0

    # Convert to DataFrame
    df_results = pd.DataFrame.from_dict(results, orient='index').reset_index()
    df_results.columns = ['Codcde', 'Ville', 'Total Quantite', 'Moyenne des Quantites']
 
    # Sort Total Quantite desc, Moyenne des Quantites desc
    df_results = df_results.sort_values(by=['Total Quantite', 'Moyenne des Quantites'], ascending=[False, False])
 
    # Take the top 100 results
    df_top_100 = df_results.head(100)
 
    # Display 5% of these results randomly
    df_sample = df_top_100.sample(frac=0.05)
    
    # Pie chart
    plt.figure(figsize=(10, 6))
    df_sample.groupby('Ville')['Total Quantite'].sum().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Random Display of 5% of the Top 100 Orders')
    plt.ylabel('')
    plt.legend(title='Cities', bbox_to_anchor=(1, 0.5), loc='center left')
    plt.tight_layout()
    plt.savefig('/datavolume1/repartition_par_ville.pdf')
    plt.close()
    
    # Extract result to an Excel file
    output_file = '/datavolume1/results_lot02.xlsx'
    df_sample.to_excel(output_file, index=False)
 
    print("5%% of the top 100 orders have been saved in: %s" % output_file)

if __name__ == "__main__":
    reducer()

