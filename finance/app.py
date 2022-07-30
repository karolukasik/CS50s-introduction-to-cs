import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    purchasedStocksRows = db.execute(
        "SELECT stock_symbol, SUM(stock_amount) AS stock_amount from purchases WHERE user_id=? GROUP BY stock_symbol", session["user_id"])
    purchaseList = []
    ordinal = 1
    totalStockCurrentValue = 0
    for row in purchasedStocksRows:
        purchaseData = {}
        response = lookup(row["stock_symbol"])
        purchaseData["ordinal"] = ordinal
        purchaseData["symbol"] = row["stock_symbol"]
        purchaseData["company"] = response.get("name")
        purchaseData["amount"] = row["stock_amount"]
        purchaseData["currentPrice"] = usd(response.get("price"))
        currentStockValue = int(
            row["stock_amount"]) * response.get("price")
        purchaseData["currentValue"] = usd(currentStockValue)
        totalStockCurrentValue += currentStockValue
        ordinal += 1
        purchaseList.append(purchaseData)

    cashBalanceDict = db.execute(
        "SELECT cash FROM users WHERE id=?", session["user_id"])
    cashBalance = cashBalanceDict[0]["cash"]
    totalBalance = totalStockCurrentValue+cashBalance
    cashBalanceUsd = usd(cashBalance)
    totalBalanceUsd = usd(totalBalance)

    return render_template("/index.html", purchaseList=purchaseList, cashBalance=cashBalanceUsd, totalBalance=totalBalanceUsd)


@ app.route("/buy", methods=["GET", "POST"])
@ login_required
def buy():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Must provide correct symbol", 400)
        if not request.form.get("shares"):
            return apology("Must provide the amount of stock to buy", 403)
        try:
            qty = int(request.form.get("shares"))
            if qty <= 0:
                return apology("quantity has to be positive integer", 400)
        except ValueError:
            return apology("quantity has to be positive integer", 400)

        symbol = request.form.get("symbol").upper()
        response = lookup(symbol)
        if response == None:
            return apology("Stock symbol not found", 400)

        stockUnitPrice = float(response.get("price"))
        quantity = int(request.form.get("shares"))
        totalPrice = stockUnitPrice * quantity
        userBalanceList = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        userBalanceFloat = userBalanceList[0].get("cash")
        if(totalPrice > userBalanceFloat):
            return apology("Not enough cash to buy", 418)
        db.execute("INSERT INTO purchases (user_id, stock_symbol, stock_amount, stock_unit_price) VALUES (?, ?, ?, ?)",
                   session["user_id"],
                   symbol,
                   quantity,
                   stockUnitPrice)
        db.execute("UPDATE users SET cash=? WHERE id=?",
                   userBalanceFloat-totalPrice, session["user_id"])
        return redirect("/")
    return render_template("/buy.html")


@ app.route("/history")
@ login_required
def history():
    rows = db.execute(
        "SELECT stock_symbol, stock_amount, stock_unit_price, timestamp FROM purchases WHERE user_id = ?", session["user_id"])
    purchaseList = []
    ordinal = 1
    for row in rows:
        purchaseDataSingleRow = {}

        purchaseDataSingleRow["ordinal"] = ordinal
        purchaseDataSingleRow["timestamp"] = row["timestamp"]

        stockAmountSigned = row["stock_amount"]
        if stockAmountSigned < 0:
            purchaseDataSingleRow["action"] = "Sold"
            purchaseDataSingleRow["amount"] = -stockAmountSigned
            totalValue = -stockAmountSigned * row["stock_unit_price"]
        else:
            purchaseDataSingleRow["action"] = "Bought"
            purchaseDataSingleRow["amount"] = stockAmountSigned
            totalValue = stockAmountSigned * row["stock_unit_price"]

        purchaseDataSingleRow["symbol"] = row["stock_symbol"]
        purchaseDataSingleRow["historicalPrice"] = usd(row["stock_unit_price"])
        purchaseDataSingleRow["totalValue"] = usd(totalValue)

        purchaseList.append(purchaseDataSingleRow)
        ordinal += 1

    return render_template("/history.html", purchaseList=purchaseList)


@ app.route("/changepassword", methods=["GET", "POST"])
@ login_required
def changepassword():
    if request.method == "POST":
        if not (request.form.get("old-password")):
            return apology("must provide old password", 403)
        if not (request.form.get("new-password-first")):
            return apology("must provide new password", 403)
        if not (request.form.get("new-password-repeat")):
            return apology("must repeat new password", 403)

        row = db.execute("SELECT hash FROM users WHERE id=?",
                         session["user_id"])
        if not check_password_hash(row[0]["hash"], request.form.get("old-password")):
            return apology("the old password was incorrect", 403)
        if not request.form.get("new-password-first") == request.form.get("new-password-repeat"):
            return apology("new passwords does not match", 403)
        if check_password_hash(row[0]["hash"], request.form.get("new-password-first")):
            return apology("the new password must be different than old password", 403)
        db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(
            request.form.get("new-password-first")), session["user_id"])
        return redirect("/")
    return render_template("/changepassword.html")


@ app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@ app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@ app.route("/quote", methods=["GET", "POST"])
@ login_required
def quote():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")
        symbol = request.form.get("symbol").upper()
        response = lookup(symbol)
        if response == None:
            return apology("stock symbol not found", 400)
        company = response.get("name")
        price = usd(response.get("price"))
        return render_template("/quoted.html", company=company, symbol=symbol, price=price)
    else:
        return render_template("/quote.html")


@ app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password twice", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("must provide the same password twice", 400)
        if len(db.execute("SELECT username FROM users WHERE username= ? ", request.form.get("username"))) == 1:
            return apology("username already exist", 400)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("confirmation")))
        return render_template("register-succesfull.html")
    else:
        return render_template("register.html")


@ app.route("/sell", methods=["GET", "POST"])
@ login_required
def sell():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 404)
        if not request.form.get("shares"):
            return apology("must provide quantity", 404)

        try:
            qty = int(request.form.get("shares"))
            if qty <= 0:
                return apology("quantity has to be positive integer", 400)
        except ValueError:
            return apology("quantity has to be positive integer", 400)
        symbol = request.form.get("symbol").upper()
        row = db.execute(
            "SELECT SUM(stock_amount) AS stock_amount FROM purchases WHERE user_id= ? AND stock_symbol=?", session["user_id"], symbol)
        if row == None:
            return apology("stock symbol invalid or you don't own stock", 404)
        stockAmount = row[0]["stock_amount"]

        if qty <= stockAmount:
            response = lookup(symbol)
            price = response.get("price")
            db.execute("INSERT INTO purchases (user_id, stock_symbol, stock_amount, stock_unit_price) VALUES (?, ?, ?, ?)",
                       session["user_id"],
                       symbol,
                       -qty,
                       usd(price))

            totalPrice = qty * price

            userBalanceList = db.execute(
                "SELECT cash FROM users WHERE id = ?", session["user_id"])
            userBalanceFloat = userBalanceList[0].get("cash")

            db.execute("UPDATE users SET cash=? WHERE id=?",
                       (userBalanceFloat+totalPrice), session["user_id"])
            return redirect("/")
        else:
            return apology("you don't have enough stock", 400)
    rows = db.execute(
        "SELECT stock_symbol FROM purchases WHERE user_id=? GROUP BY stock_symbol;", session["user_id"])
    symbolList = []
    for row in rows:
        symbolList.append(row["stock_symbol"])
    return render_template("sell.html", symbolList=symbolList)
