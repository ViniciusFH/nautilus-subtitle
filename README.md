# nautilus-subtitle
A Nautilus script written in Python to automatically find the best subtitle for a movie. It uses [OpenSubtitles API](https://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC), and a little bit of crawling.


## Prerequisites
* Python 3

## Installing
On terminal, clone the repository:
```
git clone https://github.com/ViniciusFH/nautilus-subtitle.git
```
Cd to it:
```
cd nautilus-subtitle
```
Make install.sh executable:
```
chmod +x install.sh
```
And run it:
```
./install.sh
```

## Usage
Now that it is installed, usage is quite simple:
* Open nautilus
* Locate the movie file
* Right-click on it
* Scripts &rarr; Find Subtitles &rarr; English/Portuguese

## Adding languages
If you want to add a new language, just replace in the following commands {{language name}} with the name you would like to see in Find Subtitles option, and {{language ID}} with the three letter [ISO-639](http://www.opensubtitles.org/addons/export_languages.php) of your language:
```
cp ~/.local/share/nautilus/scripts/Find\ Subtitles/English.py ~/.local/share/nautilus/scripts/Find\ Subtitles/{{language name}}.py
```
```
sed -i 's/eng/{{language ID}}/g' ~/.local/share/nautilus/scripts/Find\ Subtitles/{{language name}}.py
```

## How it works
The script basically attempts to find subtitles with two different methods. The first and preferred one is a query to the OpenSubtitles API using the movie file hash, as recommended and exemplified by the admin. The subtitle found is downloaded. But, if this query returns nothing, the script tries to machine replicate my human method of searching subtitles. First, it tries to guess the movie name and year, and get the movie ID in open subtitles. If it works, the script iterates through all subtitles for that movie ID in the specified language, and compare your file name with the ones that each subtitle is supposed to match. The comparison has a score fetched with the SequenceMatcher function from Python's difflib. If one of them has over than 90% match with the file name, the script downloads it. Otherwise, the three best matches are downloaded.
