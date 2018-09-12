# Stackoverflow-Lite API
StackOverflow-Lite is an app that allows a user to post questions, answer other questions posted on the forum. Users can accept answers to their questions and view various statistics involved such as the number of questions asked or answered.<br>
The api provides endpoints for signup, login, logout, retrieve all or a single question, post a question, answer a question and update an answer or accept an answer.

###### Travis CI [![Build Status](https://travis-ci.org/njeri-ngigi/stackoverflow_api.svg?branch=badges)](https://travis-ci.org/njeri-ngigi/stackoverflow_api) <br> Coveralls [![Coverage Status](https://coveralls.io/repos/github/njeri-ngigi/stackoverflow_api/badge.svg?branch=badges)](https://coveralls.io/github/njeri-ngigi/stackoverflow_api?branch=badges) <br>  Code Climate [![Maintainability](https://api.codeclimate.com/v1/badges/f1bd8db087f96b7543ea/maintainability)](https://codeclimate.com/github/njeri-ngigi/stackoverflow_api/maintainability)

#### Endpoints available:
| http methods |    Endpoint route                          |   Endpoint functionality                                     |
| ------------ | ----------------------------------         | ------------------------------------------------------------ |
| POST         | /api/v1/auth/signup                        |   Creates a user account                                     |
| POST         | /api/v1/auth/login                         |   Logs in a user                                             |
| POST         | /api/v1/auth/logout                        |   Logs out a user                                            |
| GET          | /api/v1/questions                          |   Get all questions on platform                              |
| POST         | /api/v1/questions                          |   Post a new question                                        |
| GET          | /api/v1/questions/<question_id>            |   Get a single question                                      |
| DELETE       | /api/v1/questions/<question_id>            |   Delete a question                                          |
| POST         | /api/v1/questions/<question_id>/answers    |   Post an answer                                             |
| GET          | /api/v1/questions/<question_id>/answers    |   Get all answers for a question                             |
| PUT          | /api/v1/questions/<question_id>/answers/<answer_id>           |   Edit or accept an answer                |
| POST         | /api/v1/questions/<question_id>/answers/<answer_id>/upvote    |   Upvote an answer                        |
| POST         | /api/v1/questions/<question_id>/answers/<answer_id>/downvote  |   Downvote an answer                      |
| GET          | /api/v1/users/questions                    |   Get all questions asked by user                            |
| POST         | /api/v1/questions/<question_id>/answers/<answer_id>/comments  |   Post a comment                          |
| GET          | /api/v1/questions/<question_id>/answers/<answer_id>/comments  |   Get all comments for an answer          |
| PUT          | /api/v1/questions/<question_id>/answers/<answer_id>           |   Edit comment                            |
|              | /comments/<comments_id>                    |                                                              |
| POST         | /api/v1/questions/search?limit=10          |   Search a question                                          |

## Prerequisites
      pip
      virtualenv
      python 3
      postgresql
## Setting up database
      Open Postgres PgAdmin and create 2 databases test_db and db_stackoverflow_lite
## Installation
   clone repo:
   ```
   https://github.com/njeri-ngigi/stackoverflow_api.git
   ```
   create virtual environment: 
   ```
   virtualenv <environment name>
   ```
   activate environment:
   ```
   $source <path to env name>/Scripts/activate (in bash)
   ```
   install dependencies:
   ```
   $pip install -r requirements.txt
   ```
   To run the application:
   ```
   $python run.py
   ```
## Running the tests
  The tests for this API are written using the python module unittests. The tests are found in the folder tests.
  Use nose to run the tests.<br>
  To run the tests:
      
   ```
   $nosetests tests/
   ```
  To show coverage:
   ```
   $nosetests tests/ --with-coverage
   ```
## Documentation
[Go to Stackoverflow-Lite Documentation on apiary.io](https://stackoverflowlite17.docs.apiary.io/#)

## Hosting
The app is hosted on heroku<br>
[Go to Stackoverflow-lite](https://my-stackoverflow-lite-api.herokuapp.com/)

## Built with 
   Flask, a python framework
   
## Authors
[Njeri Ngigi](https://github.com/njeri-ngigi)
