#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys

from xmlrpc.client import ServerProxy

from query import queryByHashAndSize, queryByMovieName
from download import downloadAndSaveFile


languageID = 'eng'

filePath = os.environ['NAUTILUS_SCRIPT_SELECTED_FILE_PATHS'].splitlines()[0]
print('File path:', filePath)
folders = filePath.split('/')
fileName = folders[len(folders)-1]
print('File name:', fileName)
folderPath = filePath[0:filePath.index(fileName)]
print('Folder path:', folderPath)

print('Searching the best subtitle for file', fileName, '...')

print('Retrieving loginToken...')

server = ServerProxy('https://api.opensubtitles.org/xml-rpc')

session = server.LogIn('', '', languageID, 'opensubtitles-download 4.1')

if session['status'] != '200 OK':
	print('Login failed. Exiting...')
	sys.exit()

loginToken = session['token']

print('Success:', loginToken)

print('First trying to query using file hash and size...')

tryHashAndSize = queryByHashAndSize(filePath, languageID, server, loginToken)

if tryHashAndSize['success']:

	downloadAndSaveFile(tryHashAndSize['downloadLink'], folderPath, fileName)

	sys.exit()

else:

	print('Query by hash and size failed.')

	tryByFileName = queryByMovieName(fileName, languageID, server, loginToken)

	if tryByFileName['success']:
		
		downloadAndSaveFile(tryByFileName['downloadLink'], folderPath, fileName)

		sys.exit()

	else:

		print('Query by movie name also failed :/')

sys.exit()