import src.ispot_scrape as ispot
import src.ad_scraper as ad
import src.ispot_clean as icl
import src.extract_audio_features as ifx

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
        
    if 'clean' in argv:
        cfg = json.load(open('config/clean-params.json'))
        icl.clean(cfg['rawdatacsv'], cfg['outdir'])
        
    if 'fxt' in argv:
        cfg = json.load(open('config/fxt-params.json'))
        ifx.extract(cfg['audiodir'], cfg['cleandatadir'], cfg['outdir'])
        
    if 'test' in argv:
        cfg = json.load(open('config/test-params.json'))
        ifx.extract(cfg['audiodir'], cfg['cleandatadir'], cfg['outdir'])
        
if __name__ == "__main__":
    main()
