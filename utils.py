import os, glob, random
import string
import secrets

persian_fe = ['پوزخند', 'لبخند', 'خونسرد', 'دندان به هم فشردن', 'لبهای به هم فشرده',
              'جمع کردن لبها به سمت پایین', 'بالابردن لب بالایی','بالابردن گوشه لب',
              'از گوشه چشم نگاه کردن', 'تنگ کردن چشمها', 'بستن چشمها', 'بالابردن ابرو', 'ابروهای گره خورده', 'بینی چین خورده',
              'تکان دادن سر', 'سر برگرداندن', 'دست به سینه', 'ادا درآوردن']

filipino_fe = ['Ngisi', 'Ngumingiti', 'Mahinahon', 'Nakaangil', 'Nakasara nang mariin ang mga labi', 'Pabagsak na mga labi', 'Nakataas ang itaas na labi', 'Nakataas ang sulok ng labi',
               'Mata sa gilid', 'Nanliliit ang mga mata', 'Nagsasara ang mata', 'Nakataas ang kilay', 'Magkasalubong ang kilay', 'Ilong na may kunot',
               'Napapailing ang ulo', 'Nakabiling ang ulo', 'Naka krus ang braso', 'Nanunuya']

english_fe = ['Smirk', 'Smiling', 'Calm', 'Snarl', 'Lips pressed togethers', 'Downturned lips', 'Raised upper lip', 'Raised lip corner',
              'Side eye', 'Squinting', 'Closing eyes', 'Raised Eyebrow', 'Eyebrows pushed together', 'Wrinkled nose',
              'Shaking head', 'Head turned away', 'Arms crossed', 'Mocking']


def get_random_video(culture, annotated_videos):
    base_dir = ""
    if culture == "north american":
        base_dir = "na/"
    elif culture == "persian":
        base_dir = "persian/"
    elif culture == "filipino":
        base_dir = "filipino/"
    files = [base_dir + os.path.basename(x) for x in glob.glob("./static/" + base_dir + "*.mp4")]

    files.sort()
    annotated_videos.sort()
    # check if user has annotated all files. If yes, return "FINISHED" keyword
    if files == annotated_videos:
        return "FINISHED"
    file = random.choice(files)
    while file in annotated_videos:
        file = random.choice(files)
    return file


def get_completed_videos(culture, annotated_videos):
    base_dir = ""
    if culture == "north american":
        base_dir = "na/"
    elif culture == "persian":
        base_dir = "persian/"
    elif culture == "filipino":
        base_dir = "filipino/"
    all = len(glob.glob("./static/" + base_dir + "*.mp4"))
    completed = len(set(annotated_videos))
    return "{} out of {} clips completed.".format(completed, all)


def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    # return ''.join(random.choice(chars) for _ in range(size))
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(size))