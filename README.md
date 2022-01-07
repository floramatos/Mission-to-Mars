# Gathering and Visualizing data on the Mission to Mars
Data related to the Mission to Mars was retrieved using a Flask web application, stored in a MongoDB database and visualized in a HTML page.

## Overview
The goal of this project was to create a Flask web application to scrape different websites containing data on the mission to Mars.

### Resources
- Python
- Jupiter Notebook
- Flask
- MongoDB
- HTML

## Results
Four different websites were scraped:
1. From https://redplanetscience.com, information about the latest media news related to the Mission to Mars is scraped. Specifically, the latest news title and its description paragraph is retrieved.
2. From https://spaceimages-mars.com, the current Featured Mars image is scraped.
3. From https://galaxyfacts-mars.com, a table comparing Mars and Earth on multiple facts is retrieved.
4. Finally, from https://marshemispheres.com/, high resolution images for each of Mar's hemispheres are scraped.

All the above scraped information was stored in a MongoDB database and is displayed in the following HTML page:
![Screen Shot 2022-01-07 at 1 21 53 PM](https://user-images.githubusercontent.com/89421440/148611964-9c28f887-b9d0-494a-94b4-0b77237c4c02.png)



