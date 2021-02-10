import os, glob, random


def get_random_video(culture, annotated_videos):
    # TODO: add culture folder
    files = glob.glob("./static/*.mp4")
    files.extend(glob.glob("*.avi"))
    file = random.choice(files)
    ## TODO: check if user has annotated all files.
    while file in annotated_videos:
        file = random.choice(files)
    return file


