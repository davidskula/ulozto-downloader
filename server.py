#!/usr/bin/env python3
"""Uloz.to quick multiple sessions downloader."""
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse   
import uvicorn
import argparse
from downloadManager import DownloadManager
import uuid

parser = argparse.ArgumentParser(
    description='Web server for ulozto downloader',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument('--port', metavar='PORT', type=int, default=8000,
                    help="Web server port")
args = parser.parse_args()

notifyId = uuid.uuid4().hex
manager = DownloadManager(f"http://localhost:{args.port}/udws/{notifyId}")

app = FastAPI(openapi_url=None)
app.mount("/site", StaticFiles(directory="site", html = True), name="site")

@app.get("/")
async def read_index():
    return RedirectResponse(url="/site/index.html")

@app.get("/queue")
def getQueue():
    return manager.getQueue()

@app.post("/queue")
async def startTask(request: Request):
    d = await request.json()
    if not "url" in d:
        raise HTTPException(status_code=404, detail="Not found")
    url = d.get("url")
    parts = d.get("parts", 10)
    out = d.get("out", "")
    manager.start(url, parts, out)
    return Response(status_code=200)

@app.get("/history")
def getHistory():
    return manager.getHistory()

@app.delete("/history")
def clearHistory():
    return manager.clearHistory()

@app.get("/actDownloading")
def getState():
    return manager.getState()

@app.post("/udws/{id}")
async def setDownloadState(id, request: Request):
    if id != notifyId:
        raise HTTPException(status_code=404, detail="Not found")
    d = await request.json()
    manager.updateState(d)

if __name__ == "__main__":
    uvicorn.run("server:app", reload=True, port=args.port, host="0.0.0.0")
