import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn


def gen_correlation_matrix(df, unusable_columns, filename):
    simplified_data = df.drop(unusable_columns, axis=1)
    #simplified_data = simplified_data[["dt", "mass", "charge"]]
    corr_matrix = simplified_data.corr()
    ax = sn.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="crest", linewidths=.5)
    ax.figure.tight_layout()
    plt.title("Mann Bruker Correlations")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


if __name__ == '__main__':
    mb_raw_data = pd.read_csv('../../data/mann_bruker.txt', sep='\t')
    mb_df = pd.DataFrame(mb_raw_data)
    mb_df = mb_df[["CCS", "Mass", "Charge", "Ion mobility index"]]
    # for all data
    not_used = ["Experiment", "Modifications", "Sequence", "Modified sequence", "Raw file"]
    gen_correlation_matrix(mb_df, [], "heatmap_mannbruker_all_columns_new_1.png")

    # just ccs and ion scores
    # not_used.append("Charge")
    # not_used.append("Score")
    # not_used.append("Intensity")
    #gen_correlation_matrix(mb_df, not_used, "heatmap_mannbruker_simplified_new.png")

    # tenzer waters
    #tw_raw_data = pd.read_csv('../../data/tenzer_waters.csv')
    #tw_df = pd.DataFrame(tw_raw_data)
    #not_used = ["run", "sequence", "type", "modification", "LiftOffRT", "TouchDownRT", "intensity", "FWHM", "rt", "score", "mass_dt_err"]
    #gen_correlation_matrix(tw_df, not_used, "tenzer_waters_new_1")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
