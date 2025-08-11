import argparse
from bs4 import BeautifulSoup
import json
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
    help="The location to save the copied files to. If not specified, defaults to renaming the files in-place rather than making renamed copies.",
    required=False,
    default=False,
)


def main():
    source_path = os.path.normpath(parser.parse_args().igfolder)
    html_json_folder_path = os.path.join(
        source_path, "your_instagram_activity", "media"
    )

    if not os.path.exists(source_path):
        print(
            source_path,
            " does not exist. Please check for typos and make sure to copy the full path of the unzipped folder.",
        )
        return 1

    is_html = os.path.splitext(os.listdir(html_json_folder_path)[0])[1] == ".html"
    file_type = ".html" if is_html else ".json"

    content_to_html_json_mapping = {
        "profile": "profile_photos" + file_type,
        "recently_deleted": "recently_deleted_content" + file_type,
        "reels": "reels" + file_type,
        "stories": "stories" + file_type,
    }
    target_content = parser.parse_args().content
    media_dict = {
        target: {"files": [], "count": None, "zeros": None} for target in target_content
    }

    for target in target_content:
        filename = content_to_html_json_mapping.get(target)
        file_path = os.path.join(html_json_folder_path, filename)

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as f:
            if is_html:
                html = BeautifulSoup(f, "html.parser").find("main")
                media = html.find_all(attrs={"src": True})

                for m in media:
                    media_dict[target]["files"].append(os.path.normpath(m["src"]))

            # is json
            else:
                json_content = json.load(f)

                if target == "reels":
                    for media in json_content.get("ig_reels_media"):
                        media_path = media.get("media")[0].get("uri")
                        media_dict[target]["files"].append(os.path.normpath(media_path))

                elif target == "stories":
                    for media in json_content.get("ig_stories"):
                        media_path = media.get("uri")
                        media_dict[target]["files"].append(os.path.normpath(media_path))

                elif target == "recently_deleted":
                    for media in json_content.get("ig_recently_deleted_media"):
                        media_path = media["media"][0].get("uri")
                        media_dict[target]["files"].append(os.path.normpath(media_path))
                else:
                    for media in json_content.get("ig_profile_picture"):
                        media_path = media["uri"]
                        media_dict[target]["files"].append(os.path.normpath(media_path))

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

            for file in media_dict[media]["files"]:
                rename_target = os.path.join(source_path, file)

                ext = os.path.splitext(rename_target)[1]
                if not os.path.exists(rename_target):
                    print("cant find", rename_target)
                    return 1
                if not os.path.exists(subfolder):
                    os.mkdir(subfolder)
                new_filepath = os.path.join(subfolder, str(count).zfill(zeros)) + ext
                print(new_filepath)

                shutil.copy2(rename_target, new_filepath)
                count -= 1
    else:
        # rename in-place
        for media in media_dict:
            count = media_dict[media]["count"]
            zeros = media_dict[media]["zeros"] + 1

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


if __name__ == "main":
    main()
