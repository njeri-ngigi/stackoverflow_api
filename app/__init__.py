'''app/__init__.py'''
from app.models import User, Question
from app.application import create_app
from app.views import (Signup, Login, Logout, BLACKLIST,
                       Questions, QuestionsQuestionId, QuestionsAnswers, QuestionsAnswersId)
