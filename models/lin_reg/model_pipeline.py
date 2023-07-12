import pickle
import sys
import numpy as np

def run_model(model, mass_table, seq, charge):
    # Load the model from the file
    loaded_model = pickle.load(open(model, 'rb'))
    # Load the mass table from the file
    with open(mass_table, "r") as file:
        loaded_mass_table = {line.strip().split("\t")[0]: line.strip().split("\t")[1] for line in file}
    # Calculate the mass of the sequence
    mass = 0
    for aa in seq:
        mass += float(loaded_mass_table[aa])

    print(mass)
    # Calculate the mass/charge ratio
    mz = mass / int(charge)
    print(mz)
    # Predict the CCS and reverse log
    ccs = np.exp(loaded_model.predict([[mz]]))
    print(ccs[0])


if __name__ == "__main__":
    model = sys.argv[1]
    mass_table = sys.argv[2]
    seq = sys.argv[3]
    charge = sys.argv[4]
    run_model(model, mass_table, seq, charge)
