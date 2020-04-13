import src.ispot_scrape as ispot
import src.ad_scraper as ad
import sys
import json

def main():
    argv = sys.argv
    if 'data' in argv:
        cfg = json.load(open('config/data-params.json'))
        year = cfg['year']
        superdata = cfg['superdata']
        otherdata = cfg['otherdata']
        datapath = cfg['datapath']
        ispot.scrape_ispot(year, datapath, superdata)
        ad.all_videos(year, otherdata, datapath)
        
if __name__ == "__main__":
    main()