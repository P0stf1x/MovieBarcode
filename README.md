# MovieBarcode

This python script is created for generating movie barcodes from videos/movies


Rick and Morty s6e8

![6x08](https://user-images.githubusercontent.com/46126263/205509355-dc85b8bd-c03a-4ad6-b10c-2077f7175881.png)

Starwars (1977) opening

![star-wars-1977-original-opening-crawl](https://user-images.githubusercontent.com/46126263/205510558-2e6572e1-a91b-450e-9da7-771e2a02e38b.png)


# Usage

1. Install python 3.8+ with Pillow 8.0.0+

2. Download and install ffmpeg from https://ffmpeg.org/

3. Run ```python main.py -i Path_to_video [Options]```

# Options

* ```--width``` - Specify resulting image width

* ```--height``` - Specify resulting image height

* ```--output``` - Specify resulting image path (By default it's the same path as input with .png file extension)
