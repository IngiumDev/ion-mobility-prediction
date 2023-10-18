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

#ccs, dt, mass, im index, seq, charge
def join_datasets(prediction):
    if str(prediction).lower() not in allowed_predictions:
        raise ValueError(f'Can only predict CCS_Z or DT. {str(prediction)} can not be predicted')

    model = joblib.load(prediction_dict[prediction]["model"])
    inputs = prediction_dict[prediction]["inputs"]

    if str(prediction).lower() == "ccs_z":
        data = pd.DataFrame(pd.read_csv(prediction_dict[prediction]["data"]))
        data = data.rename(columns={"mass": "mass_mean"})
        data = data[["charge", "mass_mean", "dt", "sequence"]]
    else:
        data = pd.DataFrame(pd.read_csv(prediction_dict[prediction]["data"], sep="\t"))
        data = data.rename(columns={"Mass": "mass_mean", "Charge": "charge", "Sequence": "sequence"})
        data = data[["charge", "mass_mean", "Ion mobility index", "CCS", "sequence"]]

    data = data.drop_duplicates(subset=["charge", "sequence"], keep="last")
    inner_join = pd.DataFrame(pd.read_csv('../data/merged_data.csv'))
    inner_join = inner_join.drop_duplicates(subset=["charge", "sequence"], keep="last")
    right_outer = inner_join.merge(data, how="right", indicator=True)
    right_outer = right_outer[right_outer["_merge"] == "right_only"]

    right_outer[prediction] = model.predict(data[inputs])

    if str(prediction).lower() == "ccs_z":
        std_and_mean = pd.read_csv("ccs_mean_std.csv")
        ccs_mean = std_and_mean["ccs_mean"][0]
        ccs_std = std_and_mean["ccs_std"][0]
        right_outer["CCS"] = right_outer[prediction] * ccs_std + ccs_mean

    full_data = right_outer.merge(inner_join, how="outer")
    full_data = full_data.drop("_merge", axis=1)
    full_data.to_csv("full.csv", index=False)


if __name__ == "__main__":
    # use ccs_z or dt as parameter
    join_datasets("ccs_z")
