import hashlib
import requests

class Shortener:
    URL_LEN = 5
    shortenedUrl = ""
    base_url = 'https://www.tinyurl/'
    
    def __init__(self, url):
        self.__shortenUrl(url)
    
    def __shortenUrl(self, url):
        hashedUrl = hashlib.sha256(url.encode())
        hexifiedUrl = hashedUrl.hexdigest()
        self.shortenedUrl = self.base_url + hexifiedUrl[0:self.URL_LEN]

    def _print(self):
        print(self.shortenedUrl)

    def is_url(self, url):
        try: 
            requests.get(url)
        except: 
            return False
        return True

if __name__ == "__main__":
    sh = Shortener("https://stackoverflow.com/questions/1641219/does-python-have-private-variables-in-classes").shortenedUrl
    # sh._print()
    print(sh)