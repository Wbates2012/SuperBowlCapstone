from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import urllib
import urllib.request
import os
import numpy as np


def get_page_links(year):

    # HTML of search page
    search_page = "https://www.ispot.tv/events/" + str(year) + "-super-bowl-commercials"
    doc = requests.get(search_page)
    soup = BeautifulSoup(doc.text)

    # Pull video page url with bs4 and regex
    pat = '"/ad/.+" '
    base_link = "http://www.ispot.tv"
    links = list()
    for sp in soup.find_all("div", {"class": "thumbnail--event thumbnail mb-0"}):
        addon = list(sp)[1]["href"]
        link = base_link + addon
        links.append(link)
    return links


def extract_data(link):
    doc = requests.get(link)
    soup = BeautifulSoup(doc.text)

    if len(soup.find_all("div", {"class": "jwplayer"})) < 1:  # Check if video exists
        return np.full(8, np.NaN)  # If not, return NaNs
    inner = [soup.find_all("div", {"class": "jwplayer"})[0]["data-mp4"]]  # Video link
    inner.append(soup.find_all("meta", {"itemprop": "name"})[0]["content"])  # Title
    inner.append(
        soup.find_all("meta", {"itemprop": "duration"})[0]["content"]
    )  # Duration
    inner.append(soup.find_all("meta", {"name": "ad_id"})[0]["content"])  # Ad ID
    inner.append(
        soup.find_all("meta", {"name": "ad_advertiser_id"})[0]["content"]
    )  # Advertiser ID
    inner.append(
        soup.find_all("meta", {"name": "ad_subcategory_id"})[0]["content"]
    )  # Subcategory ID
    inner.append(
        soup.find_all("meta", {"name": "ad_est_firstoccur"})[0]["content"]
    )  # First occurance date
    inner.append(
        soup.find_all("meta", {"name": "ad_est_lastoccur"})[0]["content"]
    )  # Last occurance date
    inner.append(
        soup.find_all("div", {"class": "col-12 mb-3 pl-0"})[0].find("a").text.strip()
    ) # Brand Name

    return inner


def create_df(data):
    return pd.DataFrame(
        data,
        columns=[
            "mp4",
            "Title",
            "Duration",
            "Ad ID",
            "Advertiser ID",
            "Subcategory ID",
            "First Occurance",
            "Last Occurance",
            "Brand"
        ],
    )


##############################################

# Year is year of analysis
# superdata is something like 'videos'
def scrape_ispot(year, datapath, superdata):

    if datapath:
        if not os.path.exists(datapath):
            os.makedirs(datapath)
    video_pages = get_page_links(year)

    data = list()
    for url in video_pages:
        data.append(extract_data(url))
    df = create_df(data)

    # Download metadata as CSV
    name = str(year) + ".csv"
    out_df = os.path.join(datapath, name)
    df.to_csv(out_df)

    # Download videos by ad-ID
    superdata = os.path.join(datapath, superdata)
    if not os.path.exists(superdata):
        os.makedirs(superdata)
    for i in range(len(df)):
        video = df["mp4"][i]
        name = str(df["Ad ID"][i]) + ".mp4"
        outlink = os.path.join(superdata, name)
        urllib.request.urlretrieve(video, outlink)
