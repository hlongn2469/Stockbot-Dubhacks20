import os 
import discord
from discord.ext import commands
from discord.utils import get
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import mysql.connector

db = mysql.connector.connect(
    host="35.224.238.245",
    user="root",
    passwd="root",
    database="data"
)
mycursor = db.cursor()

CLIENT = commands.Bot(command_prefix='/')
TOKEN = 'NzY3MTIzNzY1Mjg3OTc2OTgw.X4tVrg.sGqgDpX_Q3rbX6jXYs5C1CirCd8'

URL = 'https://finance.yahoo.com/quote/'

# Get options for chrome and make it headless when testing
# with the console message interupting
options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument('log-level=3')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument('headless')

# initialize the driver
driver = webdriver.Chrome(chrome_options=options)


# Selenium Driver for Chrome
try:
    path = r'chromedriver.exe'
except:
    path = "/chromedriver"

# When you type /ping
# the bot will say "pong!"
@CLIENT.command()
async def ping(ctx):
    await ctx.send("pong!")

@CLIENT.command()
async def sendhelp(ctx):

    await ctx.send("```You have to put the company ticker after each command with a space in between!```")
    await ctx.send("```E.g: /price BABA```")
    await ctx.send("```/price  -   Current stock price```")
    await ctx.send("```/nprice  -   Net price: Price difference between the current price and the previous closing period```")
    await ctx.send("```/npercent  -   Net price in percentage```")
    await ctx.send("```/info  -   Display basic info of stock```")
    await ctx.send("```/advinfo  -   Display advanced info of stock```")
    
# Earning per share
@CLIENT.command()
async def eps(ctx, arg1):
    try:
        await ctx.send("Loading stock data...")
        newURL = URL + arg1 +"?p=" + arg1

        driver.get(newURL)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        results = soup.find(id="quote-summary")
        if(results.find('td', {'data-test': 'EPS_RATIO-value'})):
            eps = results.find('td', {'data-test': 'EPS_RATIO-value'})
        else:
            eps = results.find('td', {'data-reactid': '153'})
        await ctx.send("Earnings per share " + eps.text.strip())
        await ctx.send("-------------------------")
    except:
        await ctx.send("Hmmm... Something wrong? :( ")

@CLIENT.command()
async def price(ctx, arg1):
    try:
        await ctx.send("Loading stock data...")
        newURL = URL + arg1 +"?p=" + arg1

        driver.get(newURL)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Get current price
        results = soup.find(id="Lead-3-QuoteHeader-Proxy")
        stock_elems = results.find("div", class_="D(ib) Mend(20px)")
        price = stock_elems.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
        cur_price_phrase = "Current price: $" + price.text.strip() 
        await ctx.send(cur_price_phrase)
    except:
        await ctx.send("Hmmm... Something wrong? :( ")

