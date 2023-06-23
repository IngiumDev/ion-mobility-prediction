import sys
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt


def gen_correlation_matrix(df, unusable_columns, filename):
    simplified_data = df.drop(unusable_columns, axis=1)
    corr_matrix = simplified_data.corr()
    ax = sn.heatmap(corr_matrix, annot=True)
    ax.figure.tight_layout()
    plt.savefig(filename)
    plt.close()

if __name__ == '__main__':
    raw_data = pd.read_csv(sys.argv[1])
    df = pd.DataFrame(raw_data)

    # for all data
    not_used = ["Experiment", "Modifications", "Sequence", "Modified sequence", "Raw file"]
    gen_correlation_matrix(df, not_used, "heatmap_mannbruker_all_columns.png")

    # just ccs and ion scores
    not_used.append("Charge")
    not_used.append("Score")
    not_used.append("Intensity")
    gen_correlation_matrix(df, not_used, "heatmap_mannbruker_simplified.png")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
