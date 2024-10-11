# simpleipynb2tex

## Overview
`simpleipynb2tex` is a simple script to convert Jupyter Notebook files (`.ipynb`) to LaTeX (`.tex`) format. This tool requires `imgkit` and `wkhtmltopdf` to create images on html outputs.
## Requirements
For up to date instructions refer to [imgkit project on Pypi](https://pypi.org/project/imgkit/)
### Install imgkit
```sh
pip install imgkit
```

### Install wkhtmltopdf

#### Debian/Ubuntu
```sh
sudo apt-get install wkhtmltopdf
```

#### MacOSX
```sh
brew install --cask wkhtmltopdf
```

#### Windows and Other Options
Check the [wkhtmltopdf homepage](https://wkhtmltopdf.org/).

## Usage
To use the `simpleipynb2tex` script, you need to provide the following parameters:
- **Title**: The title of the document.
- **Author**: The author's name.
- **ipynb path**: The path to the Jupyter Notebook file.
- **tex path**: The path where the LaTeX file will be saved.

## License
This project is licensed under the MIT License.