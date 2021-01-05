
import sys
import logging
import urllib
import random
import time

logger = logging.getLogger("basicSpider")

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

file_handler = logging.FileHandler('basicSpider.log')
file_handler.setFormatter(formatter)

consle_handler = logging.StreamHandler(sys.stdout)
consle_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(consle_handler)

PROXY_RANGE_MIN = 1
PROXY_RANGE_MAX = 10
PROXY_RANGE = 2
NUM = 10

def downloadHtml(url, headers=[],
                 proxy={}, num_retries=NUM,
                 timeout=NUM, decodeInfo="utf-8"):
    html = None
    
    if num_retries <= 0:
        return html
        
    if random.randint(PROXY_RANGE_MIN,PROXY_RANGE_MAX) > PROXY_RANGE: 
        logger.info("No Proxy")
        proxy = None 
    
    proxy_handler = urllib.request.ProxyHandler(proxy)

    opener = urllib.request.build_opener(proxy_handler)
    opener.addheaders = headers
    urllib.request.install_opener(opener)
    
    try:
        response = urllib.request.urlopen(url)
        html = response.read().decode(decodeInfo)
        logger.info(html)
    except UnicodeDecodeError:
        logger.error("UnicodeDecodeError")
    except urllib.error.URLError or \
           urllib.error.HTTPError as e:
               logger.error("urllib error")
               if hasattr(e,'code') and 400 <= e.code < 500:
                   logger.error("Client Error")
               elif hasattr(e,'code') and 500 <= e.code < 600:
                   html = downloadHtml(url,
                                       headers,
                                       proxy,
                                       timeout,
                                       decodeInfo,
                                       num_retries-1)
                   time.sleep(PROXY_RANGE)
    except:
       logger.error("Download error, ")
                   
    return html
    

logger.removeHandler(file_handler)
logger.removeHandler(consle_handler) 