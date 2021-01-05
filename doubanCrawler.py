#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 21:59:02 2021

@author: guanzhaoli
"""

import basicSpider
from bs4 import BeautifulSoup
import re


pattern = re.compile('(https://www.douban.com/doulist/114465/\?start=.*)"')
crawl_queue = []
crawled = []


# get html information of one page
def get_html(url):
    headers = [("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")]
    html = basicSpider.downloadHtml(url, headers = headers)
    return html


# get all movie info in the current page
def get_movie_all(html):
    soup = BeautifulSoup(html, "html.parser")
    movie_list = soup.find_all('div', class_ = 'bd doulist-subject')
    #print(movie_list)
    return movie_list


# get detailed info of one movie
# return: a whole line of one movie containing detailed info
def get_movie_one(movie):
    
    result = ""
    
    soup = BeautifulSoup(str(movie), "html.parser")
    title = soup.find_all('div', class_ = "title")
    
    soup_title = BeautifulSoup(str(title[0]), "html.parser")
    
    for line in soup_title.stripped_strings:
        result += line
    
    try:
        score = soup.find_all('span', class_ = "rating_nums")
        score_ = BeautifulSoup(str(score[0]), "html.parser")
        for line in score_.stripped_strings:
            result += "|| score: "
            result += line
        
    except:
        result += "|| score : 5.0"
        
    abstract = soup.find_all('div', class_ = 'abstract')
    abstract_info = BeautifulSoup(str(abstract[0]), "html.parser")
    
    for line in abstract_info.stripped_strings:
        result += "|| "
        result += line
    
    result += "\n"
    return result
        


def save_file(movieInfo):
    with open("doubanMovie.txt", "a") as f:
        f.write(movieInfo)
        
        
        
# get one page and save to a txt file
def main(url):   
    global crawl_queue
    global crawled
    global pattern
    
    html = get_html(url)
    movie_list = get_movie_all(html)
    item_urls = re.findall(pattern, html)
    
    for item in item_urls:
        if item not in crawled:
            crawl_queue.append(item)
    crawl_queue = list(set(crawl_queue))
    
    for movie in movie_list:
        save_file(get_movie_one(movie))

        

if __name__ == "__main__":

    
    url = "https://www.douban.com/doulist/114465/?start=0&amp;sort=seq&amp;playable=0&amp;sub_type=" 
    main(url)
    crawled.append(url)
     
    html = get_html(url)

    item_urls = re.findall(pattern, html)   
     
    for item in item_urls:
        if item not in crawled:
            crawl_queue.append(item)
    
    crawl_queue = list(set(crawl_queue))

    while crawl_queue:
        url = crawl_queue.pop(0)
        main(url)
        crawled.append(url)

         
     
     