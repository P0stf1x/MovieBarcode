import subprocess
import tempfile
import os.path
from math import floor
from PIL import Image

class MovieBarCode():
    def __init__(self, videoPath, width=None, height=None, outpath=None):
        print("initializing")
        self.tempfolder = tempfile.mkdtemp()
        tempfile.mkdtemp()
        self.path = videoPath
        print(self.path)
        print(os.path.realpath(self.path))
        self.videoLength = self.get_length()
        self.width = width or floor(self.videoLength)
        self.height = height or self.get_height()
        self.outpath = outpath or f"{os.path.splitext(self.path)[0]}.png"
        self.generate_valid_frames()
        self.generate_frame_data()
        self.generate_barcode()

    def generate_valid_frames(self):
        print("generating frames")
        tempfilepath = os.path.join(self.tempfolder, "frame%04d.jpg")
        print(self.videoLength)
        deltaframe = self.videoLength/self.width
        ffmpegcall = f"ffmpeg -i \"{self.path}\" -y -vf fps=1/{deltaframe} -q:v 2 {tempfilepath}"
        print(ffmpegcall)
        subprocess.call(ffmpegcall)

    def generate_frame_data(self):
        print("generating frame data")
        images = list(map(lambda file: os.path.join(self.tempfolder, file), os.listdir(self.tempfolder)))
        self.frames = list(map((lambda image: Image.open(image).resize((1, self.height), Image.ANTIALIAS)), images))

    def generate_barcode(self):
        barCode = Image.new("RGB", (self.width, self.height))
        for i in range(len(self.frames)):
            barCode.paste(self.frames[i], (i, 0))
        barCode.save(self.outpath)
        for i in os.listdir(self.tempfolder):
            os.remove(os.path.join(self.tempfolder, i))
        os.rmdir(self.tempfolder)
        print("done")
        return barCode

    def get_length(self):
        length = float(subprocess.check_output(f"ffprobe -i \"{self.path}\" -show_entries format=duration -v quiet -of csv=\"p=0\""))
        return length

    def get_height(self):
        height = int(subprocess.check_output(f"ffprobe -v error -show_entries stream=height -of csv=p=0:s=x \"{self.path}\""))
        return height

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Video to movie barcode", usage="%(prog)s [-i INPUT] [options]")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input video path")
    parser.add_argument("-w", "--width", type=int, default=None, help="Output image width")
    parser.add_argument("--height", type=int, default=None, help="Output image height")
    parser.add_argument("-o", "--output", type=str, help="Output image path")
    argv = parser.parse_args()
    if argv:
        a = MovieBarCode(videoPath=argv.input, width=argv.width, height=argv.height, outpath=argv.output)
    else:
        print("No arguments were provided\nTry using --help")