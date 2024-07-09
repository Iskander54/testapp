from dotenv import load_dotenv
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://db_user:your_password@34.76.130.195/first_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
