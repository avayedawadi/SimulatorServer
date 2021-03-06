# Introduction

This is a simulation server written for the [Georgia Tech Robotarium](https://www.robotarium.gatech.edu/). This was specifically written for use with the block code project in order to show videos of robot simulation with users who may not be able to set up Python enviornments and run the simulation themselves. However, this simulator can execute any Python code and it is not required for the frontend to just be block code.

# Installation and Usage

1. Clone this repository to your local machine using `git clone`.
2. Activate the Python virtual enviornment named `env`.
3. Run `pip3 install -r ./requirements.txt` in order to install all dependencies.
3. Run `flask run` in the rps directory in order to start the flask server.

# Running Docker

This project can also be run using Docker. The production server uses Gunicorn and by default is set to use 5 web workers and 0 additional threads. Coroutines for concurrency are not currently implemented but could be implemented for better I/O to the server (if needed). 

### Docker Instructions
1. Install Docker on your machine. It is recommended to use WSL2 if on Windows.
2. Run `docker build --tag simulator-server .` to build the Docker image.
3. Run ` docker run -p 5000:5000 simulator-server` to run the Docker image at port 5000.

# Implementation Details
- The Flask server code is in `rps/app.py`.
    - The `/simulationVideo` endpoint is the main endpoint. Data is passed in the body of a post request as JSON in the form:
    ```
    {
        code: [Python Code here]
    }
    ```
    - As seen above, the formatted Python code is posted to the Flask server to generate a video.
    - A timestamp is passed back that is used for accessing the video via URL. The URL of the generated video will be in the URL in the form `/static/uploads/[timestamp].mp4`. Insert the timestamp passed back in the `[timestamp]` above to get the correct url.
    - `app.py` also has a MyWorker Class implemented to run the process as a background thread if wanted.

- The Python code passed to the Flask server is run using the `exec()` command. This is NOT ideal but is the currently implemented method due to time constraints.

- All code to generate the simulation video itself is found in `robotarium.py`. This is NOT ideal because if changes are made to this file by the Georgia Tech Robotarium via Git, changes cannot be pulled due to obvious merge conflicts.

- The video is generated by taking each "step" of the simulation created frame-by-frame and adding these to an image folder (that is uniquely created via a timestamp). Then MoviePy is used to assemble the images into a video and that video is stored as `[timestamp].mp4` in the `static` folder where it can be accessed via a URL.
    - OpenCV was not used to create the videos because of FFMPEG codec issues that did not allow the video to be played easily in browser.
    - Note: MoviePy is relatively slow compared to OpenCV so if the codec issues could be fixed, OpenCV would be a more ideal solution for creating the video.

# Next Steps
- Python code should not continue to be executed using the `exec()` command which has essentially no error handling. 
    - Ideally, the server would pass back error messages to the user via the endpoint directly returning a message which is currently impossible.
    - As a workaround, errors could be passed back via a log file that is written to by the Python.
- The Python simulation video should be created in someway without needing to (majorly) change the `robotarium.py` file. Currently, updating `robotarium.py` would be a major task and that process would need to be streamlined by keeping changes to the base file to a minimum.
- As mentioned above, error handling back to the user is a critical part of programming that is currently not implemented.
- Some form of long-polling to pass continued updates on the progress of the simulation back to the user would enhnace the user experience.
- The project could be updated to use coroutines in order to achieve greater concurrency in the web server. This would only be needed if the server is bottlenecked by I/O. 

