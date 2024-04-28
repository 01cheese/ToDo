from pytube import YouTube


def download_video(url, save_path, resolution='720p'):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=f"{resolution}").first()
        stream.download(output_path=save_path)
        print("The end")
    except Exception as e:
        print("Error:", str(e))
