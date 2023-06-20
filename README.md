# random-youtube
Tool for downloading a random youtube video/audio

# Instructions
Install python
`https://www.python.org/downloads/`

Install requirements
`pip install -r requirements.txt`

Usage
`python .\main.py [option] ... [-v "{Youtube Link}" | -cs "{0}" | -cl "{60}" ] [-a -c -cr]...`

Example
`python .\main.py -v "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a -c -cr`

Options 
```
-v "{Youtube Link}"     : Link for youtube video
-pl "{Youtube Playlist}"     : Link for youtube playlist. This option will get a random video on the playlist
-a                      : Download audio only
-c                      : Crop the video/audio
-cr                     : Crop a random portion of the video/audio
-cs                     : Set a starting point for the cropping
-cl                     : Cropped length
```
