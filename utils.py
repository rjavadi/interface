import os, glob, random


def get_random_video(culture, annotated_videos):
    # TODO: add culture folder
    base_dir = ""
    if culture == "north american":
        base_dir = "na/"
    elif culture == "persian":
        base_dir = "persian/"
    elif culture == "filipino":
        base_dir = "filipino/"
    files = [base_dir + os.path.basename(x) for x in glob.glob("./static/" + base_dir + "*.mp4")]
    files.extend([base_dir + os.path.basename(x) for x in glob.glob("./static/" + base_dir + "*.avi")])
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


