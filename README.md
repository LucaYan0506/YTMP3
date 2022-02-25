# YTMP3
I created a website using Django Rest Framework for the backend and HTML & CSS & JS for the backend.
I used pytube to download YouTube video.
This is a website where users can convert YouTube video to MP3 and download it.

## How to run your application:
Make sure that [python](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installation/) and [pipenv](https://pipenv.pypa.io/en/latest/install/) are installed  
#### set up virtual environment 
```
pipenv install django  
pipenv shell
pip install -r requirements.txt
```

#### run the app
```
python manage.py migrate
python manage.py runserver
```

## LIVE DEMO: https://ytmp3.herokuapp.com/
![Image of the website](https://github.com/LucaYan0506/YTMP3/blob/master/Screenshot%202022-02-19%20193931.jpg)
