import src.ispot_scrape as ispot
import src.ad_scraper as ad
import src.ispot_clean as icl
import src.extract_audio_features as ifx
import src.video_processing as vid
import src.vis_video as vis_vid
import src.predictor as pred

import sys
import json

def main():
    argv = sys.argv
        
    if 'data' in argv:
        cfg = json.load(open('config/data-params.json'))
        years = cfg['years']
        superdata = cfg['superdata']
        otherdata = cfg['otherdata']
        datapath = cfg['datapath']
        vizpath = cfg['vizpath']
        ispot.scrape_ispot(years, datapath, superdata)
        ad.all_videos(years, otherdata, datapath)
        vid.dataframe_processor(years, superdata, otherdata, datapath, superdata)
        vid.dataframe_processor(years, superdata, otherdata, datapath, otherdata)
        vis_vid.get_visualizations(superdata, otherdata, datapath, vizpath)
        pred.predict(superdata, otherdata, datapath)
        
    if 'clean' in argv:
        cfg = json.load(open('config/clean-params.json'))
        icl.clean(cfg['rawdatacsv'], cfg['outdir'])
        
    if 'fxt' in argv:
        cfg = json.load(open('config/data-params.json'))
        superdata = cfg['superdata']
        otherdata = cfg['otherdata']
        datapath = cfg['datapath']
        audiodir = cfg['audiodir']
        ifx.extract(datapath, superdata, audiodir)
        ifx.extract(datapath, otherdata, audiodir)
        
    if 'test-project' in argv:
        cfg = json.load(open('config/test-params.json'))
        years = cfg['years']
        superdata = cfg['superdata']
        otherdata = cfg['otherdata']
        datapath = cfg['datapath']
        audiodir = cfg['audiodir']
        vizpath = cfg['vizpath']
        vid.dataframe_processor(years, superdata, otherdata, datapath, superdata)
        vid.dataframe_processor(years, superdata, otherdata, datapath, otherdata)
        ifx.extract(datapath, superdata, audiodir)
        ifx.extract(datapath, otherdata, audiodir)
        vis_vid.get_visualizations(superdata, otherdata, datapath, vizpath)
        pred.predict(superdata, otherdata, datapath)
        
if __name__ == "__main__":
    main()