# Phishing-Awareness-Chatbot

An AI-powered application to enhance awareness regarding phishing


## How to start the app ?

- Ensure you have docker (/ docker desktop on windows) installed on your computer.
    - Please refer to https://www.docker.com/get-started/ for any help
- Clone the repo using `git clone`
- Create a `~/Application/pac-back/envs/.env` file according to `~/Application/pac-back/envs/.env.example` using your keys.
- Create a `~/Application/pac-front/.env` file according to `~/Application/pac-front/.env.example` using your keys.

### To start the backend only:

- Navigate to `./Application/pac-back`
- Start the app using `docker compose up --build`, `--build` being optional, upon first up or upon changes.
- Access the backend's interactive Swaggers at:

| Service Name   | Host      | Port | URL                   |
|----------------|-----------|------|-----------------------|
| Authentication | localhost | 8001 | http://localhost:8001 |


### To start the whole app:

- Navigate to `./Application/pac-back`
- Start the app using `docker compose up --build`, `--build` being optional, upon first up or upon changes.
- Access the app at `http://localhost:8080`
