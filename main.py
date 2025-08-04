import argparse
from bs4 import BeautifulSoup
from bs4 import Tag
import os


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

    master_path = parser.parse_args().igfolder

    html_folder_path = os.path.join(master_path, "your_instagram_activity", "media")

    content_to_html_mapping = {
        "profile": "profile_photos.html",
        "recently_deleted": "recently_deleted_content.html",
        "reels": "reels.html",
        "stories": "stories.html",
    }

    target_content = parser.parse_args().content

    media_dict = {target: set() for target in target_content}

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
                # print(m)
                media_dict.get(target).add(m.get("src"))

    print(media_dict)
    # print(dir(Tag))
    # #         imgs = html.find_all("img")
    #         for img in imgs:
    #             src = img.get("src")

    #             media_dict.get(target).append(os.path.join(master_path, src))

    # print(media_dict)

main()
