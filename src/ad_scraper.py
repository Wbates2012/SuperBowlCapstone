from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os

ADCOUNT = 0  # global variable


def get_video_content(link, otherdata):
    global ADCOUNT
    source = requests.get(link)
    soup = BeautifulSoup(source.text)
    videourl = soup.find("source", {"itemprop": "contentUrl"})["src"]
    videoformat = videourl.split(".")[-1]
    videofilename = "{0}/{1}.{2}".format(otherdata, ADCOUNT, videoformat)
    try:
        response = requests.get(videourl)
        if response.status_code == 200:
            with open(videofilename, "wb") as f:
                f.write(response.content)
    except:
        print("Error with url: " + str(videourl))


def related_videos(brand, year, otherdata, datapath):
    global ADCOUNT
    inputurl = "https://www.adforum.com/creative-work/search?brand=%s&media_strkey=ATX100&location=country_strkey:COU149&yearange=%s-%s&o=relevance"
    baseurl = "https://www.adforum.com"
    formattedurl = inputurl % (brand, year, year)
    source = requests.get(formattedurl)
    soup = BeautifulSoup(source.text)
    links = list()

    for sp in soup.find_all("a", {"class": "b-latest-ads__item__link"}):
        url = baseurl + sp["href"]
        links.append(url)
    data = pd.DataFrame()
    if os.path.exists(datapath):
        if os.path.exists("%s/dataframe.csv" % (datapath)):
            data = pd.read_csv(
                ("%s/dataframe.csv" % (datapath)), index_col=0, keep_default_na=False
            )
    else:
        os.mkdir(datapath)
    otherdata = os.path.join(datapath, otherdata)
    if not os.path.exists(otherdata):
        os.mkdir(otherdata)
    for i in links:
        get_video_content(i, otherdata)
        pagedata = pd.read_html(i)[0]
        metadata = (
            pagedata.set_index(0)
            .T.iloc[0]
            .rename(ADCOUNT)[
                ["Title", "Agency", "Campaign", "Advertiser", "Brand", "Length"]
            ]
        )
        metadata["Year"] = year
        metadata = metadata.groupby(metadata.index).first()
        data = data.append(metadata, sort=False)
        ADCOUNT = ADCOUNT + 1
    data.to_csv("%s/dataframe.csv" % (datapath))

def all_videos(year, otherdata, datapath):
    superdf = pd.read_csv(
        ("%s/%s.csv" % (datapath, year)), index_col=0, keep_default_na=False
    )
    for i in superdf['Advertiser ID']:
        related_videos(i, year, otherdata, datapath)