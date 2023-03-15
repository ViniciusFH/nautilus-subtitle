import requests
import re
from helpers import success, error


def getSubAndVideosNames(subtitleLink):

	print('Checking subtitle in', subtitleLink)

	rSubtitle = requests.get(subtitleLink)

	subtitlesHTML = rSubtitle.text

	print('Checking subtitle name first...')

	videosNames = re.findall(r'title=\"Subtitle filename\" \/>(.+)[\n\s\(]+', subtitlesHTML)

	videosNames = videosNames + re.findall('title=\"Download - (.+)\" href', subtitlesHTML)

	if not videosNames:
		print('Videos names were not found!')
		return error('Not found!')

	return success('names', videosNames)