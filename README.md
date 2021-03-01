# themightyduck

Hack30 Mini Hackathon project

`Quiz Platform`

`Covid Cases Count`
Tracks Covid Cases Daily with search functionality for a particular city

# How To Run Project:-

1.  Fork this repository.
2.  Clone the forked repository from `https://github.com/tusharrao198/themightyduck`

3.  You can have the project running in a virtual environment or otherwise. Virtual environment is a preferred option.

    **Steps to set up a virtual environment for this project**

    1. Create a virtual environment using `python3 -m venv venv` or `virtualenv venv`
    2. Activate virtual environment -

       **For Linux** `source venv/bin/activate`

       **For Windows** `venv\Scripts\activate`

    3. Install required modules using `pip3 install -r requirements.txt`.

4.  Store your secrets by adding them at the end of `venv/bin/activate`. They will be set whenever you run the virtual environment.

    **On Linux** `export SECRET_KEY=''`

    **On Windows** `set SECRET_KEY=''`

5.  Change directory to src using `cd src`.
6.  Check your changes before running `python manage.py check`.
7.  Run the server on your machine using `python manage.py runserver`. Now head over to the url provided in the terminal after running server. or `http://127.0.0.1:8000/`

To check created REST API Data using django rest framework :
`http://127.0.0.1:8000/covidtracker/api/districts/`
`http://127.0.0.1:8000/covidtracker/api/states/`

Done!.
