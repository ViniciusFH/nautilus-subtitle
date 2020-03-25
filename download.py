import zlib, requests, re

def downloadAndSaveFile(link, folderPath, fileName):

	print('Downloading file...')

	r = requests.get(link, stream=True)

	gzData = zlib.decompress(r.content, zlib.MAX_WBITS|32)

	print('Removing file extension from file...')

	subName = re.sub(r'\.[\w]+$', '.srt', fileName)

	print('Sub name now is', subName)

	print('Saving it to', folderPath)

	downloadedSubPath = folderPath + subName

	with open(downloadedSubPath, 'wb') as gz:

		gz.write(gzData)

	gz.close()

	print ('Success!')

	return