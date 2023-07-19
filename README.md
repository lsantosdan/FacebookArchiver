FACEBOOK ARCHIVER v0.2
==============================

Facebook Archiver helps you re-add metadata to your Facebook photos once you download them, and reorganizes them in month/year folders for easier importing into other photo management tools.

This was created after many frustrating attempts to download my data in any useable way from Facebook. Metadata is stored separately and filenames are meaningless, which make it incredibly hard for regular users to sort through years of photos and videos outside of Facebook's html viewer.


REQUIREMENTS
============

- Python 3.x

Python Modules (all can be installed with pip):
- imageio
- Pillow
- piexif
- mutagen


PROCESS
=======

1) All json files from messages and photo albums are compiled into a single file.
2) This file is cleaned to fix accented characters and @ mentions.
3) All image and video files are copied to a temp folder. A photosvideos.csv file with all their paths is created.
4) The script goes through this list, and matches timestamps and description (if found in the json) to each file, adding this metadata to photosvideos_metadata.csv. Taken timestamp is preferred, but others are used if this isn't found (for example, message sent timestamp for messaged photos).
5) All PNG and BMP images are converted to JPG.
6) EXIF metadata (photos) and QTFF metadata (videos) for each file is updated with the timestamp extracted, and the description. The filesystem metadata (file creation and last modified date) is also updated with this timestamp to make sure photo importers like synology photos identify the correct date.
7) Photos that you are tagged in are sorted next. There is no metadata unfortunately beyond the filename with the current method, so that gets passed over to EXIF and filesystem metadata as well.
8) Files are moved to Year/Month directories, which are created based on their timestamp/filename. The temp folder is renamed to "UPLOAD".

INSTRUCTIONS
============

1) Put in a request to download a copy of your Facebook information via https://www.facebook.com/dyi/. Format: JSON. Select your media quality and date range. Select ALL information to download.

2) Wait for the file to be generated. This can take over 24 hours. Download it then extract it. It is preferable to keep only the folders "posts" and "messages".

3) Use a third party browser extension such as "Download Albums for Facebook™" to download all the photos in your "photos of you" album (or do it manually). It is located here: https://www.facebook.com/profile.php?id=XXXXXXXXXXXXXXX&sk=photos_of (replace the id with yours). Unfortunately, for reasons that are possibly against GDPR, facebook does not include these in your data download. Move them to a folder named "tagged" in the same directory as your "posts" and "messages" folders.

4) Make sure you have all the required modules and python version. Extract all scripts to the same directory as your folders. Run "FacebookArchiver.py" and wait.


DISCLAIMERS
===========

- Make a copy of your data before attempting this.
- I'm not a coder, so use this at your own peril.
- Partially written by ChatGPT
- Any improvements/advice on how to make this more efficient are most welcome.
- Tested under Windows 10 (64)
- Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)
