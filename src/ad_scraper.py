from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os


def get_video_content(link, name, datapath, otherdata):
    print(link)
    source = requests.get(link)
    soup = BeautifulSoup(source.text)
    try:
        videourl = soup.find("source", {"itemprop": "contentUrl"})["src"]
        videoformat = videourl.split(".")[-1]
        if videoformat != 'mp4':
            return None
        videofilename = os.path.join(datapath, otherdata, "%s.%s" % (name, videoformat))
    except:
        print("Error with webpage: " + str(link))
        return None
    try:
        response = requests.get(videourl)
        if response.status_code == 200:
            with open(videofilename, "wb") as f:
                f.write(response.content)
    except:
        print("Error with url: " + str(videourl))


def related_videos(brand, year, otherdata, datapath):
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
        if os.path.exists(os.path.join(datapath, "other dataframe.csv")):
            data = pd.read_csv(
                os.path.join(datapath, "other dataframe.csv"),
                index_col=0,
                keep_default_na=False,
            )
    else:
        os.mkdir(datapath)
    otherdata = os.path.join(datapath, otherdata)
    if not os.path.exists(otherdata):
        os.mkdir(otherdata)
    for i in links:
        pagedata = pd.read_html(i)[0]
        pagedata = pagedata.set_index(0).T.reset_index(drop=True).iloc[0]
        metadata = (
            pagedata.groupby(pagedata.index)
            .first()
            .reindex(["Title", "Agency", "Campaign", "Advertiser", "Brand", "Length"])
        )
        metadata["Year"] = year
        metadata["URL"] = i
        metadata = metadata.groupby(metadata.index).first()
        data = data.append(metadata, sort=False)
    data.to_csv(os.path.join(datapath, "other dataframe.csv"))


def download_videos(otherdata, datapath):
    sampler = pd.read_csv(
        os.path.join(datapath, "other dataframe.csv"),
        index_col=0,
        keep_default_na=False,
    )
    sampler = sampler.reset_index(drop=True)
    sampler.to_csv(os.path.join(datapath, "other dataframe.csv"))
    for i, j in sampler.iterrows():
        get_video_content(j["URL"], i, datapath, otherdata)


def expandyear(l):
    expanded = []
    for year in l:
        year = int(year)
        for i in range(year - 1, year + 2):
            if i > 2020:
                continue
            expanded.append(i)
    # Unique values only
    return list(dict.fromkeys(expanded))


def all_videos(years, otherdata, datapath):
    # add one year more and one year less
    superdf = pd.read_csv(
        os.path.join(datapath, "superbowl.csv"), index_col=0, keep_default_na=False
    )
    for i in superdf.groupby("Brand")["Year"].apply(list).iteritems():
        brand = i[0]
        yearrange = expandyear(i[1])
        for year in yearrange:
            related_videos(brand, year, otherdata, datapath)
    download_videos(otherdata, datapath)
