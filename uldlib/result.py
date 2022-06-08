import requests

class Result:

    def __init__(self, url):
        self.url = url

    def init(self, url, numOfParts, output):
        self._send("init", { "url": url, "parts": numOfParts, "out": output })

    def log(self, text):
        self._send("log", text)

    def error(self, text):
        self._send("err", text)

    def done(self):
        self._send("done", "")

    def info(self, file, downloadType, size):
        self._send("info", { "file": file, "type": downloadType, "size": size })

    def part_status(self, id, text):
        self._send("part", { "id": id, "text": text })

    def captcha_status(self, text):
        self._send("captchaState", text)

    def tor_status(self, text):
        self._send("torState", text)

    def saved_status(self, text):
        self._send("savedState", text)

    def _send(self, type, data):
        d = { "type": type, "data": data }
        requests.post(self.url, json=d)
