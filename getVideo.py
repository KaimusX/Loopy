from pytube import YouTube
import hashlib
import pandas as pd

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
        
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Download the video and get the file path
video_url = 'https://youtu.be/f4FuR9fTKeo'
video_path = download_youtube_video(video_url)

# Calculate the MD5 hash of the downloaded video
md5Hash = calculate_md5(video_path)

# Create a DataFrame with the file path and MD5 hash
df = pd.DataFrame({'File_Path': [video_path], 'MD5_Hash': [md5Hash]})

# Save the DataFrame to a CSV file
df.to_csv('file_info.csv', index=False)