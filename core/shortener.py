import hashlib
import requests

class Shortener:
    URL_LEN = 5
    shortenedUrl = ""
    
    def __init__(self, url):
        self.__shortenUrl(url)
    
    def __shortenUrl(self, url):
        hashedUrl = hashlib.sha256(url.encode())
        hexifiedUrl = hashedUrl.hexdigest()
        self.shortenedUrl = hexifiedUrl[0:self.URL_LEN]

    def _print(self):
        print(self.shortenedUrl)

    def is_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False

if __name__ == "__main__":
    sh = Shortener("https://stackoverflow.com/questions/1641219/does-python-have-private-variables-in-classes").shortenedUrl
    # sh._print()
    print(sh)