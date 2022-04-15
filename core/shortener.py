import hashlib
import re
'''
Functionality for the shortener service. 
'''

class Shortener:
    URL_LEN = 5
    shortenedUrl = ""
    base_url = 'https://www.tiny/'
    
    def __init__(self, url):
        self.__shortenUrl(url)
    
    def __shortenUrl(self, url):
        hashedUrl = hashlib.sha256(url.encode())
        hexifiedUrl = hashedUrl.hexdigest()
        self.shortenedUrl = self.base_url + hexifiedUrl[:self.URL_LEN]

    def _print(self):
            print(self.shortenedUrl)

def is_url(url):
    '''Code from: https://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python'''
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)