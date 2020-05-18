import pandas as pd
import os
import plotly.graph_objects as go
import numpy as np


def read_features(datapath, whichdata):
    output_filename = "%s features.csv" % (whichdata)
    output_filename = os.path.join(datapath, output_filename)
    return pd.read_csv((output_filename), index_col=0, keep_default_na=False)


def histvis(combined, feature, vispath):
    superbowl = combined[combined["issuperbowl"] == 1][feature]
    notsuperbowl = combined[combined["issuperbowl"] == 0][feature]

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=superbowl, name="Superbowl", histnorm="probability"))
    fig.add_trace(
        go.Histogram(x=notsuperbowl, name="Non-Superbowl", histnorm="probability")
    )

    fig.update_layout(title_text=feature.title())
    fig.write_image(os.path.join(vispath, "%s histogram.png" % (feature)))
    # fig.show(renderer="png")


def get_visualizations(superdata, otherdata, datapath, vizpath):
    if not os.path.exists(vizpath):
        os.mkdir(vizpath)
    superdf = read_features(datapath, superdata)
    otherdf = read_features(datapath, otherdata)

    combined = superdf.append(otherdf)
    for i in combined.columns:
        histvis(combined, i, vizpath)
