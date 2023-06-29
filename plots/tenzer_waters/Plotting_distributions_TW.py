import pandas as pd
import matplotlib.pyplot as plt
import shutil

# load data
tenzer_waters = pd.read_csv("/Users/mad_hatter/Desktop/Bioinfo/PBL/data/tenzer_waters.csv")
print(tenzer_waters.iloc[1], "\n")


# for later download
def save_n_download(pdf_name):
    plt.savefig(pdf_name + ".pdf")
    source_file = pdf_name + ".pdf"
    destination_file = "/Users/mad_hatter/Desktop/Bioinfo/PBL/data/plots/" + pdf_name + ".pdf"
    shutil.copy2(source_file, destination_file)


# Drift time histogram
dt_counts = tenzer_waters["dt"].value_counts()
plt.figure(figsize=(8, 6))
n, bins, patches = plt.hist(dt_counts.index, bins=200, align='mid')

plt.xlabel("drift time")
plt.ylabel("Count")
plt.title("Drift time distribution")
save_n_download("Drift time histogram")

# Drift time boxplots
plt.figure(figsize=(8, 6))
tenzer_waters.boxplot(column="dt")
plt.title("drift time distribution boxplot")
save_n_download("Drift time boxplot")

# summary statistics
print("Summary Statistics for drift time HERE")
summary_IMI = tenzer_waters["dt"].describe().round(2)
print(summary_IMI, "\n")

# Mass histogram
mass_counts = tenzer_waters["mass"].value_counts()
plt.figure(figsize=(8, 6))
n, bins, patches = plt.hist(mass_counts.index, bins=200, align='mid')
# Set x-axis tick positions and labels
plt.xticks(bins)
plt.gca().set_xticks(bins[::20])  # Set tick positions to every second bin

plt.xlabel("mass")
plt.ylabel("Count")
plt.title("mass distribution")
save_n_download("Mass histogram")

# Mass boxplot
plt.figure(figsize=(8, 6))
tenzer_waters.boxplot(column="mass")
plt.title("mass distribution boxplot")
save_n_download("Mass boxplot")

# summary statistics
print("Summary Statistics for Mass HERE")
summary_IMI = tenzer_waters["mass"].describe().round(2)
print(summary_IMI, "\n")

# Charge boxplot
plt.figure(figsize=(8, 6))
tenzer_waters.boxplot(column="charge")
plt.title("charge distribution boxplot")
save_n_download("Charge boxplot")

# summary statistics
print("Summary Statistics for Charge HERE")
summary_IMI = tenzer_waters["charge"].describe()
print(summary_IMI, "\n")

# Score histogram
score_counts = tenzer_waters["score"].value_counts()
plt.figure(figsize=(8, 6))
n, bins, patches = plt.hist(score_counts.index, bins=200, align='mid')

plt.xlabel("Score")
plt.ylabel("Count")
plt.title("Score distribution")
save_n_download("Score histogram")

# Score boxplot
plt.figure(figsize=(8, 6))
tenzer_waters.boxplot(column="score")
plt.title("score distribution boxplot")
save_n_download("Score boxplot")

# summary statistics
print("Summary Statistics for score HERE")
summary_IMI = tenzer_waters["score"].describe()
print(summary_IMI)
