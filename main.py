import argparse
import os

html_folder = "your_instagram_activity"

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
# print(parser.parse_args())


def main():

    main_folder = parser.parse_args().igfolder  # master folder

    # targent_content has the content type ("profile", "recently_deleted", "reels", "stories") as the key and a list of the full file paths as the values
    target_content = {content: [] for content in parser.parse_args().content}

    print()

    for content in target_content.keys():
        path = os.path.join(main_folder, "media", content)
        for subdir in os.listdir(path):
            full_dir_path = os.path.join(path, subdir)
            for file in os.listdir(full_dir_path):
                full_file_path = os.path.join(full_dir_path, file)
                target_content[content].append(full_file_path)

    print(target_content)


main()
