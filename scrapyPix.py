import argparse
import ImageTooker as ima

from check import *
from logger import *
from colorama import just_fix_windows_console

def parse_args():
    parser = argparse.ArgumentParser(description="Download files using URL.")
    parser.add_argument(
        "-u", "--url", 
        required = True, 
        help = "URL of the file to download."
    )
    parser.add_argument(
        "-p", "--path", 
        default = "Downloaded/", 
        help = "Path where the file will be saved. Default is 'Downloaded/'."
    )
    parser.add_argument(
        "-d", "--delay",
        default = 1,
        type = int,
        help = "Delay for image_tooker"
    )
    parser.add_argument(
        "-m", "--max",
        default = -1,
        type = int,
        help="Sets maximum images to download."
    )

    return parser.parse_args()

def main():
    just_fix_windows_console()

    args = parse_args()
    inscode = installs(log)

    URL = args.url
    DOWNLOAD_PATH = args.path
    DELAY = args.delay
    MAX_IMAGES = args.max

    if not __name__.__eq__("__main__") or inscode == 0:
        exit(0)
    else:
        inscode = None
        del inscode

    try:
        log("Starting scraping")
        data = ima.scrape_images(URL, DOWNLOAD_PATH, DELAY, MAX_IMAGES, logger = log)
        log(f"Program ended ({data})", SUCCESS)
        
    except KeyboardInterrupt: pass
    except Exception as exception:
        log(f"Exception: {exception}", ERROR)

    del args

if __name__.__eq__("__main__"):
    main()
