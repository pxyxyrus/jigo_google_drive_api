
## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
  - [Prerequisites](#prereq)
  - [Installing](#installing)
  - [Running](#running)
- [Features](#features)
- [Built Using](#built_using)
- [Authors](#authors)

## About <a name = "about"></a>

This Streamlit application allows you to explore and interact with your Google Drive files and folders directly from your browser. It provides a simple interface for navigating through folders, selecting files, and viewing metadata, with the ability to download selected files as a ZIP archive.

## Features <a name="features"></a>

**Google Drive Authentication***: Securely authenticate with your Google account to access your Google Drive.
**Folder Navigation**: Browse through folders in your Google Drive, with the current path displayed at the top.
**File Selection**: View files in the selected folder, with checkboxes to select multiple files.
**Metadata Display**: When a file is selected, its metadata (including name, created date, modified date, and size) is displayed on the right side of the screen.
**Download as ZIP**: After selecting files, you can download them as a ZIP archive.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development.

### Prerequisites <a name = "prereq"></a>

* You need to set up a Google Cloud project, which can be done by following [Google's official quickstart guide](https://developers.google.com/drive/api/quickstart/python) to enable the necessary APIs and obtain your credentials

* In your Google Cloud Console, you'll need to create OAuth 2.0 credentials. After generating the credentials, download the credentials file and save it in a secure location within your project directory

* You need to install Python 3.10 and have virtualenv installed



### Installing <a name = "installing"></a>

First create a python virtual environment

```
virtualenv -p 3.10 .venv
```

Activate the virtual environment
```
source .venv/bin/activate
```

Install required packages
```
pip install -r requirements.txt
```

### Running  <a name = "running"></a>

#### Config Setup
Once you finish installing everything you need to create a `.env` file at the **root directory** of the project containing the following content

```
CONFIG="your_config_folder"
```
where `your_config_folder` should be a folder under [config](./config) containing the `config.toml` file.

There are a few more rules to consider when setting up a new configuration. For detailed information, please refer to the [configuration README](./config/README.md).

You can refer to a sample configuration in [confing/local/config.toml](./config/local/config.toml).

Once everything is set up, you can run the project by the following command.
```
streamlit run app.py
```

To run the locally project after installation
* create a `.env` file at the root directory of the project with the variable `CONFIG="local"`
* run the project


## Built Using <a name = "built_using"></a>

- [Streamlit](https://streamlit.io/) - Frontend Framework
- [GoogleAPIClient](https://github.com/googleapis/google-api-python-client) - Google API Library

## Authors <a name = "authors"></a>

- [@pxyxyrus](https://github.com/pxyxyrus)


