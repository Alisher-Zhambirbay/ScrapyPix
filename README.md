# ScrapyPix

**ScrapyPix** is a Python tool designed for downloading images from URLs with an option to set a delay and a maximum limit for the number of images to download.

## Features
- **Image Scraping**: Downloads images from a given URL.
- **Customizable Settings**: Set a delay between downloads and a maximum number of images to download.
- **Cross-platform**: Works on Windows, Linux, and macOS.
- **Logging**: Provides helpful logging with different levels: `INFO`, `WARN`, `DEBUG`, `SUCCESS` and `ERROR`.

## Installation

Clone the repository:

   ```bash
   git clone https://github.com/Alisher-Zhambirbay/ScrapyPix.git
   cd ScrapyPix
   ```

## Usage

### Command-Line Arguments

The tool can be run from the command line with the following arguments:

- `-u`, `--url`: **Required**. The URL of the page containing images to download.
- `-p`, `--path`: **Optional**. The directory where images will be saved. Default is `downloaded/`.
- `-d`, `--delay`: **Optional**. Delay in seconds between downloads. Default is `1`.
- `-m`, `--max`: **Optional**. The maximum number of images to download. Default is `-1` (download all images).

### Example Command:

```bash
py scrapyPix.py -u "https://example.com/images" -p "images/" -d 2 -m 5
```

This command will scrape images from the URL `https://example.com/images`, save them to the `images/` directory, with a 2-second delay between downloads and a maximum of 5 images.

## How It Works

### 1. **Run the Script**:
The script starts by ensuring the necessary requirements are installed using `install_check()`. It then adds the script's directory to the system’s `PATH` (if not already done) for ease of access.

### 2. **Scraping Images**:
The script uses the `ImageTooker` module to scrape images from the provided URL. It supports setting a delay between requests and limiting the number of images to download.

### 3. **Logging**:
The script logs the progress and any errors or warnings during the scraping process to provide feedback to the user.

## Logs

The script supports three log levels:

- **INFO**: General information about the script's progress.
- **WARN**: Warnings, e.g., when files cannot be added to `PATH`.
- **ERROR**: Errors, e.g., if something goes wrong during scraping or file downloading.
- **SUCCES**: Completed operations, e.g., when something completes successfully.
Logs will be printed to the console with appropriate colors for each log level.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
