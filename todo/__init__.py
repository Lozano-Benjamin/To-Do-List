import os
from flask import Flask

def create_app():
    app=Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='mikey',
        
    )
