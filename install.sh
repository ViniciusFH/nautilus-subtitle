#!/usr/bin/env bash
if [ ! -d "~/.local/share/nautilus/scripts/Find Subtitles" ]
then
	mkdir ~/.local/share/nautilus/scripts/Find\ Subtitles
fi

if [ ! -d "~/.nautilus-subtitle" ]
then
	mkdir ~/.nautilus-subtitle
fi 

cp ./source/languages/* ~/.local/share/nautilus/scripts/Find\ Subtitles
cp ./source/tools/* ~/.nautilus-subtitle