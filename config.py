import os

from dotenv import (
    load_dotenv
)

load_dotenv()

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:

    SECRET_KEY = os.getenv(
        'SECRET_KEY'
    )

    db_url = os.getenv(
        'DATABASE_URL'
    )

    if db_url and db_url.startswith(
        'sqlite:///'
    ):
        db_path = db_url.replace(
            'sqlite:///',
            ''
        )

        SQLALCHEMY_DATABASE_URI = (
            f"sqlite:///{os.path.join(BASE_DIR, db_path)}"
        )

    else:
        SQLALCHEMY_DATABASE_URI = db_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_DEBUG = (
        os.getenv(
            'FLASK_DEBUG',
            'True'
        ) == 'True'
    )

    FAKE_LOADING_TIME = float(
        os.getenv(
            'FAKE_LOADING_TIME',
            1.5
        )
    )