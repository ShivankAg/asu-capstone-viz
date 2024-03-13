# asu-capstone-viz

This repo contains the visualizations we want to add to the SpaceDucks analytics page (https://spaceducks.owlintegrations.com/launch-1)

## Building Locally

Clone the project or download the [zip](https://github.com/trashykoifish1/strongmind-pizza/archive/refs/heads/main.zip)

```shell
$ git clone https://github.com/ShivankAg/asu-capstone-viz.git
```

Ensure that [Python](https://www.python.org/) is installed

```shell
$ python --version
Python 3.11.0
```

> [!NOTE]
> Because the server uses `Django 5.0.1` so `Python >= 3.10` is reccommended

Navigate to the project folder (`python` folder) and create a Python virtual environment

**Windows:**

```shell
$ python -m venv env
$ .\env\Scripts\activate
```

**Mac/Linux:**

```bash
$ python -m venv env
$ source env/bin/activate
```

Ensure that `pip` is installed if not refer to [pip installation guide](https://pip.pypa.io/en/stable/installation/) and install the dependencies

```shell
$ pip --version
pip 22.3 from FILEPATH (python 3.11)
$ pip install -r requirements.txt
```

Run the project locally

```
$ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
February 09, 2024 - 02:20:24
Django version 5.0.1, using settings 'pizza_app.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Navigate to [localhost:8000](http://localhost:8000/) to access the page