@CLIENT.command()
async def nprice(ctx, arg1):
    try:
        await ctx.send("Loading stock data...")
        newURL = URL + arg1 +"?p=" + arg1

        driver.get(newURL)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        results = soup.find(id="Lead-3-QuoteHeader-Proxy")
        stock_elems = results.find("div", class_="D(ib) Mend(20px)")
        price = stock_elems.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")

        # Get net price
        if (stock_elems.find("span", class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")):
            price = stock_elems.find("span", class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")
        else:
            price = stock_elems.find("span", class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)")
        net_price_phrase = "Net price: $" + (price.text.strip().split()[0])
        await ctx.send(net_price_phrase)
    except:
        await ctx.send("Hmmm... Something wrong? :( ")

@CLIENT.command()
async def npercent(ctx, arg1):
    try:
        await ctx.send("Loading stock data...")
        newURL = URL + arg1 +"?p=" + arg1

        driver.get(newURL)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        results = soup.find(id="Lead-3-QuoteHeader-Proxy")
        stock_elems = results.find("div", class_="D(ib) Mend(20px)")
        price = stock_elems.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")

        # Get net price
        price = -1
        if(stock_elems.find("span", class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")):
            price = stock_elems.find("span", class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")
        else:
            price = stock_elems.find("span", class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)")
        percent = float(price.text.strip().split()[1].replace('(', '').replace(')', '').replace('%', ''))
        net_percent_change = "Net percent change of " + arg1 + ": " + str(percent) + "%"
        await ctx.send(net_percent_change)
    except:
        await ctx.send("Hmmm... Something wrong? :( ")

# When you type /hello
# the bot will say "hello!"
@CLIENT.command()
async def hello(ctx):
    await ctx.send("hello!")

@CLIENT.command()
async def info(ctx, arg1):
    try:
        await ctx.send("Loading stock data...")
        newURL = URL + arg1 +"?p=" + arg1

        driver.get(newURL)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find(id="quote-summary")

        # Previous Closing Price of stock
        pprice = str(results.find('span', {'data-reactid': '98'}).text.strip())
        await ctx.send("Previous Closing: $" + pprice)
        await ctx.send("-------------------------")
        # Open Price
        oprice = str(results.find('span', {'data-reactid': '103'}).text.strip())
        await ctx.send("Open Price: $" + oprice)
        await ctx.send("-------------------------")

        # Day Range
        if(results.find('td', {'data-test': 'DAYS_RANGE-value'})):
            dRStatus = results.find('td', {'data-test': 'DAYS_RANGE-value'})
        else:
            dRStatus = results.find('td', {'data-reactid': '117'})
        await ctx.send("Day Range: " + dRStatus.text.strip())
        await ctx.send("-------------------------")

        # 52 Week range
        if(results.find('td', {'data-test': 'FIFTY_TWO_WK_RANGE-value'})):
            wRStatus = results.find('td', {'data-test': 'FIFTY_TWO_WK_RANGE-value'})
        else:
            wRStatus = results.find('td', {'data-reactid': '121'})
        await ctx.send("Week Range: " + wRStatus.text.strip())
        await ctx.send("-------------------------")

        # Volume 
        if(results.find('td', {'data-test': 'TD_VOLUME-value'})):
            VStatus = results.find('td', {'data-test': 'TD_VOLUME-value'})
        else:
            VStatus = results.find('td', {'data-reactid': '125'})
        await ctx.send("Volume: " + VStatus.text.strip())
        await ctx.send("-------------------------")

    except:
        await ctx.send("Hmmm... Something wrong? :( ")

@CLIENT.command()
async def advinfo(ctx, arg1):
    try:
        await ctx.send("Loading stock data...")
        newURL = URL + arg1 +"?p=" + arg1

        driver.get(newURL)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find(id="quote-summary")

        # Bid Price of stock
        if(results.find('span', {'data-reactid': '108'})):
            bPrice = results.find('span', {'data-reactid': '108'})
        else:
            bPrice = results.find('span', {'data-reactid': '108'})
        if bPrice is not None:
            bPrice = bPrice.text.strip()
            await ctx.send("Bid Price: $" + str(bPrice.split(' x ')[0]))
            await ctx.send("-------------------------")
        else:
            await ctx.send("Bid Price: $0")
            await ctx.send("-------------------------")

        # Ask price    
        if(results.find('td', {'data-test': 'ASK-value'})):
            aStatus = results.find('td', {'data-test': 'ASK-value'})
        else:
            aStatus = results.find('td', {'data-reactid': '112'})
        await ctx.send("Ask: " + aStatus.text.strip())
        await ctx.send("-------------------------")

        # Market Cap
        if(results.find('td', {'data-test': 'MARKET_CAP-value'})):
            MCStatus = results.find('td', {'data-test': 'MARKET_CAP-value'})
        else:
            MCStatus = results.find('td', {'data-reactid': '138'})
        await ctx.send("Market Cap: " + MCStatus.text.strip())
        await ctx.send("-------------------------")

        # PE Ratio
        if(results.find('td', {'data-test': 'PE_RATIO-value'})):
            PEStatus = results.find('td', {'data-test': 'PE_RATIO-value'})
        else:
            PEStatus = results.find('td', {'data-reactid': '148'})
        await ctx.send("PE Ratio: " + PEStatus.text.strip())
        await ctx.send("-------------------------")

        # Dividend & yield
        if(results.find('td', {'data-test': 'DIVIDEND_AND_YIELD-value'})):
            DYStatus = results.find('td', {'data-test': 'DIVIDEND_AND_YIELD-value'})
        else:
            DYStatus = results.find('td', {'data-reactid': '163'})
        await ctx.send(" Ratio: " + DYStatus.text.strip())
        await ctx.send("-------------------------")
    except:
        await ctx.send("Hmmm... Something wrong? :( ")

# This method only runs once in the beginning
@CLIENT.event
async def on_ready():
    print("Discord Bot Activated")

# This is testing by Jong
# @CLIENT.command()
# async def jtesting(ctx):
#     print(ctx.author.id)
#     await ctx.send(ctx.author.id)
#
@CLIENT.command()
async def empty(ctx):
    mycursor.execute("DELETE from User")
    await ctx.send("IT'S EMPTY!")

@CLIENT.command()
async def create(ctx, name, amount):
    id = ctx.author.id / 1000000000
    try:
        newUser(id, name, amount)
    except:
        await ctx.send("Your account already exists")
    else:
        await ctx.send("You created account!")

@CLIENT.command()
async def buy(ctx, company, amount):
    id = ctx.author.id / 1000000000
    try:
        buy(id, company, amount, price(company))
    except:
        await ctx.send("Something went wrong")
    else:
        await ctx.send("You got it!")

def newUser(id, name, amount):
    try:
        task1 = "INSERT INTO User (userId, name, cash, net) VALUES (%s, %s, %s, %s)"
        val1 = (id, name, amount, amount)
        mycursor.execute(task1, val1)
    except:
        raise Exception


def buy(id, code, number, price):
    try:
        t1 = "UPDATE Wallet SET amount = amount + %s WHERE userId = %s company = %s"
        val1 = (number, id, code)
        mycursor.execute(t1, val1)
    except:
        t2 = "INSERT INTO Wallet (userId, company, amount) VALUES (%s, %s, %s)"
        val2 = (id, code, number)
        mycursor.execute(t2, val2)
    t3 = "INSERT INTO History (userId, company, bs, number, price) VALUES (%s, %s, %s, %s, %s)"
    val3 = (id, code, "B", number, price)
    mycursor.execute(t3, val3)
    t4 = "UPDATE User SET cash = cash - %s, net = net + %s WHERE userId = %s"
    val4 = (price, price, id)
    db.commit()

def sell(id, code, number, price):
    try:
        t1 = "UPDATE Wallet SET amount = amount - %s WHERE userId = %s company = %s"
        val1 = (number, id, code)
        mycursor.execute(t1, val1)
    except:
        print("Error, not enough money or don't have company")
    else:
        t3 = "INSERT INTO History (userId, company, bs, number, price) VALUES (%s, %s, %s, %s, %s)"
        val3 = (id, code, "S", number, price)
        mycursor.execute(t3, val3)
        t4 = "UPDATE User SET cash = cash + %s, net = net - %s WHERE userId = %s"
        val4 = (price, price, id)
    db.commit()

def checkWallet(id):
    t1 = "SELECT * FROM Wallet WHERE userId = %s"
    mycursor.execute(t1, id)
    wallet = mycursor.fetchall()
    for x in wallet:
        print(x)

def checkbalance(id):
    t1 = "SELECT cash, net FROM Wallet WHERE userId = %s"
    mycursor.execute(t1, id)
    balance = mycursor.fetchone()
    print(balance)

def price(arg1):
    newURL = URL + arg1 +"?p=" + arg1

    driver.get(newURL)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Get current price
    results = soup.find(id="Lead-3-QuoteHeader-Proxy")
    stock_elems = results.find("div", class_="D(ib) Mend(20px)")
    price = stock_elems.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
    cur_price_phrase = price.text.strip()
    return int(cur_price_phrase)

CLIENT.run(TOKEN)
