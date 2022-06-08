
import subprocess
import threading
import time
import os

class DownloadManager:

    def __init__(self, localUrl):
        self.running = False
        self.localUrl = localUrl
        self.queue = []
        self.lock = threading.Lock()
        self.result = Result()
        self.history = []

    def start(self, url, parts, output):
        with self.lock:
            self.queue.append((url, parts, output))
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=DownloadManager.loop, args=(self,))
            self.thread.start()

    def updateState(self, state):
        self.result.update(state)

    def getState(self):
        return self.result.to_json()

    def getHistory(self):
        return self.history

    def getQueue(self):
        return [{"url": t[0], "parts": t[1], "out": t[2]} for t in self.queue]
    
    def clearHistory(self):
        self.history = []

    @staticmethod
    def loop(self):
        workingDir = os.path.abspath(os.path.dirname(__file__))
        while True:
            with self.lock:
                if len(self.queue) == 0:
                    self.running = False
                    break
                (url, parts, output) = self.queue.pop(0)
            self.result = Result()
            p = subprocess.Popen(
                [f"python {os.path.join(workingDir, 'ulozto-downloader.py')} --auto-captcha --parts {parts} --output '{output}' --notify-url '{self.localUrl}' '{url}'"],
                shell=True, close_fds=True)
            while p.poll() is None:
                time.sleep(5)
            r = self.result.to_json()
            self.history.append(r)
            self.result = Result()
            

class Result:

    def __init__(self):
        self.updaters = {
            "init": self._udate_init,
            "log": self._update_log,
            "err": self._update_error,
            "done": self._update_done,
            "info": self._update_info,
            "part": self._update_part,
            "captchaState": self._update_captcha_state,
            "torState": self._update_tor_state,
            "savedState": self._update_saved_state,
        }
        self.state = {
            "url": "",
            "out": "",
            "file": "",
            "type": "",
            "size": "",
            "captchaState": "",
            "torState": "",
            "savedState": "",
            "logs": [],
            "parts": [],
            "error": "",
            "done": 0
        }

    def _udate_init(self, state):
        self.state["url"] = state["url"]
        self.state["out"] = state["out"]
        self.state["parts"] = ["" for x in range(state["parts"])]

    def _update_log(self, state):
        self.state["logs"].append(state)

    def _update_error(self, state):
        self.state["error"] = state
        self.state["done"] = 1

    def _update_done(self, state):
        self.state["done"] = 1

    def _update_info(self, state):
        self.state["file"] = state["file"]
        self.state["type"] = state["type"]
        self.state["size"] = state["size"]
    
    def _update_part(self, state):
        id = state["id"]
        self.state["parts"][id] = state["text"]

    def _update_captcha_state(self, state):
        self.state["captchaState"] = state

    def _update_tor_state(self, state):
        self.state["torState"] = state

    def _update_saved_state(self, state):
        self.state["savedState"] = state

    def update(self, state):
        type = state.get("type")
        data = state.get("data")
        if not type in self.updaters:
            return
        updater = self.updaters.get(type)
        updater(data)

    def to_json(self):
        return self.state