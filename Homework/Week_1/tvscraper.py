#!/usr/bin/env python
# Name: Brent Kok
# Student number: 10725156
"""
This script scrapes IMDB and outputs a CSV file with highest rated tv series.
"""

import csv
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series"
BACKUP_HTML = 'tvseries.html'
OUTPUT_CSV = 'tvseries.csv'


def extract_tvseries(dom):
    """
    Extract a list of highest rated TV series from DOM (of IMDB page).
    Each TV series entry should contain the following fields:
    - TV Title
    - Rating
    - Genres (comma separated if more than one)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """
    w = requests.get(TARGET_URL)
    x = BeautifulSoup(w.text, "html.parser")

    movies = x.find_all('div', class_='lister-item mode-advanced')

    title = []
    rating = []
    genre = []
    actor = []
    runtime = []


    for i in movies:
        title.append(i.h3.a.text)
        rating.append(i.strong.text)
        genre.append(i.find('span', class_='genre').text.split())
        runtime.append(i.find('span', class_='runtime').text.strip(" min"))
        imdbactor1 = i.find_all('p')[2]
        imdbactor = imdbactor1.find_all('a')
        series_actors = []
        for i in imdbactor:
            series_actors.append(i.text)
        actor.append(series_actors)


    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED TV-SERIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

#def save_csv(outfile, tvseries):
    """
    Output a CSV file containing highest rated TV-series.
    """
    file = open("tvseries.csv", "w")
    writer = csv.writer(file)   
    writer.writerow(['Title', 'Rating', 'Genre', 'Actors', 'Runtime'])
    for i in range(50):
        writer.writerow((title[i], rating[i], ''.join(map(str, genre[i])), ','.join(actor[i]), runtime[i]))
    file.close()

    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE TV-SERIES TO DISK


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the tv series (using the function you implemented)
    tvseries = extract_tvseries(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, tvseries)
