import struct, os, re

def error(message):

	return { 'success': False, 'errorMessage': message }


def success(key, data):

	return { 'success': True, key: data }


def hashFile(path):
	"""Produce a hash for a video file: size + 64bit chksum of the first and
	last 64k (even if they overlap because the file is smaller than 128k)"""
	try:
		longlongformat = 'Q' # unsigned long long little endian
		bytesize = struct.calcsize(longlongformat)
		fmt = "<%d%s" % (65536//bytesize, longlongformat)

		f = open(path, "rb")

		filesize = os.fstat(f.fileno()).st_size
		filehash = filesize

		if filesize < 65536 * 2:
		    return error("SizeError")

		buf = f.read(65536)
		longlongs = struct.unpack(fmt, buf)
		filehash += sum(longlongs)

		f.seek(-65536, os.SEEK_END) # size is always > 131072
		buf = f.read(65536)
		longlongs = struct.unpack(fmt, buf)
		filehash += sum(longlongs)
		filehash &= 0xFFFFFFFFFFFFFFFF

		f.close()
		returnedhash = "%016x" % filehash
		return success('hash', returnedhash)

	except Exception as err:

		print(err)

		return error("IOError")

def guessMovieName(fileName):

	fileNamePieces = re.split('[\,\.\(\)\'\-\[\] ]', fileName)

	probableMovieName = ''

	for i in fileNamePieces:

		if re.match('^[a-zA-Z]+$', i):

			probableMovieName += i

		elif probableMovieName != '':

			break

		probableMovieName += ' '


	if not probableMovieName:
		return False

	return probableMovieName
	

def guessMovieYear(fileName):

	tryToGuess = re.findall(r'((?:19|2[012])\d{2})', fileName)

	if len(tryToGuess):
		return tryToGuess[0]

	return 