import re, requests, sys

def guessMovieName(fileName):

	fileNamePieces = re.split('[\,\.\(\)\'\-\[\] ]', fileName)

	probableMovieName = ''

	for i in fileNamePieces:

		if re.match('^[a-zA-Z]+$', i):

			probableMovieName += i

		else:

			break

		probableMovieName += ' '

	probableMovieName = probableMovieName.strip()

	return probableMovieName

files = [
	"L ufficiale e la spia-J'accuse (2019) ITA-FRE Ac3 5.1 BDRip 1080p H264 [ArMor].mkv",
	'Inside.Llewyn.Davis.2013.1080p.BluRay.x264.[ExYu - SRB].mp4',
	'Society.1989.1080p.BluRay.x264-[YTS.AM]',
	'Rashomon.1950.1080p.BluRay.x264-[YTS.AM].srt',
	'Gaslight.1944.(Crime.Drama.Film-Noir).1080p.x264-Classics.mkv',
	'Shallow.Grave.1994.1080p.BluRay.x264-[YTS.AG].mp4',
	'Riding.in.Cars.with.Boys.2001.720p.WEBRip.x264.AAC-ETRG.mp4',
	'Kuroneko.1968.1080p.Criterion.BluRay.x264.anoXmous.mp4',
	'Jeanne.Dielman.23.Quai.du.Commerce.1080.Bruxelles.1975.1080p.Criterion.BluRay.x265.HEVC.AAC-SARTRE.mkv',
	'Blood.Feast.1963.1080p.BluRay.x264.YIFY.mp4   WWW.YTS.RE.jpg',
	'Big.Daddy.1999.1080p.BluRay.H264.AAC-RARBG.mp4',
	'Barton.Fink.1991.1080p.BluRay.x264-[YTS.AM].srt'
]

# for i in files:

name = guessMovieName(files[2])
year = re.findall(r'((?:19|2[012])\d{2})[^p]', files[2])[0]

print(name, year)

suggestionsBaseURL = 'https://www.opensubtitles.org/libs/suggest.php?format=json3&MovieName='
suggestionsURL = suggestionsBaseURL + name.replace(' ', '%20') + '%20' + year

rSuggestions = requests.get(suggestionsBaseURL)

moviesList = rSuggestions.json()
print(moviesList)