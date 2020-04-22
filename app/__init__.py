#import bibliotek
from flask import Flask

#tworzenie obiektu klasy Flask reprezentującego aplikację
app = Flask(__name__)

#import widoków/routingów z aplickaji
from app import views

#uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)