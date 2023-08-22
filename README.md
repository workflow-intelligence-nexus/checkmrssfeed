# MRSS Feed URL Checker

## Overview

The `checkmrss.py` script is designed to process an MRSS (Media Really Simple Syndication) feed and identify URLs that are not publicly downloadable. Specifically, it checks for URLs that return an "Access Denied" error message.

## Features

- **Efficient URL Checking**: Uses the HTTP `HEAD` method to quickly check URLs without downloading the entire content.
- **Parallel Processing**: Employs parallel processing to speed up the checking of multiple URLs.
- **Flexible URL Detection**: Identifies any XML element with a `url` attribute, allowing for flexible detection of URLs within the MRSS feed.

## Requirements

- **Python 3.6 or higher**
- **Requests Library**: Required for making HTTP requests.

You can install the Requests library using the following command:

\`\`\`bash
pip install requests
\`\`\`

## Usage

### Command Line

Run the script from the command line with the following syntax:

\`\`\`bash
python3 checkmrss.py <MRSS_Feed_URL>
\`\`\`

Replace `<MRSS_Feed_URL>` with the URL of the MRSS feed you want to check.

### Example

\`\`\`bash
python3 checkmrss.py https://s3.us-west-2.amazonaws.com/iconik-mrss-feeds/mrss-collection-55c8a372-3e1b-11ee-a807-6a717ad5a8d9.xml
\`\`\`

## Output

The script prints the URLs that lead to an "Access Denied" error page.

## How It Works

1. **Download MRSS Feed**: Downloads the specified MRSS feed and parses the XML content.
2. **Identify URLs**: Finds all elements with a `url` attribute within the XML document.
3. **Check URLs**: Sends a `HEAD` request to each URL to retrieve the headers without downloading the body. If the `Content-Type` indicates an error page, a `GET` request is made to check for the specific "Access Denied" message.
4. **Parallel Processing**: Utilizes a thread pool to check multiple URLs simultaneously, reducing the overall time taken.
5. **Print Results**: Prints the URLs that lead to an "Access Denied" error page.

## License

Please refer to the project's license documentation for information on how you can use, modify, and distribute this code.

## Support and Contribution

Feel free to open issues or submit pull requests as needed. Your contributions are welcome!
