import pandas as pd
import matplotlib.pyplot as plt
import shutil

from Tools.scripts.var_access_benchmark import C


def plots():
    # load data
    tenzer_waters = pd.read_csv("tenzer_waters.csv")
    print(tenzer_waters)
    mb_path = "mann_bruker_simplified.txt"
    mann_brukers = pd.read_csv(mb_path, sep=",")

    print(mann_brukers.iloc[1], "\n")

    # min - max normalize CCS and CCS length values - really not used but just in case for later
    mann_brukers["CCS_normalized"] = mann_brukers["CCS"] - mann_brukers["CCS"].min() / mann_brukers["CCS"].max() - \
                                     mann_brukers["CCS"].min()

    # plotting for ion mobility length, first extract counts then plot
    ion_mobility_length_counts = mann_brukers["Ion mobility length"].value_counts()
    plt.figure(figsize=(8, 6))
    ion_mobility_length_counts.plot.hist(bins=9)
    plt.xlabel("Ion mobility length")
    plt.ylabel("Count")
    plt.title("Ion mobility length distribution")

    # Specify the subset of x-axis values to display
    #subset_values = [40, 70, 100, 130, 160]
    #subset_positions = [ion_mobility_length_counts.index.get_loc(value) for value in subset_values]
    #plt.xticks(subset_positions, subset_values, rotation=0)  # Set the subset values and rotate them horizontally
    plt.tight_layout()
    # plt.show()

    # Save the plot as a PDF file and download
    # plt.savefig('Ion mobility length.pdf')
    #source_file = 'Ion mobility length.pdf'
    #destination_file = "Ion mobility length.pdf"
    #shutil.copy2(source_file, destination_file)

    # summary statistics
    print("Summary Statistics for Ion mobility length HERE")
    summary_IMI = mann_brukers["Ion mobility length"].describe().round(2)
    print(summary_IMI, "\n")

    # ion mobility index - is the same as drift time!
    ion_mobility_index_counts = mann_brukers["Ion mobility index"].value_counts()
    plt.figure(figsize=(8, 6))
    ion_mobility_index_counts.plot.hist(bins=20)

    plt.xlabel("Ion mobility index")
    plt.ylabel("Count")
    plt.title("Ion mobility index distribution")


    plt.tight_layout()
    plt.show()

    # Save the plot as a PDF file
    # plt.savefig('Ion mobility index.pdf')
    #source_file = 'Ion mobility index.pdf'
    #destination_file = "Ion mobility index.pdf"
    #shutil.copy2(source_file, destination_file)

    # summary statistics
    print("Summary Statistics for Ion mobility index HERE")
    summary_IMI = mann_brukers["Ion mobility index"].describe().round(2)
    print(summary_IMI, "\n")

    # CCS, or Collision Cross-Section, refers to the effective area that an ion occupies during collisions with gas
    # molecules in the ion mobility separation process. CCS_counts = mann_brukers["CCS_normalized"].value_counts()
    plt.figure(figsize=(8, 6))
    mann_brukers.boxplot(column="CCS")
    plt.title("CCS distribution boxplot")
    plt.show()

    # Save the plot as a PDF file and download
    # plt.savefig('CCS.pdf')
    #source_file = 'CCS.pdf'
    #destination_file = "CCS.pdf"
    #shutil.copy2(source_file, destination_file)

    # summary statistics
    print("Summary Statistics for CCS HERE")
    summary_IMI = mann_brukers["CCS"].describe()
    print(summary_IMI, "\n")

    # CCS length, or Collision Cross-Section Length, refers to the physical length or extent of an ion along
    # the drift path in an ion mobility cell. It represents the distance that an ion travels during the ion mobility
    # separation process. CCS_length_counts = mann_brukers["CCS length"].value_counts()
    plt.figure(figsize=(8, 6))
    mann_brukers.boxplot(column="CCS length")
    plt.title("CCS length distribution boxplot")
    plt.show()

    # Save the plot as a PDF file and download
    # plt.savefig('CCS length.pdf')
    #source_file = 'CCS length.pdf'
    # = "CCS length.pdf"
    #shutil.copy2(source_file, destination_file)

    # summary statistics
    print("Summary Statistics for CCS length HERE")
    summary_IMI = mann_brukers["CCS length"].describe()
    print(summary_IMI)


if __name__ == "__main__":
    plots()
