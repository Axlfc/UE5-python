# coding=utf-8
import sys
import requests
import urllib
from requests_html import HTMLSession


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.',
                      'https://google.',
                      'https://webcache.googleusercontent.',
                      'http://webcache.googleusercontent.',
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links


def get_results(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)

    return response


def parse_results(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    results = response.html.find(css_identifier_result)

    output = []

    for result in results:
        item = {
            'link': result.find(css_identifier_link, first=True).attrs['href']
        }

        output.append(item)

    return output


def google_search(query):
    return parse_results(get_results(query))


def main():
    result = google_search(sys.argv[1])
    links = []
    for line in result:
        links.append(line["link"])

    for link in range(len(links)):
        print(str(link + 1) + ". " + links[link])


if __name__ == '__main__':
    main()