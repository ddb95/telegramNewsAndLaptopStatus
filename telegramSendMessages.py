#!/usr/bin/python3.6

import requests
import telegram
from config import telegram_token, newsAPIKey
from newsapi import NewsApiClient
import time

MAX_MESSAGE_LENGTH = 4000

top_articles_business_url = 'https://newsapi.org/v2/top-headlines?country=in&category=business&page=1&page_size=1&apiKey=' + newsAPIKey
top_articles_health_url = 'https://newsapi.org/v2/top-headlines?country=in&category=health&page=2&page_size=15&apiKey=' + newsAPIKey
top_articles_science_url = 'https://newsapi.org/v2/top-headlines?country=in&category=health&page=2&page_size=15&apiKey=' + newsAPIKey
top_articles_sports_url = 'https://newsapi.org/v2/top-headlines?country=in&category=health&page=2&page_size=15&apiKey=' + newsAPIKey
top_articles_technology_url = 'https://newsapi.org/v2/top-headlines?country=in&category=health&page=2&page_size=15&apiKey=' + newsAPIKey

'''
You can search for articles with any combination of the following criteria:

Keyword or phrase. Eg: find all articles containing the word 'Microsoft'.
Date published. Eg: find all articles published yesterday.
Source name. Eg: find all articles by 'TechCrunch'.
Source domain name. Eg: find all articles published on nytimes.com.
Language. Eg: find all articles written in English.

You can sort the results in the following orders:
Date published
Relevancy to search keyword
Popularity of source
'''


# Get Request for Sports, Health, Business, Tech and Science
def getDataGetRequest(url, type):
    response = requests.get(url)
    if response.status_code == 200:
        print(response.status_code)
        format_Business_Health_Science_Sports_Tech_data(response.json()['articles'], type)
        return response.json()['articles']
    else:
        response.status_code


# Format the data for Sports, Health, Business, Tech and Science
def format_Business_Health_Science_Sports_Tech_data(data, type):
    message = '\n\n\n'
    for items in range(len(data)):
        source = data[items]['source']['name']
        title = data[items]['title']
        url = data[items]['url']
        if data[items]['author'] is not None:
            author = data[items]['author']
        else:
            author = 'Correspondent'
        if data[items]['description'] is not None:
            description = data[items]['description']
        else:
            description = 'N/A'
        message += '\n\n'
        message += 'Source: ' + '<u>' + source + '</u>' + '\n'
        message += 'Author: ' '<u>' + author + '</u>' + '\n'
        message += 'Title: ' + title + '\n'
        message += 'Description: ' + description + '\n'
        message += '\n'
        message += '[<a href="' + url + '">Click for more information</a>]'
        message += '\n\n'
    time.sleep(5)
    send_message(message, type)


def send_message(text, types):
    # Send in parts so that there are no Message Length Error

    if len(text) <= MAX_MESSAGE_LENGTH:
        return bot.send_message(chat_id="@djangowithddb", text=text + types, parse_mode=telegram.ParseMode.HTML)
    parts = []
    while len(text) > 0:
        if len(text) > MAX_MESSAGE_LENGTH:
            part = text[:MAX_MESSAGE_LENGTH]
            first_lnbr = part.rfind('\n')
            if first_lnbr != -1:
                parts.append(part[:first_lnbr])
                text = text[(first_lnbr + 1):]
            else:
                parts.append(part)
                text = text[MAX_MESSAGE_LENGTH:]
        else:
            parts.append(text)
            break

    msg = None
    for part in parts:
        msg = bot.send_message(chat_id="@djangowithddb", text=part + types, parse_mode=telegram.ParseMode.HTML)
        time.sleep(1)
    return msg  # return only the last message


if __name__ == '__main__':
    bot = telegram.Bot(token=telegram_token)
    newsapi = NewsApiClient(api_key=newsAPIKey)

    # Top Headlines in India
    top_headLines = newsapi.get_top_headlines(q='india',
                                              sources='bbc-news, al-jazeera-english, axios, google-news-in, fox-news, independent, reuters, rte, the-hindu, the-huffington-post, the-washington-post, the-washington-times, time, vice-news',
                                              language='en')
    # # Format and Send the data
    format_Business_Health_Science_Sports_Tech_data(top_headLines['articles'], 'Top Headlines in India')

    # Top 15 Articles in India
    top_articles = newsapi.get_everything(q='india',
                                          sources='bbc-news, al-jazeera-english, axios, fox-news, independent, reuters, rte, the-hindu, the-huffington-post, the-washington-post, the-washington-times, time, vice-news',
                                          from_param='2020-01-21',
                                          to='2020-01-22',
                                          language='en',
                                          sort_by='popularity',
                                          page=2,
                                          page_size=15)
    # # Format and Send the data
    format_Business_Health_Science_Sports_Tech_data(top_articles['articles'], 'Top Articles in India')

    # Top 15 Articles Health in India
    top_articles_health_data = getDataGetRequest(top_articles_health_url, 'Top Articles in Health')
    # Top 15 Articles Science in India
    top_articles_science_data = getDataGetRequest(top_articles_science_url, 'Top Articles in Science')
    # Top 15 Articles Sports in India
    top_articles_sports_data = getDataGetRequest(top_articles_sports_url, 'Top Articles in Sports')
    # Top 15 Articles Technology in India
    top_articles_technology_data = getDataGetRequest(top_articles_technology_url, 'Top Articles in Tech')
    # Top 15 Articles Business in India
    top_articles_business_data = getDataGetRequest(top_articles_business_url, 'Top Articles in Business')
