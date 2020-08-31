#### *What Makes a Super Bowl Commercial Super?*
* Group members: Chatson Frankenberg, William Bates
* Contact email: cfranken, wbates (@ucsd.edu)

Materials: 
* [Website](https://furbeh.github.io/SuperBowlCapstoneWebPage/)
* [Presentation](https://vimeo.com/430842102)
* [Project Report](https://drive.google.com/file/d/1FgO24ujWUXjq8vkLYdiR3ezzCbOutoCW/view)

Abstract: The Super Bowl is annually the most watched television program, which means companies are willing to spend up to $5.6 million for a mere 30 seconds of the nation’s attention. In parallel to the financial evidence, the commercials have been described anecdotally as “ambitious”, “notorious”, and “must-have guests [to the main event]”. The cultural phenomenon of the Super Bowl commercial is well-recognized. Thus, the cultural analytics question becomes how modern data analysis techniques can help us to better decipher what makes these commercials so special and generally abnormal. To generate these results, we analyzed quantitative differences between television commercials that air during the Super Bowl and those that air any other time. As a branch of cultural analytics, this project seeks to determine the capability of data processing to validate or otherwise opine on the social consensus regarding the commercials. Our project will be more focused on the social dynamics of the commercials. We have analyzed a decade worth of Super Bowl commercials, comparing them to counterparts in visual and auditory attributes. Using techniques such as shot detection, spectral transformations, and text analysis, this project offers a complete discussion of the concept of attention-getting in advertising from an analytical viewpoint.

# Project Repository Description below:

# SuperBowlCapstone

Collects superbowl and non-superbowl commercials from ispot and adforum respectively.
Generates features from their audio and video content
Builds multiple models based off of the generated features.
Creates multiple visualizations.

## Usage Instructions

Potential run.py arguments:
* data: does the webscraping
* fxt: feature extraction, requires data to be run
* analyze: model and visual generation, requires fxt to be run
* test-project: using given test commercials, tests project.

## Project Contents

```
ROOT FOLDER
├── .gitignore
├── README.md
├── config
│   ├── data-params.json
│   ├── test-params.json
│   └── env.json
├── chosen data folder
│   ├── chosen superbowl commercial folder
│   │   └── chosen audio folder
│   └── chosen non-superbowl commercial folder
│       └── chosen audio folder
├── notebooks
│   └── .gitkeep
├── run.py
└── src
    └── etl.py
```

### `src`

* `ad_scraper.py`: Library code that collects non-superbowl commercials from adforum based off of collected superbowl commercials.
* `ispot_scrape.py`: Library code that collects superbowl commercials from ispot.
* `video_processing.py`: Library code that generates visual features.
* `extract_audio_features.py`: Library code that generates audio features.
* `vis_video.py`: Library code that generates visualizations for generated features.
* `predictor.py`: Library code that generates predictions from Logistic Regression and Random Forest models.

### `config`

* `data-params.json`: Common parameters for getting data, serving as
  inputs to library code.
  
* `test-params.json`: parameters for running small process on small
  test data.

### `notebooks`

* Jupyter notebooks for analysis, mainly audio-orientated.
