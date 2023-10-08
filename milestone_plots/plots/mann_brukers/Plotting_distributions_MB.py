import pandas as pd
import matplotlib.pyplot as plt
import shutil
import numpy as np
from matplotlib import cm
import matplotlib.patches as patch


# for later download
def save_n_download(pdf_name):
    plt.savefig(pdf_name + ".pdf")
    source_file = pdf_name + ".pdf"
    destination_file = "/Users/mad_hatter/Desktop/Bioinfo/PBL/data/plots/" + pdf_name + ".pdf"
    shutil.copy2(source_file, destination_file)


# load data
mb_path = "/Users/mad_hatter/Desktop/Bioinfo/PBL/data/mann_bruker_simplified.txt"
mann_brukers = pd.read_csv(mb_path, sep=",")
print(mann_brukers.iloc[1], "\n")

# plotting for ion mobility length, first extract counts then plot
ion_mobility_length_counts = mann_brukers["Ion mobility length"].value_counts()
plt.figure(figsize=(8, 6))
ion_mobility_length_counts.plot(kind="bar")
plt.xlabel("Ion mobility length")
plt.ylabel("Count")
plt.title("Ion mobility length distribution")

# Specify the subset of x-axis values to display
subset_values = [40, 70, 100, 130, 160]
subset_positions = [ion_mobility_length_counts.index.get_loc(value) for value in subset_values]
plt.xticks(subset_positions, subset_values, rotation=0)  # Set the subset values and rotate them horizontally
plt.tight_layout()
save_n_download("Ion mobility length")

# summary statistics
print("Summary Statistics for Ion mobility length HERE")
summary_IMI = mann_brukers["Ion mobility length"].describe().round(2)
print(summary_IMI, "\n")

# ion mobility index
ion_mobility_index_counts = mann_brukers["Ion mobility index"].value_counts()
plt.figure(figsize=(8, 6))
ion_mobility_index_counts.plot(kind="bar")
plt.xlabel("Ion mobility index")
plt.ylabel("Count")
plt.title("Ion mobility index distribution")

subset_values = [54, 303, 486, 612, 882]
subset_positions = [ion_mobility_index_counts.index.get_loc(value) for value in subset_values]
plt.xticks(subset_positions, subset_values, rotation=0)  # Set the subset values and rotate them horizontally
plt.tight_layout()
save_n_download("Ion mobility index")

# summary statistics
print("Summary Statistics for Ion mobility index HERE")
summary_IMI = mann_brukers["Ion mobility index"].describe().round(2)
print(summary_IMI, "\n")

# CCS, or Collision Cross-Section, refers to the effective area that an ion occupies during collisions with gas
# molecules in the ion mobility separation process. CCS_counts = mann_brukers["CCS_normalized"].value_counts()
plt.figure(figsize=(8, 6))
mann_brukers.boxplot(column="CCS")
plt.title("CCS distribution boxplot")
save_n_download("CCS boxplot")

# CCS histogram
CCS_counts = mann_brukers["CCS"].value_counts()
plt.figure(figsize=(8, 6))
n, bins, patches = plt.hist(CCS_counts.index, bins=200, align='mid')
plt.xlabel("CCS")
plt.ylabel("Count")
plt.title("CCS distribution")
save_n_download("CCS histogram")


# CCS bar plot by charge
CCS_counts = mann_brukers["CCS"].value_counts()

# Compute the histogram
hist, bin_edges = np.histogram(CCS_counts.index, bins=bins)
majority_charge_states = []
num_colors = len(mann_brukers["Charge"].unique())

# Manually define colors
color_list = ["red", "blue", "green", "yellow"]  # Manually selected colors
# Set up the color map
color_map = cm.get_cmap('tab10', num_colors + 1)

# Create a dictionary to map charge states to colors
charge_colors = {}

# Iterate over each bin
for i in range(len(hist)):
    bin_lower = bins[i]
    bin_upper = bins[i + 1]

    # Subset the data to include only samples within the bin
    subset = mann_brukers[(mann_brukers['CCS'] >= bin_lower) & (mann_brukers['CCS'] < bin_upper)]

    # Check if the subset is empty
    if subset.empty:
        print(f"No samples in bin {i}")
        continue

    # Count the occurrences of each charge state within the subset
    charge_counts = subset['Charge'].value_counts()

    # Print the charge counts for debugging
    print(f"Charge counts for bin {i}: {charge_counts}")

    # Determine the charge state with the highest count
    majority_charge_state = charge_counts.idxmax()
    majority_charge_states.append(majority_charge_state)

    # Get the color corresponding to the majority charge state
    color = color_list[majority_charge_state % num_colors]

    # Plot the bin with the assigned color
    plt.bar(bin_edges[i], hist[i], width=np.diff(bin_edges)[i], color=color)

    # Add the charge state and its corresponding color to the dictionary
    charge_colors[majority_charge_state] = color

plt.xlabel("CCS")
plt.ylabel("Count")
plt.title("CCS distribution by charge state")

# Create a list of legend handles and labels
legend_handles = [patch.Patch(facecolor=color, label=charge_state) for charge_state, color in charge_colors.items()]

# Display the legend
plt.legend(handles=legend_handles, title="Majority Charge States")
save_n_download("CCS histogram charge states")
plt.show()

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
save_n_download("CCS length")

# summary statistics
print("Summary Statistics for CCS length HERE")
summary_IMI = mann_brukers["CCS length"].describe()
print(summary_IMI)
