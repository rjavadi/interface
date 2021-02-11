import os, glob, random


def get_random_video(culture, annotated_videos):
    # TODO: add culture folder
    files = [os.path.basename(x) for x in glob.glob("./static/*.mp4")]
    files.extend([os.path.basename(x) for x in glob.glob("./static/*.avi")])
    print("~~~~All video files: ", files)
    print("####User's annotated videos: ", annotated_videos)
    files.sort()
    annotated_videos.sort()
    # check if user has annotated all files. If yes, return "FINISHED" keyword
    if files == annotated_videos:
        return "FINISHED"
    file = random.choice(files)
    while file in annotated_videos:
        file = random.choice(files)
    return file


