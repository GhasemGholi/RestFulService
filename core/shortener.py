import hashlib

class Shortener:
    __URL_LEN = 5
    __shortenedUrl = ""
    def __init__(self, url):
        self.__shortenUrl(url)
    
    def __shortenUrl(self, url):
        hashedUrl = hashlib.sha512(url.encode())
        hexifiedUrl = hashedUrl.hexdigest()
        self.shortenedUrl = hexifiedUrl[0:self.__URL_LEN]

    def _print(self):
        print(self.__shortenedUrl)

if __name__ == "__main__":
    sh = Shortener("https://stackoverflow.com/questions/1641219/does-python-have-private-variables-in-classes")
    sh._print()