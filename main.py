import argparse
from bs4 import BeautifulSoup
import os
import shutil

parser = argparse.ArgumentParser(
    description="Chronologically orders media downloaded from instagram."
)
parser.add_argument(
    "-f",
    "--igfolder",
    metavar="igfolder",
    required=True,
    type=str,
    help=r"The path of the folder that Instagram gives you. For example: 'C:\Users\[...]\instagram-ig_username-yyyy-mm-dd-xxxxxxxx' or '/users/[...]/instagram-ig_username-yyyy-mm-dd-xxxxxxxx'",
)
parser.add_argument(
    "-c",
    "--content",
    type=str.lower,
    metavar="content",
    choices=["profile", "recently_deleted", "reels", "stories"],
    help='The content you wish to order. Should be one or more of the following: "profile", "recently_deleted", "reels", and "stories"',
    nargs="+",
    required=True,
)
parser.add_argument(
    "-l",
    "--copylocation",
    metavar="copylocation",
    type=str,
    help="The location to save the copied files to. If not specified, defaults to renaming the files in-place rather than making renamed copied.",
    required=False,
    default=False,
)


def main():
    source_path = os.path.normpath(parser.parse_args().igfolder)
    html_folder_path = os.path.join(source_path, "your_instagram_activity", "media")
    content_to_html_mapping = {
        "profile": "profile_photos.html",
        "recently_deleted": "recently_deleted_content.html",
        "reels": "reels.html",
        "stories": "stories.html",
    }
    target_content = parser.parse_args().content
    media_dict = {
        target: {"files": [], "count": None, "zeros": None} for target in target_content
    }
    for target in target_content:
        filename = content_to_html_mapping.get(target)
        file_path = os.path.join(html_folder_path, filename)

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as f:
            html = BeautifulSoup(f, "html.parser").find("main")
            media = html.find_all(attrs={"src": True})

            for m in media:
                media_dict[target]["files"].append(os.path.normpath(m["src"]))

    for media in media_dict:
        media_dict[media]["files"] = list(dict.fromkeys(media_dict[media]["files"]))
        media_dict[media]["count"] = len(media_dict[media]["files"])
        media_dict[media]["zeros"] = len(str(media_dict[media]["count"]))

    if copy_location := parser.parse_args().copylocation:
        # copy rename
        if not os.path.exists(copy_location):
            print(copy_location, "doesnt exist, creating new folder.")
            os.mkdir(copy_location)
        for media in media_dict:
            count = media_dict[media]["count"]
            zeros = media_dict[media]["zeros"] + 1

            subfolder = os.path.join(copy_location, media)
            os.mkdir(subfolder)
            print(subfolder)


            for file in media_dict[media]["files"]:
                rename_target = os.path.join(source_path, file)

                ext = os.path.splitext(rename_target)[1]
                if not os.path.exists(rename_target):
                    print('cant find', rename_target)
                    return
                if not os.path.exists(subfolder):
                    os.mkdir(subfolder)
                new_filepath = (
                    os.path.join(subfolder, str(count).zfill(zeros)) + ext
                )
                print(new_filepath)

                shutil.copy2(rename_target, new_filepath)
                count -= 1
    else:
        # rename in-place
        for media in media_dict:
            count = media_dict[media]["count"]
            zeros = media_dict[media]["zeros"] + 1

            # do rename
            for file in media_dict[media]["files"]:
                rename_target = os.path.join(source_path, file)
                new_filepath = (
                    os.path.join(
                        os.path.dirname(rename_target), str(count).zfill(zeros)
                    )
                    + os.path.splitext(rename_target)[1]
                )
                os.rename(rename_target, new_filepath)
                count -= 1

main()
