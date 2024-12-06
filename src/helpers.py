import re
import requests
import os
import struct
from difflib import SequenceMatcher


def getVideoInfo() -> dict:
    videoPath = os.environ["NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"].splitlines()[
        0]
    folders = videoPath.split("/")
    videoName = folders[len(folders)-1]
    folderPath = videoPath[0:videoPath.index(videoName)-1]

    return {
        "videoPath": videoPath,
        "videoName": videoName,
        "folderPath": folderPath
    }


def hashVideo(path: str) -> str:
    """Produce a hash for a video file: size + 64bit chksum of the first and
    last 64k (even if they overlap because the file is smaller than 128k)"""
    try:
        longlongformat = "Q"  # unsigned long long little endian
        bytesize = struct.calcsize(longlongformat)
        fmt = "<%d%s" % (65536 // bytesize, longlongformat)

        f = open(path, "rb")

        filesize = os.fstat(f.fileno()).st_size
        filehash = filesize

        if filesize < 65536 * 2:
            raise Exception("File too small.")

        buf = f.read(65536)
        longlongs = struct.unpack(fmt, buf)
        filehash += sum(longlongs)

        f.seek(-65536, os.SEEK_END)  # size is always > 131072
        buf = f.read(65536)
        longlongs = struct.unpack(fmt, buf)
        filehash += sum(longlongs)
        filehash &= 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash = "%016x" % filehash
        return returnedhash

    except Exception as err:
        print(err)


def sortBySimilarity(subtitles: list[dict], videoName: str) -> list[dict]:
    subsWithSim = parseSimilarity(subtitles, videoName)
    sortedSubs = sorted(
        subsWithSim, key=lambda s: s["similarity"], reverse=True)

    return sortedSubs


def parseSimilarity(subtitles: list[dict], videoName: str) -> list[dict]:
    subFiles = map(lambda s: s["attributes"]["files"][0], subtitles)
    filesWithSim = map(lambda s: compareNames(videoName, s), list(subFiles))
    return list(filesWithSim)


def compareNames(videoName: str, sub: dict) -> float:
    similarity = SequenceMatcher(None, videoName, sub["file_name"]).ratio()
    return sub | {"similarity": similarity}


def downloadAndSaveFile(link: str, folderPath: str, videoName: str) -> None:

    subName = getSubName(videoName)
    subPath = f"{folderPath}/{subName}"

    fileResponse = requests.get(link, timeout=1)

    open(subPath, "wb").write(fileResponse.content)

    return


def getSubName(videoName: str) -> str:

    subName = re.sub(r'\.[\w]+$', '.srt', videoName)

    return subName


def getSearchParams(guessedInfo: dict, opts: dict) -> dict:
    params = {
        "query": guessedInfo["title"],
        "type": guessedInfo["type"],
    }

    if (guessedInfo["type"] == "episode"):
        params["episode_number"] = guessedInfo["episode"]
        params["season_number"] = guessedInfo["season"]

    else:
        params["year"] = guessedInfo["year"]

    params = params | opts

    return params

def parseSubNames(subtitles: list[dict]) -> list[str]:
    namesMap = map(lambda s: s["file_name"], subtitles)
    return list(namesMap)

def findDictByValue(lst, key, value):
    for dct in lst:
        if key in dct and dct[key] == value:
            return dct
    return None

