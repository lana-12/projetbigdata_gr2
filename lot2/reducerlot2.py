import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd


def reducer():
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

