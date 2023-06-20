import pytube
import random
import shutil
from moviepy.editor import VideoFileClip, AudioFileClip
import argparse

TIME_LENGTH = 60
VIDEOS_FOLDER='./videos-folder'
AUDIO_FOLDER='./audio-folder'

def crop_video(title, length, crop_length = TIME_LENGTH, crop_start = 0, crop_random = False):
    path = f'{VIDEOS_FOLDER}/{title}.mp4'
    clip = VideoFileClip(path)
    if crop_random:
        print('LENGTH: ', length)
        max_length = length - crop_length
        random_start = random.randint(0,max_length)
        clip = clip.subclip(random_start, random_start + crop_length)
    else:
        clip = clip.subclip(crop_start, crop_length)

    filename = f'{title}.mp4'
    clip.write_videofile(filename,fps=30)
    clip.close()
    shutil.move(filename, f'{VIDEOS_FOLDER}/{filename}')
    print('FILE CREATED AT: ', f'{VIDEOS_FOLDER}/{filename}')

def crop_audio(title, length, crop_start = 0, crop_random = False, crop_length = TIME_LENGTH):
    path = f'{AUDIO_FOLDER}/{title}.mp3'
    clip = AudioFileClip(path)
    if crop_random:
        max_length = length - crop_length
        random_start = random.randint(0,max_length)
        clip = clip.subclip(random_start, random_start + crop_length)
    else:
        clip = clip.subclip(crop_start, crop_length)

    # Save the segment as an MP3 audio file
    filename = f'{title}.mp3'
    clip.write_audiofile(filename, codec="mp3")
    clip.close()
    shutil.move(filename, f'{AUDIO_FOLDER}/{filename}')
    print('FILE CREATED AT: ', f'{AUDIO_FOLDER}/{filename}')

def download_video(video_url):
    video = pytube.YouTube(video_url)
    length = video.length
    video = video.streams.get_highest_resolution()
    print('Downloading ' + video.title + '...')

    try:
        video.download(VIDEOS_FOLDER, f'{video.title}.mp4')
    except:
        print("Failed to download video")

    print("video was downloaded successfully")
    return video.title, length

def download_audio(video_url):
    video = pytube.YouTube(video_url)
    length = video.length
    audio = video.streams.filter(only_audio = True).first()
    print('Downloading ' + video.title + '...')

    try:
        audio.download(AUDIO_FOLDER, f'{video.title}.mp3')
    except:
        print("Failed to download audio")

    print("audio was downloaded successfully")
    return video.title, length

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required = False, help = "URL to youtube video")
    ap.add_argument("-pl", "--playlist", required = False, help = "URL to youtube playlist")
    ap.add_argument("-a", "--audio", required = False, help = "audio only", action = argparse.BooleanOptionalAction)
    ap.add_argument("-c", "--crop", required = False, help = "crop video", action = argparse.BooleanOptionalAction)
    ap.add_argument("-cr", "--crop_random", required = False, help = "crop random", action = argparse.BooleanOptionalAction)
    ap.add_argument("-cl", "--crop_length", required = False, help = "crop length")
    ap.add_argument("-cs", "--crop_start", required = False, help = "crop start")
    args = vars(ap.parse_args())

    video_url = ''
    if args["playlist"]:
        playlist = pytube.Playlist(args["playlist"])
        random_video = random.randint(0,playlist.length-1)
        video_url = playlist.video_urls[random_video]

    if args["video"]:
        video_url = args["video"]


    video = None
    if args["audio"]:
        title, length = download_audio(video_url)
        if title and length and args['crop']:
            crop_audio(
                title,
                length,
                crop_length = args["crop_length"] or TIME_LENGTH,
                crop_start = args["crop_start"] or 0,
                crop_random = args["crop_random"] or False
            )
    else:
        title, length = download_video(video_url)
        if title and length and args['crop']:
            crop_video(
                title,
                length,
                crop_length = args["crop_length"] or TIME_LENGTH,
                crop_start = args["crop_start"] or 0,
                crop_random = args["crop_random"] or False
            )
