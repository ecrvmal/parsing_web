# WEB Parsing 
the repo contains 3 folders with scripts for parsing multi-page WEB-sites 
with BeautifulSoup package

# Folder "01_beautifulsoup"
Script Find site title, all links, headers h1, h2 from single site
Output is printing to console

# Folder "01_health-diet"
Script Find all child sites, copies HTML script to local folder,  
Parse data to .csv file and to .json file
Result is stored in local folder "html_data"

# Folder "03_imgs_to_pdf"
Script Find all images from selected div, stores images to local folder.
Also script converts all fetched images to .pdf file
Results stored in local folder "media"

# Stack:
- Python 3.9
  - BS4 BeautifulSoup
  - requests
  - imd2pdf
    
# License
MIT

