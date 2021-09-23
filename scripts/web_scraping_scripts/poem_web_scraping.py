import os
import requests
from bs4 import BeautifulSoup

"""
STEPS:
- Get links to all poems on the page
- Get poems from the links
- save them all as text files
"""
# setting poems path where to save poems later
poems_directory = "/Users/rachelberryman/Desktop/DSR_Intro_to_Python/Intro_to_Python_DSR/text_files"
# getting homepage HTML.
# From here, will extract all links
response = requests.get('https://poestories.com/poetry.php')
soup = BeautifulSoup(response.text)
link_section = [link for link in soup.find_all('a')]
true_links = [link['href'] for link in link_section[1:]]
# looking at the website, the links to the other poems all start with "read/"
corrected_links = [link for link in true_links if "read" in link]

for link in corrected_links:
    print(link)
    poem_response = requests.get('https://poestories.com/' + link)
    poem_soup = BeautifulSoup(poem_response.text, 'html.parser')
    try:
        # pulling out the poem section from the soup
        container = poem_soup.findAll("p", attrs= {"class": "poem"})[0]
        # converting blob of text to string, to be able to filter
        text = str(container)
        text = text.replace("<br/>", "")
        text = text.split('<p class="poem">')[1]
        text = text.split('<span ')[0]
        # getting the last part of the link name, which is the poem name
        name = link.split("/")[2]
        filename = name  + "_poem.txt"
        with open(os.path.join(poems_directory, filename), 'w') as f:
            f.write(text)
    except IndexError:
        print(f'poem {link.split("/")[2]} could not be scraped')
