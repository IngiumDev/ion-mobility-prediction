import pickle

import numpy as np
import pandas as pd
# Duplicate handle for MB TW
# Append data from TW on MB
# Group identical sequences and Charge like we did for second milestone
# predict the missing values (CCS, DT)
def join_dataset(mb, tw,ccs_sd, rfccsmodel, rfdtmodel):
    # Load the data
    mb_data = pd.read_csv(mb, sep='\t')
    # Keep only necessary columns
    mb_data = mb_data[['Sequence', 'CCS', 'Mass', 'Charge', 'Length', 'Ion mobility index']]
    # Group by 'Sequence' and 'Charge', and calculate median of 'Mass' and 'CCS'
    mb_data = mb_data.groupby(['Sequence', 'Charge']).agg(
        {'Mass': 'median', 'CCS': 'median', 'Length': 'median', 'Ion mobility index': 'median'}).reset_index()

    # Load the data
    tw_data = pd.read_csv(tw, sep=',')
    # Keep only necessary columns
    tw_data = tw_data[['sequence', 'dt', 'mass', 'charge']]
    # Add Length column
    tw_data['length'] = tw_data['sequence'].str.len()
    # Rename columns
    tw_data.columns = ['Sequence', 'dt', 'Mass', 'Charge', 'Length']
    # Group by 'Sequence' and 'Charge', and calculate median of 'Mass' and 'dt'
    tw_data = tw_data.groupby(['Sequence', 'Charge']).agg({'Mass': 'median', 'dt': 'median', 'Length': 'median'}).reset_index()

    # Append the two dataframes
    data = pd.concat([mb_data, tw_data], ignore_index=True)

    # Group by 'Sequence' and 'Charge', and calculate median of 'Mass', 'Length', 'CCS', and 'dt'
    data = data.groupby(['Sequence', 'Charge']).agg(
        {'Mass': 'median',
         'Length': 'median',
         'CCS': 'median',
         'dt': 'median', 'Ion mobility index' : 'median'}).reset_index()

    # Load in the two models with pickle (scikit.learn random forest regressor)
    ccs_model = pickle.load(open(rfccsmodel, 'rb'))
    dt_model = pickle.load(open(rfdtmodel, 'rb'))
    # Predict the missing values (for CCS: use Charge, Mass, DT) (for DT: Charge, Mass, IM-Index, CCS)
    # Identify rows with missing CCS values
    missing_ccs = data['CCS'].isna()

    # Prepare the features for the rows with missing CCS values
    X_ccs = data.loc[missing_ccs, ['Charge', 'Mass', 'dt']]
    # Temporarily rename Charge to charge, Mass to mass_mean
    X_ccs.columns = ['charge', 'mass_mean', 'dt']
    # Predict the missing CCS values
    predicted_ccs = ccs_model.predict(X_ccs)
    # Reverse the z-score normalization
    std_and_mean = pd.read_csv(ccs_sd)
    ccs_mean = std_and_mean["ccs_mean"][0]
    ccs_std = std_and_mean["ccs_std"][0]
    predicted_ccs = predicted_ccs * ccs_std + ccs_mean

    # Rename the columns back to their original names
    X_ccs.columns = ['Charge', 'Mass', 'dt']

    # Fill in the missing CCS values in the dataframe
    data.loc[missing_ccs, 'CCS'] = predicted_ccs

    # Repeat the process for the 'dt' column
    missing_dt = data['dt'].isna()
    X_dt = data.loc[missing_dt, ['Charge', 'Mass', 'Ion mobility index', 'CCS']]
    # Temporarily rename Charge to charge, Mass to mass_mean
    X_dt.columns = ['charge', 'mass_mean', 'Ion mobility index', 'CCS']
    predicted_dt = dt_model.predict(X_dt)
    # Rename the columns back to their original names
    X_dt.columns = ['Charge', 'Mass', 'Ion mobility index', 'CCS']
    data.loc[missing_dt, 'dt'] = predicted_dt

    # Save the dataframes to csv
    data.to_csv('joined_dataset.csv', index=False)

if __name__ == '__main__':
    join_dataset('../data/mann_bruker.txt', '../data/tenzer_waters.csv', '../dataset_joining/ccs_mean_std.csv', '../dataset_joining/correlation_curves/predict_ccs.pkl', '../dataset_joining/correlation_curves/predict_dt.pkl')