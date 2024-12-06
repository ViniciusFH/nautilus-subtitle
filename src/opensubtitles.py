import requests
import helpers as H


class OpenSubtitles():
    def __init__(self) -> None:

        self.language = ""
        self.videoName = ""
        self.videoPath = ""
        self.folderPath = ""
        self.videoHash = ""
        self.baseURL = "https://api.opensubtitles.com/api/v1"
        self.apiKey = "JrIVczpYieqqQqjKYpjLK3RuStUu6DpK"
        self.userName = "lodono"
        self.password = "bocegajen"
        self.I = {}
        self.basicHeaders = {
            "Api-Key": self.apiKey,
            "User-Agent": "nautilus-sub v0.1",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Connection": "keep-alive"
        }
        self.timeout = 1
        self.userPayload = {
            "username": self.userName,
            "password": self.password
        }
        self.session = requests.Session()
        self.session.headers = self.basicHeaders

    def login(self) -> dict:
        url = self.baseURL + "/login"

        response = self.session.post(
            url,
            json=self.userPayload,
            timeout=self.timeout
        )

        json = response.json()
        token = json["token"]

        self.session.headers["Authorization"] = f"Bearer {token}"

        return token

    def search(self, queryParams: dict) -> list[dict]:

        url = self.baseURL + "/subtitles"

        response = self.session.get(
            url,
            params=queryParams,
            timeout=self.timeout,
        )

        json = response.json()

        return json["data"]

    def guessit(self, videoname: str) -> dict:

        url = self.baseURL + "/utilities/guessit"

        queryParams = {"filename": videoname}

        response = self.session.get(
            url,
            params=queryParams,
            timeout=self.timeout
        )

        return response.json()

    def getDownloadLink(self, fileId):

        self.login()

        url = self.baseURL + "/download"

        payload = {"file_id": str(fileId)}

        response = self.session.post(
            url,
            json=payload
        )

        return response.json()["link"]

    def setVideoInfo(self, videoInfo: dict) -> None:
        self.videoName = videoInfo["videoName"]
        self.videoPath = videoInfo["videoPath"]
        self.folderPath = videoInfo["folderPath"]

    def setLanguage(self, language: str) -> None:
        self.language = language

    def hashVideo(self) -> None:
        videoHash = H.hashVideo(self.videoPath)
        self.videoHash = videoHash

    def queryByHash(self) -> list[dict]:
        params = {
            "languages": self.language,
            "moviehash": self.videoHash
        }

        data = self.search(params)

        return data

    def queryByInfo(self) -> list[dict]:
        guessedInfo = self.guessit(self.videoName)

        params = H.getSearchParams(guessedInfo, {"languages": self.language})

        data = self.search(params)

        return data
    
    def query(self) -> list[dict]:
        subtitles = self.queryByHash()

        if len(subtitles) == 0:
            subtitles = self.queryByInfo()

        subtitles = H.sortBySimilarity(subtitles, self.videoName)

        return subtitles

    def downloadSelectedSub(self, subtitle: list[dict]):
        downloadLink = self.getDownloadLink(subtitle["file_id"])
        self.I.infoMessage("Fazendo download...")
        H.downloadAndSaveFile(downloadLink, self.folderPath, self.videoName)

    def setInterface(self, interface) -> None:
        self.I = interface