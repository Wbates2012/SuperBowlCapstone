from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import os


def read_features(datapath, whichdata):
    output_filename = "%s features.csv" % (whichdata)
    output_filename = os.path.join(datapath, output_filename)
    return pd.read_csv((output_filename), index_col=0, keep_default_na=False)


def predict(superdata, otherdata, datapath):
    superdf = read_features(datapath, superdata)
    otherdf = read_features(datapath, otherdata)
    combined = superdf.append(otherdf)
    train, test = train_test_split(df, test_size=0.2)

    clf = LogisticRegression(random_state=0).fit(
        train.drop("words", axis=1), train["issuperbowl"]
    )

    result = test
    result["Prediction"] = clf.predict(test.drop("words", axis=1))
    result["Superbowliness Score"] = [
        i[1] for i in clf.predict_proba(test.drop("words", axis=1))
    ]
    result.to_csv(os.paths.join(datapath, "model results.csv"))
