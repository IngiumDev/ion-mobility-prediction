import sys
import pandas as pd
import matplotlib.pyplot as plt


def duplicates_mb():
    mb_raw_data = pd.read_csv("../../data/mann_bruker_simplified.csv")
    mb_df = pd.DataFrame(mb_raw_data)
    mb_df = mb_df[["Sequence", "CCS", "Charge"]]
    mb_df = mb_df.groupby(["Sequence", "Charge"])
    mb_df_count = mb_df.count()
    mb_df_count["CCS"] = mb_df_count["CCS"] - 1
    maximum_duplicates = mb_df_count["CCS"].max()
    mb_df_count = mb_df_count.rename(columns={"CCS": "Mann Bruker"})
    IQR_count = mb_df_count.quantile(0.75) - mb_df_count.quantile(0.25)
    mb_df_count.boxplot()
    print(mb_df_count.quantile(1))
    print(mb_df_count.quantile(0.54125))

    plt.ylabel("Duplicates per Sequence and Charge")
    plt.savefig("mb_count_same_seq")
    plt.close()

    std_mb_df = mb_df.transform("std")
    std_mb_df = std_mb_df.rename(columns={"CCS": "Mann Bruker"})
    plt.ylabel("STD of CCS Values with same Sequence and Charge")
    std_mb_df.boxplot()
    IQR_STD = std_mb_df.quantile(0.75) - std_mb_df.quantile(0.25)
    #plt.savefig("mb_std_same_seq")


def duplicates_tw():
    tw_raw_data = pd.read_csv("../../data/tenzer_waters.csv")
    tw_df = pd.DataFrame(tw_raw_data)
    tw_df = tw_df[["sequence", "charge", "dt"]]

    tw_df = tw_df.groupby(["sequence", "charge"])
    tw_df_count = tw_df.count()
    tw_df_count["dt"] = tw_df_count["dt"] - 1
    maximum_duplicates = tw_df_count["dt"].max()
    tw_df_count = tw_df_count.rename(columns={"dt": "Tenzer Waters"})
    IQR_count = tw_df_count.quantile(0.75) - tw_df_count.quantile(0.25)
    tw_df_count.boxplot()
    print("------------")
    print(tw_df_count.quantile(0.74))
    print("------------")
    plt.ylabel("Duplicates per Sequence and Charge")
    plt.savefig("tw_count_same_seq_new_test")

    plt.close()
    std_tw_df = tw_df.transform("std")
    std_tw_df = std_tw_df.rename(columns={"dt": "STD of DT Values with same Sequence"})
    std_tw_df.boxplot()
    IQR_STD = std_tw_df.quantile(0.75) - std_tw_df.quantile(0.25)
   # print(IQR_STD)

    #plt.savefig("tw_std_same_seq")


if __name__ == "__main__":
    duplicates_tw()
    duplicates_mb()
