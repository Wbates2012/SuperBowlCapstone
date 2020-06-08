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
    combined = combined.drop('words', axis=1)
    combined = combined.drop('ID', axis=1)
    train, test = train_test_split(combined, test_size=0.2)
    train_y = train['issuperbowl']
    train = train.drop('issuperbowl', axis=1)

    clf = LogisticRegression(random_state=0).fit(train, train_y)

    result = test
    test_y = test['issuperbowl']
    test = test.drop('issuperbowl', axis=1)
    result['Prediction'] = clf.predict(test)
    result['Superbowliness Score'] = [i[1] for i in clf.predict_proba(test)]
    result.to_csv(os.path.join(datapath, 'model results.csv'))