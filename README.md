# Mapexify
A web application that collects data from the user and then presents a map with marked routes between points and information about the trip.

## Table of Contents
- [Introduction](#introduction)
- [Project structure](#project-structure)
- [Before run](#before-run)
- [How to Run](#how-to-run)

## Introduction
The application allows you to determine a road route between selected points on the map. The user enters values ​​such as country, city, street, house number or postal code in `search` tab. After clicking the button, a list of suggestions with places will appear below.

After selecting the appropriate option, a list of route points will be displayed in the `plan` tab. After selecting all points **(2 - 10)** and pressing the **submit** button in the **plan** tab, a layer with a road route between the entered points will be applied to the map.

In the `vehicle` tab, you can select profile and currency to calculate the informations about route and costs. After accepting, information on the distance, time and cost of the trip will be displayed.

## Project structure
```
.
├── app
│   ├── requirements.txt
│   └── website
│       ├── main.py
│       ├── mapexify.py
│       ├── static.py
│       ├── static
│       │   ├── scripts.js
│       │   ├── styles.css
|       |   └── src
|       |       └── favicon.png
│       └── templates
│           └── home.html
├── docker-compose.yml
├── Dockerfile
├── nginx
│   └── default.conf
└── README.md
```


## Before run
First of all, put your API key in a file `app/website/static.py`
```python
api_key = "YOUR_APY_KEY"
```

## How to Run
If you have docker you can use this commends to run app

```bash
$ sudo docker-compose up -d --build
``` 
or
```bash
$ sudo docker-compose build && sudo docker-compose up -d
```

After a while the application will open in `localhost:5000` in your browser.
