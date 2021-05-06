import os, glob, random, math
import string
import secrets
import logging

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


logging.basicConfig(level=logging.DEBUG)


def get_random_video(culture, annotated_videos, user_id):
    logging.debug("cuture: {}".format(culture))
    base_dir = ""
    if culture == "north american":
        base_dir = "na/"
    elif culture == "persian":
        base_dir = "persian/"
    elif culture == "filipino":
        base_dir = "filipino/"
    # Find the integer part of user id
    counter = int(user_id[user_id.find('_')+1:])
    logging.debug("user counter: {}".format(counter))
    even = '02468'
    odd = '13579'
    even_files = []
    odd_files = []
    files = [base_dir + os.path.basename(x) for x in glob.glob("./static/" + base_dir + "*.mp4")]
    for f in files:
        dot_index = f.find('.')
        last_digit = f[dot_index - 1]
        if last_digit in even:
            even_files.append(f)
        elif last_digit in odd:
            odd_files.append(f)
    logging.debug("odd files: {}".format(odd_files))
    logging.debug("even files: {}".format(even_files))
    user_files = None
    if counter % 2 == 0:
        user_files = even_files
    else:
        user_files = odd_files

    remaining_videos = list(set(user_files) - set(annotated_videos))
    logging.debug("remaining_videos: {}".format(remaining_videos))
    if len(remaining_videos) == 0:
        logging.debug("all files annotated by user")
        return "FINISHED"

    file = random.choice(remaining_videos)
    logging.debug("returning file")
    return file


def get_completed_videos(culture, annotated_videos):
    base_dir = ""
    if culture == "north american":
        base_dir = "na/"
    elif culture == "persian":
        base_dir = "persian/"
    elif culture == "filipino":
        base_dir = "filipino/"
    all = math.ceil(len(glob.glob("./static/" + base_dir + "*.mp4")) / 2)
    completed = len(set(annotated_videos))

    return completed, all

def count_gift_cards(culture, annotated):
    completed, all = get_completed_videos(culture, annotated)
    if completed == all:
        return 2
    if completed >= 20:
        return 1
    return 0



def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    # return ''.join(random.choice(chars) for _ in range(size))
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(size))