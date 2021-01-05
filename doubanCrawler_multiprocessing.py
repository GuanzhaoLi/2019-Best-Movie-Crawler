#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 21:59:02 2021

@author: guanzhaoli
"""

import basicSpider
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool,Manager, cpu_count

crawl_queue = []
crawled = []

# get html information of one page
def get_html(url):
    headers = [("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")]
    html = basicSpider.downloadHtml(url, headers = headers)
    return html


# get all movie info in the current page
def get_movie_all(html):
    soup = BeautifulSoup(html, "lxml")
    movie_list = soup.find_all('div', class_ = 'doulist-item')
    
    return movie_list


# get detailed info of one movie
# return: a whole line of one movie containing detailed info
def get_movie_one(movie):
    result = ""
    
    soup = BeautifulSoup(str(movie), "lxml")
    title = soup.find_all('div', class_ = "title")
    
    soup_title = BeautifulSoup(str(title[0]), "html.parser")
    
    for line in soup_title.stripped_strings:
        result += line
    
    try:
        score = soup.find_all('span', class_ = "rating_nums")
        score_ = BeautifulSoup(str(score[0]), "lxml")
        for line in score_.stripped_strings:
            result += "|| score: "
            result += line
        
    except:
        result += "|| score : 5.0"
    
    try:
        abstract = soup.find_all('div', class_ = 'abstract')
        abstract_info = BeautifulSoup(str(abstract[0]), "lxml")

        for line in abstract_info.stripped_strings:
            result += "|| "
            result += line
    except:
        result += "|| no comment"
    
    try:
        comment = soup.find_all('div', class_ = 'comment-item content')
        comment_ = BeautifulSoup(str(comment[0]), "lxml")

        for line in comment_.stripped_strings:
            result += "|| "
            result += line
    except:
        result += "|| no comment"

    result += "\n"
    return result
        


def save_file(movieInfo, lock):
    with open("doubanMovie.txt", "a") as f:
        lock.acquire()
        f.write(movieInfo)
        lock.release()
        
        
        
# get one page and save to a txt file
def main(url, q, lock):
    global pattern
    
    html = get_html(url)
    movie_list = get_movie_all(html)
    
    for movie in movie_list:
        save_file(get_movie_one(movie), lock)
    
    q.put(url) # completed url


if __name__ == "__main__":
    
    pool = Pool(cpu_count()) # use all cpu cores
    lock = Manager().Lock() 
    q = Manager().Queue()
    
    for i in range(26):
        url =  "https://www.douban.com/doulist/114465/?start=" + str(25*i) + "&amp;sort=seq&amp;playable=0&amp;sub_type="
        crawl_queue.append(url)

    while crawl_queue:
        url = crawl_queue.pop(0)
        pool.apply_async(func= main, args=(url, q, lock))
        url_completed = q.get()
        crawled.append(url_completed)
        
    pool.close()
    pool.join()

         
     
     