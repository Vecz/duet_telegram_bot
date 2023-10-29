# Project Documentation
## Project Overview
#### This project is a Telegram bot that provides various functionalities related to controlling a 3D printer. It allows users to monitor the printer's status, capture images, and manage uploaded video files.

# Advantages
## Asynchrony
This project is entirely asynchronous, allowing efficient management of numerous concurrent operations. Asynchronous handling of requests and commands enables optimal resource utilization and maintains high responsiveness of the application.

## Aiogram 3.x
By utilizing aiogram 3.x, we have access to the latest capabilities and improvements for interacting with the Telegram Bot API. This version of the library ensures reliable and flexible interaction with the Telegram API, making it easy to create bots with diverse functionality.

## Modularity
The project is divided into a set of modules, each serving specific functions. This improves code readability and maintainability, as well as facilitates ease of making changes and adding new features.

## Comprehensive Documentation
We place special emphasis on documentation to provide a clear understanding of the project's structure and capabilities of each module. Code comments, README files, and API documentation assist new developers in quickly onboarding to the project and getting started.

### Directory Structure
- #### app/: Contains the main application files.
- #### handlers/: Handlers for processing user commands.
- #### middlewares/: Middleware components for processing updates.
- `models.py`: Defines database models and functions for interacting with the database.
- `camera.py`: Handles capturing images from the printer's camera.
- `keys.py`: Functions for creating keyboard markup and loading messages.
- `compress_video.py`: Module for compressing video files.
- #### config/: Configuration files.
- #### media/: Directory for storing media files.
- #### locale/: Localization files.
- main.py: Main entry point of the application.

## File Descriptions
### app/handlers/
- #### bot_settings.py: Handles user settings and configurations.
- #### list_of_videos.py: Manages the list of uploaded video files.
- #### printer_control.py: Provides functions for controlling the printer.
- #### root.py: Handles root-level commands and settings.
- #### sftp.py: Manages SFTP connections for file transfers.
- #### status.py: Handles status-related commands and actions.
### app/middlewares/
- #### is_root.py: Middleware for checking if a user has root access.
- #### sendFiles.py: Middleware for processing file-related updates.
- #### upload.py: Middleware for handling file uploads.
- #### app/models.py: Defines database models (User and UploadedFiles) and functions for database interactions.
### app/
- #### app/camera.py: Captures images from the printer's camera and saves them as video files.

- #### app/keys.py: Provides functions for creating keyboard markup and loading messages.

- #### app/compress_video.py: Module for compressing video files.

### main.py
- Main entry point of the application. Initializes the bot, sets up components, and starts polling for updates.

## Usage
- Ensure you have the necessary dependencies installed.
- Set up your configuration in config/config.py.
- Run main.py to start the bot.
## Dependencies
- aiogram
- aiohttp
- gino
- ffmpeg-python
- pillow
- redis
- OpenvCv
  maybe something else
## Acknowledgements
This project was developed by Vecz 28.10.2023
Tested with reprapfrimware 3.4.4
## License
#### GNU General Public License v3.0
The source files in this project are licensed under GPLv3, see http://www.gnu.org/licenses/gpl-3.0.en.html.

