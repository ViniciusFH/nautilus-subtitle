import zlib, requests, re

def downloadAndSaveFile(link, folderPath, subName):

	print('Downloading file...')

	r = requests.get(link, stream=True)

	gzData = zlib.decompress(r.content, zlib.MAX_WBITS|32)

	print('Sub name is', subName)

	print('Saving it to', folderPath)

	downloadedSubPath = folderPath + subName

	with open(downloadedSubPath, 'wb') as gz:

		gz.write(gzData)

	gz.close()

	print ('Success!')

	return