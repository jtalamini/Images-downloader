from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import sys
import urllib

options = Options()
options.add_argument("headless")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)

query = ""

if len(sys.argv) < 2:
    print "no argument provided.."
    exit(1)

else:
    for arg in sys.argv[1:]:
        query += arg+"+"


driver.get("http://www.google.com/search?q="+query)
a_list = driver.find_elements_by_tag_name("a")
for a in a_list:
    if a.get_attribute("class") == "q qs":
        a.click()
        break
time.sleep(2)

SCROLL_PAUSE_TIME = 0.5
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
SCROLLS = 5
for s in range(SCROLLS):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# get more results
inputs = driver.find_elements_by_tag_name("input")
for inpt in inputs:
    if inpt.get_attribute("type") == "button":
        inpt.click()
        break

for s in range(SCROLLS):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

images = driver.find_elements_by_tag_name("img")
index = 0

folder = query.replace("+", "_")
if os.path.exists(folder):
    os.remove(folder)
else:
    os.mkdir(folder)

for i in images:
    if i.get_attribute("class") == "rg_ic rg_i":
        src = ""
        try:
            src = i.get_attribute("src")
            if src is not None:
                str_src = src.encode("ascii", "ignore").lower()

                filename = folder+"/"+str(index)
                urllib.urlretrieve(src, filename)
                index += 1
        except: print src


