import argparse
import os

content_to_html_mapping = {
    "profile": "profile_photos.html",
    "recently_deleted": "recently_deleted_content.html",
    "reels": "reels.html",
    "stories": "stories.html",
}
parser = argparse.ArgumentParser(description="Orders media downloaded from instagram.")

parser.add_argument(
    "-f",
    "--igfolder",
    metavar="igfolder",
    required=True,
    help="The path to the folder you get after unzipping the zip that Instagram gives you.",
)

parser.add_argument(
    "-c",
    "--content",
    metavar="content",
    choices=["profile", "recently_deleted", "reels", "stories"],
    nargs="+",
    required=True,
)

print(parser.parse_args())

main_folder = parser.parse_args().igfolder
target_content = parser.parse_args().content

media_folder = os.path.join(main_folder, "")

# print(os.listdir(path=))
