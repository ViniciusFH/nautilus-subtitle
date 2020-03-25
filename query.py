import os
import re
from difflib import SequenceMatcher
from helpers import success, error, hashFile, guessMovieName
from crawler import getMovieID, getSubtitlesIDs, getSubAndVideosNames


def queryByHashAndSize(filePath, languageID, server, loginToken):

	print('Creating video hash...')

	tryVideoHash = hashFile(filePath)

	if not tryVideoHash['success']:

		print('Could not generate hash.')

		return error(tryVideoHash['errorMessage'])

	videoHash = tryVideoHash['hash']	
	videoSize = str(os.path.getsize(filePath))

	print('Sucess - Hash:', videoHash, '- Size:', videoSize)

	query = [{ 'sublanguageid': languageID, 'moviehash': videoHash, 'moviebytesize': videoSize }]

	print('Performing query...')

	subtitles = server.SearchSubtitles(loginToken, query)

	if 'data' in subtitles and subtitles['data']:

		print('A subtitle was found!')

		print('Choosing the one with the language id selected...')

		correctLanguageSubs = [sub for sub in subtitles['data'] if sub['SubLanguageID'] == languageID]

		if not correctLanguageSubs:

			print('A subtitle for the language ID selected was not found!')
			return error('A subtitle for the language ID selected was not found!')

		print('A subtitle for the language ID selected was found!')

		print('Selecting the first one...')

		firstSub = correctLanguageSubs[0]

		print('The first one:', firstSub)

		subDownloadLink = firstSub['SubDownloadLink']

		print('Its download link:', subDownloadLink)

		return success('downloadLink', subDownloadLink)


	else:

		print('Nothing was found :(')

		return error('No subtitle was found.')




def queryByMovieName(fileName, languageID, server, loginToken):

	tryGuessName = guessMovieName(fileName)

	if not tryGuessName['success']:
		return error(tryGuessName['errorMessage'])

	probableMovieName = tryGuessName['name']

	print('Probable movie name:', probableMovieName)

	print('Searching...')

	tryGetMovieID = getMovieID(probableMovieName)

	if not tryGetMovieID['success']:
		return error(tryGetMovieID['errorMessage'])

	movieID = tryGetMovieID['ID']

	print('Movie ID:', movieID)

	tryGetSubtitlesIDs = getSubtitlesIDs(movieID, languageID)

	if not tryGetSubtitlesIDs['success']:
		return error(tryGetSubtitlesIDs['errorMessage'])

	subtitlesIDs = tryGetSubtitlesIDs['IDs']

	highestSimilarity = 0
	highestSimID = ''
	chosenSubtitleID = ''

	for subtitleID in subtitlesIDs:

		tryGetSubAndMoviesNames = getSubAndVideosNames(subtitleID)

		if 'success' not in tryGetSubAndMoviesNames:
			continue

		subtitleName = tryGetSubAndMoviesNames['names']['subtitle']

		subtitleSimilarity = SequenceMatcher(None, subtitleName, fileName).ratio()

		print('Subtitle similarity:', subtitleSimilarity)

		if subtitleSimilarity >= 0.9:

			print('Ok, that\'s the one!')
			
			chosenSubtitleID = subtitleID
			break

		if subtitleSimilarity > highestSimilarity:

			highestSimilarity = subtitleSimilarity
			highestSimID = subtitleID

		else:
			print('Checking videos names...')

		videosNames = tryGetSubAndMoviesNames['names']['videos']

		if not videosNames:
			continue

		for videoName in videosNames:

			print('Calculating similarity for video name:', videoName)

			videoSimilarity = SequenceMatcher(None, videoName, fileName).ratio()

			print('Similarity:', videoSimilarity)

			if videoSimilarity >= 0.9:

				chosenSubtitleID = subtitleID

				break

			if videoSimilarity > highestSimilarity:

				highestSimilarity = videoSimilarity
				highestSimID = subtitleID

		if chosenSubtitleID:
			break


	if not chosenSubtitleID:
		print('Could not find a perfect match. Using match of similarity', highestSimilarity)
		chosenSubtitleID = highestSimID


	query = [{ 'idsubtitle': chosenSubtitleID }]

	print('Performing query with ID', chosenSubtitleID)

	chosenSubtitle = server.SearchSubtitles(loginToken, query)

	if 'data' in chosenSubtitle and chosenSubtitle['data']:

		print('The subtitle was found!')

		theSubtitle = chosenSubtitle['data'][0]

		print('The subtitle:', theSubtitle)

		subDownloadLink = theSubtitle['SubDownloadLink']

		print('The download link:', subDownloadLink)

		return success('downloadLink', subDownloadLink)


	else:

		print('Nothing was found :(')

		return error('No subtitle was found.')