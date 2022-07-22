from flask import Flask, render_template, url_for, redirect
from sqlalchemy import false
from forms import RegistrationForm
from stockinfo import getinfo, getlabels, getvalues
from newsdata import getnews
from forms import LoginForm, RegistrationForm, StockSearchForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, login_user, UserMixin, logout_user
import secrets


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


###Changes made###
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


'''
y finance, flask, flask wtf, newsdataapi, these are the required imports, form ,flask_behind_proxy, email_validator, flask_login
'''


db = SQLAlchemy(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Pref(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    stockticker = db.Column(db.String(6), unique=True, nullable = False)

    def __repr__(self):
        return f"User('{self.stockticker}')"

db.create_all()

def getpopularstocks(stocklist, timeperiod, timeinterval = ''):
    stocksinfo = []
    stocks = set(stocklist)
    for stock in stocks:
        stockdict = {}
        priceaction = getvalues(stock, timeperiod, timeinterval)

        trend = ''
        if priceaction[0] <= priceaction[len(priceaction) - 1]:
            trend = 'Up'
        else:
            trend = 'Down'
        
        percentchange = ((priceaction[len(priceaction) - 1] - priceaction[0]) / priceaction[0]) * 100
        pricechange = priceaction[len(priceaction) - 1] - priceaction[0]
        stockdict[stock] = {'Date' : getlabels(stock, timeperiod, timeinterval), 'Close' : getvalues(stock, timeperiod, timeinterval), 'Trend' : trend, 'PercentChange' : percentchange, 'PriceChange' : pricechange}
        stocksinfo.append(stockdict)
    return stocksinfo

#--------------------------------------------------------------------------------------------------------------------------#
'''
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
'''
@login_manager.user_loader
def get_user(id):
  return User.query.get(int(id))

@app.route('/')
def index():
    index = getpopularstocks(['^IXIC', '^GSPC', '^DJI'], '1d', '1m')
    ticker = ['NFLX', 'AAPL', 'AMC', 'GME']

    if current_user.is_authenticated:
        for x in Pref.query.filter_by(username = current_user.username).all():
            ticker.append(x.stockticker)
   
    stocks = getpopularstocks(ticker, '1d', '1m')
    news = getnews()
    return render_template('home.html', majorindexes = index, stocklists = stocks, stocknews = news, status = current_user.is_authenticated)

@app.route('/stocksearch.html', methods = ["POST", "GET"])
def search():
    form = StockSearchForm()
    
    if form.validate_on_submit():
        ticker = form.ticker.data.upper()
        period = form.timeperiod.data
        interval = form.timeinterval.data

         
        info = getinfo(ticker)

        #TODO: Add time span and interval

        labels = getlabels(ticker, period, interval)
        values = getvalues(ticker, period, interval)

        trend = ''
        if values[0] <= values[len(values) - 1]:
            trend = 'Up'
        else:
            trend = 'Down'
        
        percentchange = ((values[len(values) - 1] - values[0]) / values[0]) * 100
        pricechange = values[len(values) - 1] - values[0]

        if current_user.is_authenticated and Pref.query.filter_by(stockticker = ticker).all() == []:
            newpref = Pref(username = current_user.username, stockticker = ticker)
            db.session.add(newpref)
            db.session.commit()

        return render_template('stocksearch.html', form = form, infodict = info, labels = labels, values = values, 
                                trend = trend, percentchange = percentchange, pricechange = pricechange, status = current_user.is_authenticated)        
    
    return render_template('stocksearch.html', form = form)

@app.route("/register.html", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): 
        if current_user.is_authenticated == False:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('home')) 
    

    return render_template('register.html', title='Register', form=form, status = current_user.is_authenticated)


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if current_user.is_authenticated == False:
            user = User.query.filter_by(username = form.username.data, password = form.password.data).first()
            db = User.query.all()
            if user != None:
                login_user(user)
                return redirect(url_for('home'))

    return render_template('login.html', title="Login", form=form, status = current_user.is_authenticated)

@app.route('/home.html')
def home():
    index = getpopularstocks(['^IXIC', '^GSPC', '^DJI'], '1d', '1m')
    ticker = ['NFLX', 'AAPL', 'AMC', 'GME']

    if current_user.is_authenticated:
        for x in Pref.query.filter_by(username = current_user.username).all():
            ticker.append(x.stockticker)
   
    stocks = getpopularstocks(ticker, '1d', '1m')
    news = getnews()
    return render_template('home.html', majorindexes = index, stocklists = stocks, stocknews = news, status = current_user.is_authenticated)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/resources.html')
def resources():
    return render_template('resources.html')

if __name__ == '__main__':
    app.run(debug = True, port = 0)