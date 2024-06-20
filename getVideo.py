from pytube import YouTube

#downloads the video and puts it into the Video_Media folder
def download_youtube_video(url, output_path='Video_Media'):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream available
        stream = yt.streams.get_highest_resolution()

        # Download the video
        video_path = stream.download(output_path)

        print(f'Download completed: {yt.title}')
        return video_path
    except Exception as e:
        print(f'An error occurred: {e}')

# Replace 'YOUR_VIDEO_URL' with the URL of the YouTube video you want to download
video_url = 'https://youtu.be/f4FuR9fTKeo'
video_path = download_youtube_video(video_url)
print(video_path)

# video_url = 'https://www.youtube.com/watch?v=S3F1vZYpH8c'
# video_url = 'https://www.youtube.com/watch?v=BT5mqjOyvK0'
# video_url = 'https://www.youtube.com/watch?v=AH5xSq3mKfQ'
# video_url = 'https://www.youtube.com/watch?v=phABhg_Um2E'
# video_url = https://www.youtube.com/watch?v=Xbe1LuXzrKU'