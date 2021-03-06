# Dr Manisha Bandishti: Back-End

> This repository is the back-end of Dr Manisha Bandishti's Patient and Diet Management System.

<img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/d3837adb-d1ea-4fae-aef7-4b16e43ffb3d/drm_logo_black.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20200904%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200904T071036Z&X-Amz-Expires=86400&X-Amz-Signature=23cf5f81737cb6103ae403ee81fcbb7c29a48a7a81968052af2346d9c4100978&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22drm_logo_black.png%22">

> View the Project Documentation [here](https://www.notion.so/Dr-Manisha-Bandishti-Back-End-24820115c5564fc9a78c6f9ae30ac0b1).
>
> View the API Documentation [here](https://documenter.getpostman.com/view/8369112/TVKEVwYd).

---
[![Build Status](https://travis-ci.org/SameeranB/drm_backend.svg?branch=master)](https://travis-ci.org/SameeranB/drm_backend)
[![Coverage Status](https://coveralls.io/repos/github/SameeranB/drm_backend/badge.svg?branch=master)](https://coveralls.io/github/SameeranB/drm_backend?branch=master)
## Description:

This is a patient management platform built for Lifestyle and Obesity Management. It allows for patient onboarding, appointment management, diet management, payment portal and so on.


## Setup

This project is built using the `Django Rest Framework` . The following are the steps to setup and run this project:

* Clone the repository.
* Copy the contents of `drm_backend/env_template.txt` to a `drm_backend/.env ` file and fill them out.
* Create your virtual environment and install all the requirements using `pip install -r requirements.txt` .
* Run migrations using `python manage.py migrate`.
* Run tests using `python manage.py test`.
* Create a super-user using `python manage.py createsuperuser`.

## Run

* Run the development server using `python manage.py runserver`.
* Run the development Docker containers using `docker-compose -f Docker/docker-compose.dev.yml  up --build`.
* Run the production Docker containers using `docker-compose -f Docker/docker-compose.prod.yml  up --build`.

## Roadmap

* Add Caching
* Phase 2 - Appointment Management 
* Phase 3 - Diet Preperation and Management
* Phase 4 - Health Monitoring and Activity Logging for Patients

