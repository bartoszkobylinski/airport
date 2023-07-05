# Air Traffic Control Simulation

## Introduction
Welcome to the Air Traffic Control Simulation project! This application is a simple yet effective simulation of air 
traffic control, where airplanes land at an airport. Written purely in Python and leveraging sockets for communication, 
this application presents an interesting study in concurrent programming and socket communication.

## Features
- Air Traffic Simulation: This application simulates air traffic within a control space of dimensions 10000x10000x5000.
- Airplane Characteristics: Each airplane is simulated with varying properties, such as different initial coordinates 
(within a square area of -5000,5000 and height 2000,5000), velocities, fuel levels, and fuel usage rates.
- Air Traffic Control: The airport can control up to 100 airplanes at a time. It concurrently handles only two 
descending airplanes while the rest are made to fly randomly in the control area.
- Traffic Overflow Handling: In case of more than 100 airplanes, the airport handles the overflow by rejecting access to
the new airplanes and shutting down their corresponding threads.
- Collision Prevention: The simulation also takes into account potential collisions during approach, implementing 
measures to prevent them.
- Database Integration: All information about airplanes and their flight data are persistently stored in a database.

## Technologies Used
- Python: This application is written purely in Python, showcasing the language's capabilities in handling concurrent 
programming, socket communication, and database integration.
- Sockets: The application uses sockets for communication between different components of the simulation, such as 
between airplanes and the airport control.
- Threading: Each airplane is implemented as a separate thread, demonstrating Python's threading capabilities in 
handling concurrent tasks.
- SQLite: All flight data is persistently stored in an SQLite database, which provides lightness, simplicity, and good 
performance for this kind of application.

## Installation and Setup
# Prerequisites
- Python 3.x installed on your system. You can download Python from the official site.
- SQLite comes pre-installed with Python.

# Steps
1. Clone the repository

    If you have git installed, you can clone the repository by running the following command in your terminal:

    ```
    git clone https://github.com/bartoszkobylinski/airport.git
    ```
    Otherwise, you can simply download it as a zip file and extract it.

2. Navigate to the directory

   Use the command line to navigate into the directory where the project resides. You can do this with the ```cd```
   command. For example:

    ```
    cd airport
    ```

3. Set up a virtual environment (Optional)

    This step is optional, but it's good practice to create a virtual environment when running a Python project. This 
keeps any dependencies you install separated from your system-level Python installation, which can prevent versioning 
conflicts. You can create a virtual environment and activate it using the following commands:

    For Unix or macOS:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```
    For Windows:

    ```bash
   py -m venv env
   .\env\Scripts\activate
   ```

4. Install the dependencies

    The dependencies are listed in the requirements.txt file. After activating your virtual environment, you can use the
following command to install these dependencies:

    ```bash 
    pip install -r requirements.txt```


5. Run the application

    Open two terminal windows (or tabs). In the first one, run the following command to start the airport server:

    ```python
    python airport.py
    ```

    In the second terminal window, run the following command to spawn an airplane:
   ```python
   python airplane.py --planes 5
   ```
   You can adjust the number of planes that spawn at any one time by modifying the ```'--planes'``` argument in the 
command. This example would spawn 5 planes. If you don't specify a ```'--planes'``` argument, a random number between 
4 and 15 planes will be spawned by default:
   ```python
   python airplane.py
   ```
   The planes will be continuously spawned at intervals ranging from 5 to 15 seconds. You can adjust this range in the 
```airplane.py``` script.