# In Order: the instagram media download orderer

You can download all of your stories, reels, and profile pictures by requesting your data from Meta (Settings -> Meta Accounts Centre -> Your information and permissions -> Download your information). The data you get back includes the `media` folder (which contains the actual media files from the stories/reels/profile pictures/recently deleted) and then `your_instagram_activity` folder which has either `.html` or `.json` files containing all the metadata of those media files. Frustratingly, the media files are not given in chronological order. However, they *are* correctly ordered in the HTML/JSON files. This program extracts the correct order from the HTML/JSON files and renames the media files accordingly so that you can view them in chronological order. You can either rename the files in-place, or specify a location to have renamed copies saved to.

## How to use

1. Unzip the file Instagram gives you (make sure to extract it to a contained folder)
2. Open up your command line/ terminal and navigate to the folder where you've saved `inorder.py`
3. Type `py inorder.py` and then the following command-line arguments:

    `-f` specifies the path of the folder that Instagram gives you. For example: 'C:\Users\\[...]\instagram-ig_username-yyyy-mm-dd-xxxxxxxx' for Windows OS or '/users/[...]/instagram-ig_username-yyyy-mm-dd-xxxxxxxx' for MacOS.
    
    `-c` specifies what media you want to order. Must be one or more of the following: "profile", "recently_deleted", "reels", or "stories"

    `-l` (optional) specifies the copy location of the renamed files. If not specified, defaults to renaming the files in-place rather than making renamed copies.
    
