import mysql.connector

db = mysql.connector.connect(
    host="35.224.238.245",
    user="root",
    passwd="root",
    database="data"
)

mycursor = db.cursor()

# mycursor.execute("DROP TABLE User")
# mycursor.execute("DROP TABLE Wallet")
# mycursor.execute("DROP TABLE History")

# Creating User Table
# mycursor.execute("CREATE TABLE User("
#                  "userId int,"
#                  "name VARCHAR(50),"
#                  "cash int DEFAULT 0,"
#                  "net int DEFAULT 0)")

# Creating Wallet Table
# mycursor.execute("CREATE TABLE Wallet("
#                  "userId int,"
#                  "company VARCHAR(50),"
#                  "amount int UNSIGNED)")

# Creating History Table
# mycursor.execute("CREATE TABLE History("
#                  "userId int,"
#                  "company VARCHAR(50),"
#                  "bs ENUM('B', 'S') NOT NULL,"
#                  "number int DEFAULT 0,"
#                  "price int DEFAULT 0)")

def newUser(id, name, amount):
    task1 = "INSERT INTO User (userId, name, cash, net) VALUES (%s, %s, %s, %s)"
    val1 = (id, name, amount, amount)
    mycursor.execute(task1, val1)
    task2 = "INSERT INTO Wallet (userId) VALUES (%s)"
    val2 = id
    mycursor.execute(task2, val2)

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


# mycursor.execute("DESCRIBE User")
# for x in mycursor:
#     print(x)
# print("")
# mycursor.execute("DESCRIBE Wallet")
# for x in mycursor:
#     print(x)
# print("")
# mycursor.execute("DESCRIBE History")
# for x in mycursor:
#     print(x)
# print("")
db.close()



