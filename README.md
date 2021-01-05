# 2019-Best-Movie-Crawler
A crawler for 2019 best movies from douban using multiprocessing

Information extraction in this crawler is implemented by Beautiful Soup 4. 


make sure you have python 3 and bs4 in your environment

to run the main program, simply use

***python3 doubanCrawler_multiprocessing.py

You may find it will generate .log file named basicSpider.log, in which debug info can be found.

*** The doubanCrawler.py starts from a starting url and crawl all the pages that is in the navigator in a BFS manner. 
    Not useful in this case but I just put there for future reference.
