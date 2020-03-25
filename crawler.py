import requests
import re
from helpers import success, error

def getMovieID(name):

	suggestionsBaseURL = 'https://www.opensubtitles.org/libs/suggest.php?format=json3&MovieName='
	suggestionsURL = suggestionsBaseURL + name.replace(' ', '%20')

	rSuggestions = requests.get(suggestionsURL)

	moviesList = rSuggestions.json()

	if not moviesList:
		return error('Could not find', probableMovieName)

	print('Found th(is|ese) movie(s):', moviesList)

	firstMovie = moviesList[0]

	print('Choosing the first one:', firstMovie)

	movieID = firstMovie['id']

	return success('ID', movieID)


def getSubtitlesIDs(movieID, languageID):

	movieBaseURL = 'https://www.opensubtitles.org/en/search/sublanguageid-'
	movieLanguageURL = movieBaseURL + languageID + '/idmovie-'
	movieURL = movieLanguageURL + str(movieID)

	rMovie = requests.get(movieURL)

	movieHTML = rMovie.text

	subtitlesIDs = re.findall('servOC\(([\d]+)\,\'', movieHTML)

	if not subtitlesIDs:
		return error('No subtitle found.')

	return success('IDs', subtitlesIDs)


def getSubAndVideosNames(subtitleID):

	print('Checking subtitle with ID', subtitleID)

	names = {}

	subtitleBaseURL = 'https://www.opensubtitles.org/en/subtitles/'
	subtitleURL = subtitleBaseURL + str(subtitleID)

	rSubtitle = requests.get(subtitleURL)

	subtitlesHTML = rSubtitle.text

	print('Checking subtitle name first...')

	trySubtitleName = re.findall(r'title=\"Subtitle filename\" \/>(.+)[\n\s\(]+', subtitlesHTML)

	if trySubtitleName:

		subtitleName = trySubtitleName[0]

		print('Subtitle name:', subtitleName)

		names['subtitle'] = subtitleName

	videosNames = re.findall('title=\"Download - (.+)\" href', subtitlesHTML)

	names['videos'] = videosNames

	return success('names', names)