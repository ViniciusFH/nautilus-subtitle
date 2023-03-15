import os
import re
import requests
from difflib import SequenceMatcher
from helpers import success, error, hashFile, guessMovieName, guessMovieYear
from crawler import getSubAndVideosNames


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
	



def queryByFileName(fileName, languageID, server, loginToken):

	print('First looking for movie suggestions with guessed movie name and year.')

	query = [{ 'sublanguageid': languageID, 'query': fileName }]

	guessQuery = ''

	guessedName = guessMovieName(fileName)

	if guessedName:

		print('Guessed movie name:', guessedName)

		guessQuery = guessedName

		guessedYear = guessMovieYear(fileName)

		if guessedYear:

			print('Guessed movie year:', guessedYear)

			guessQuery += ' ' + guessedYear

	movieID = ''

	if guessQuery:

		print('Requesting suggestions...')
		
		suggestionsBaseURL = 'https://www.opensubtitles.org/libs/suggest.php?format=json3&MovieName='
		suggestionsURL = suggestionsBaseURL + guessQuery.replace(' ', '%20')

		rSuggestions = requests.get(suggestionsURL)

		moviesList = rSuggestions.json()

		if len(moviesList) == 1:

			print('Found only one movie. Using its ID.')

			movieID = moviesList[0]['id']

	if movieID:

		query = [{ 'sublanguageid': languageID, 'idmovie': movieID }]

	print('Performing subtitles query...')

	queryResponse = server.SearchSubtitles(loginToken, query)

	# Try again with guessed movie name and year.
	if not 'data' in queryResponse or not queryResponse['data']:

		print('No subtitle was found.')

		if not guessQuery:
			return error('Query with file name returned empty, and function could not guess movie name.')

		print('Trying with guessed movie name and year.')

		query = [{ 'sublanguageid': languageID, 'query': guessQuery }]

		queryResponse = server.SearchSubtitles(loginToken, query)

		if not 'data' in queryResponse or not queryResponse['data']:
			return error('Both queries returned empty.')	

	print('Success!')	

	subtitles = queryResponse['data']

	similarities = []
	chosenSubtitles = []

	for sub in subtitles:

		tryGetSubAndMoviesNames = getSubAndVideosNames(sub['SubtitlesLink'])

		if 'success' not in tryGetSubAndMoviesNames or not tryGetSubAndMoviesNames['success']:
			continue

		videosNames = tryGetSubAndMoviesNames['names']

		thisHighestSimilarity = 0

		for videoName in videosNames:

			print('Calculating similarity for video name:', videoName)

			videoSimilarity = SequenceMatcher(None, videoName, fileName).ratio()

			print('Similarity:', videoSimilarity)

			if videoSimilarity >= 0.9:

				chosenSubtitles.append(sub)

				break

			if videoSimilarity > thisHighestSimilarity:
				thisHighestSimilarity = videoSimilarity


		if chosenSubtitles:
			break

		similarities.append(thisHighestSimilarity)


	if not chosenSubtitles:
		print('Could not find a perfect match.')
		print('Adding the three best matches in the line...')

		fixedSimilarities = similarities[:]
		similarities.sort(reverse = True)

		i = 0

		while i < len(similarities) and i < 3:

			subIndex = fixedSimilarities.index(similarities[i])

			print('Adding subtitle of similarity', similarities[i])

			chosenSubtitles.append(subtitles[subIndex])

			print('The subtitle link is', subtitles[subIndex]['SubtitlesLink'])

			i += 1

	if not chosenSubtitles:
		print('No video name was found, so similarity failed. Using the three best of the query.')

		i = 0

		while i < len(subtitles) and i < 3:

			chosenSubtitles.append(subtitles[i])

			i += 1

	downloadLinks = []

	for sub in chosenSubtitles:
		downloadLinks.append(sub['SubDownloadLink'])

	return success('links', downloadLinks)
