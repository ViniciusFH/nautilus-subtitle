import os
from xmlrpc.client import ServerProxy
from helpers import hashFile, guessMovieName
from difflib import SequenceMatcher


languageID = 'eng'

filePath = '/home/lodono/Downloads/Inside.Llewyn.Davis.2013.1080p.BluRay.x264.[ExYu - SRB].mp4'
fileName = "Jeanne.Dielman.23.Quai.du.Commerce.1080.Bruxelles.1975.1080p.Criterion.BluRay.x265.HEVC.AAC-SARTRE.mkv"

server = ServerProxy('https://api.opensubtitles.org/xml-rpc')

session = server.LogIn('', '', languageID, 'opensubtitles-download 4.1')
loginToken = session['token']

if session['status'] != '200 OK':
	print('Login failed. Exiting...')
	sys.exit()

# videoHash = hashFile(filePath)['hash']
# videoSize = str(os.path.getsize(filePath))

query = [{ 'sublanguageid': languageID, 'idmovie': '25196' }]
# query = [{ 'sublanguageid': languageID, 'query': 'Society.1989.1080p.BluRay.x264-[YTS.AM]' }]

subtitles = server.SearchSubtitles(loginToken, query)

print(subtitles)


# for i in data:

# 	release = i['MovieReleaseName']

# 	videoSimilarity = SequenceMatcher(None, release, fileName).ratio()

# 	print(videoSimilarity)

