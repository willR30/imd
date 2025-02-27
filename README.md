# Is my Website Down (IMD)

This Python script checks if a given website is active or down.

## Features
- Accepts a text file containing URLs (one per line) as a command-line argument..
- Uses the `requests` library to check the website's status.
- Provides informative messages based on the HTTP response.
- Handles errors such as connection failures and timeouts.

## Prerequisites
- Python 3.x
- `requests` library (`pip install requests`)

## Installation
```bash
# Clone this repository
git clone https://github.com/yourusername/website-status-checker.git

# Navigate to the project directory
cd website-status-checker

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
python script.py https://example.com
```

## Output Examples
```plaintext
✅ The website is active (Code 200).
⚠️ The website responds with a different HTTP status code.
❌ The website is down or inaccessible.
⏳ The website took too long to respond.
```

## License
This project is licensed under the MIT License.


