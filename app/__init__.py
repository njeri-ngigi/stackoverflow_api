'''app/__init__.py'''
from models import User, Question
from application import createApp
from views import (Signup, Login, Logout, BLACKLIST,
                    Questions, QuestionsQuestionId, QuestionsAnswers, QuestionsAnswersId)
