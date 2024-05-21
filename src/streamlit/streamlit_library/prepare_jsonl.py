import pandas as pd
import json


# -----------------------------------------------------------------------------
def delecte_dict(data):
    """
    Remove dict-like objects from a dictionnary.
    Specified keys to delete:
        - input_features,
        - estimator_parameters,
        - feature_importances
    Args:
        - data: a dictionnary containing dict-like object.
    Return:
        - the same dictionnary without the dict-like objects.
    """
    dicts_to_delete = [
        "input_features",
        "estimator_parameters",
        "feature_importances"
    ]
    for entry in dicts_to_delete:
        if entry in data:
            del data[entry]
    return data


# -----------------------------------------------------------------------------
def jsonl_to_df(data_jsonl):
    """
    Take a requested jsonl, remove all dict-like objects in it,
    and return a dataframe.
    Args:
        - data_jsonl: a list of dictionnaries with the same keys
    Return:
        -df a dataframe pandas object
    """
    new_jsonl = []
    for line in data_jsonl:
        data_json = delecte_dict(line)
        new_jsonl.append(data_json)

    # Ouvrir un fichier en mode écriture
    with open('data.jsonl', 'w') as file:
        for data in new_jsonl:
            # Convert data in json string and save it inside file:
            file.write(json.dumps(data) + '\n')

    df = pd.read_json('data.jsonl', lines=True)
    df['request_id'] = df['request_id'].astype("str")

    return df
