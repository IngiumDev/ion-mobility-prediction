import sys
import pandas as pd
import matplotlib.pyplot as plt

def duplicates_mb():
    mb_raw_data = pd.read_csv(sys.argv[1])
    mb_df = pd.DataFrame(mb_raw_data)
    mb_df = mb_df.drop(["Modifications", "Modified sequence", "Charge", "Raw file",
                            "Experiment", "Ion mobility index", "Ion mobility length", "CCS length",
                            "Score", "Intensity"], axis=1)

    mb_df = mb_df.groupby(["Sequence"])
    mb_df_count = mb_df.count()
    mb_df_count["CCS"] = mb_df_count["CCS"] - 1
    maximum_duplicates = mb_df_count["CCS"].max()
    mb_df_count = mb_df_count.rename(columns={"CCS": "Duplicates per Sequence"})
    IQR_count = mb_df_count.quantile(0.75) - mb_df_count.quantile(0.25)
    mb_df_count.boxplot()
    print(mb_df_count.quantile(0.75))
    print(mb_df_count.quantile(0.25))

    plt.savefig("mb_count_same_seq")
    plt.close()

    std_mb_df = mb_df.transform("std")
    std_mb_df = std_mb_df.rename(columns={"CCS": "STD of CCS Values with same Sequence"})
    std_mb_df.boxplot()
    IQR_STD = std_mb_df.quantile(0.75) - std_mb_df.quantile(0.25)
    plt.savefig("mb_std_same_seq")


def duplicates_tw():
    mb_raw_data = pd.read_csv(sys.argv[2])
    mb_df = pd.DataFrame(mb_raw_data)
    mb_df = mb_df.drop(["run", "mass", "charge",
                            "FWHM", "rt", "LiftOffRT", "TouchDownRT",
                            "modification", "type", "score", "mass_dt_err", "intensity"], axis=1)

    mb_df = mb_df.groupby(["sequence"])
    mb_df_count = mb_df.count()
    mb_df_count["dt"] = mb_df_count["dt"] - 1
    maximum_duplicates = mb_df_count["dt"].max()
    mb_df_count = mb_df_count.rename(columns={"dt": "Duplicates per Sequence"})
    IQR_count = mb_df_count.quantile(0.75) - mb_df_count.quantile(0.25)
    mb_df_count.boxplot()
    print(mb_df_count.quantile(0.75))
    print(mb_df_count.quantile(0.25))

    plt.savefig("tw_count_same_seq")

    plt.close()
    std_mb_df = mb_df.transform("std")
    std_mb_df = std_mb_df.rename(columns={"dt": "STD o f DT Values with same Sequence"})
    std_mb_df.boxplot()
    IQR_STD = std_mb_df.quantile(0.75) - std_mb_df.quantile(0.25)
    print(IQR_STD)
    plt.savefig("tw_std_same_seq")



if __name__ == "__main__":
    duplicates_tw()
    duplicates_mb()
