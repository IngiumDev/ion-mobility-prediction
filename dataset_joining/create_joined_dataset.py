import sys
import joblib
import pandas as pd

allowed_predictions = ["ccs_z", "dt"]
prediction_dict = {"ccs_z": {"model": "../dataset_joining/correlation_curves/predict_ccs.pkl",
                           "data": "../data/tenzer_waters.csv",
                           "inputs": ["charge", "mass_mean", "dt"]},
                   "dt": {"model": "../dataset_joining/correlation_curves/predict_dt.pkl",
                          "data": "../data/mann_bruker.txt",
                          "inputs": ["charge", "mass_mean", "Ion mobility index", "CCS"]}}


def join_datasets(prediction):
    if str(prediction).lower() not in allowed_predictions:
        raise ValueError(f'Can only predict CCS_Z or DT. {str(prediction)} can not be predicted')

    data = pd.DataFrame()
    model = joblib.load(prediction_dict[prediction]["model"])
    inputs = prediction_dict[prediction]["inputs"]

    if str(prediction).lower() == "ccs_z":
        data = pd.DataFrame(pd.read_csv(prediction_dict[prediction]["data"]))
        data = data.rename(columns={"mass": "mass_mean"})
    else:
        data = pd.DataFrame(pd.read_csv(prediction_dict[prediction]["data"], sep="\t"))
        data = data.rename(columns={"Mass": "mass_mean", "Charge": "charge"})

    #merged_data = pd.DataFrame(pd.read_csv('../data/merged_data.csv'))
    data[prediction] = model.predict(data[inputs])

    if str(prediction).lower() == "ccs_z":
        std_and_mean = pd.read_csv("ccs_mean_std.csv")
        ccs_mean = std_and_mean["ccs_mean"][0]
        ccs_std = std_and_mean["ccs_std"][0]
        data["ccs"] = data[prediction] * ccs_std + ccs_mean

    print(data)


if __name__ == "__main__":
    join_datasets("ccs_z")
