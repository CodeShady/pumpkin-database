
![title-image](https://i.imgur.com/lQ3xHv6.png)

# What is Pumpkin?
Pumpkin or Pumpkin DB, is an extremely lightweight database manager written in **Python3** made for **Python3**.

Ever since I first started programming, I wanted to make my own Twitter-like app. But I couldn't. I didn't know enough to create anything like that. And I had no idea how to do any type of database stuff. So, for all those beginner programmers, try PumpkinDB. It's easy to use, fast, and I've even written my own tutorial on how to make a console Twitter app in Python3. [Which you can find here](https://www.codeshady.com/how-to-make-a-twitter-app-with-python-pumpkindb/).

## Donations
I hope PumpkinDB will make your Python experience sweet. Donations are seriously appreciated.

**Bitcoin Donations (BTC):** bc1qfpz9q09xmvsk206p0ts6nul88hrxzzkfr4p0rr

## Requirements
Pumpkin requires **Python3**. (Python2 will just not work).

Pumpkin uses encryption, so it needs the package **PyCrypto**, which can be imported as shown.
```shell
pip3 install pycrypto
```

## Installation

Pumpkin is designed to be the easiest database you are going to ever set up.

```shell
git clone https://github.com/CodeShady/pumpkin-database.git
```

## Get Started

```python
# Import Pumpkin Database
from pumpkindb import *

pumpkin = PumpkinDB()

# Set an encryption key so others cannot see your database
password = "123456"

# Create a new database with the encryption key
pumpkin.create("notes", password)

# Use that new database
pumpkin.use("notes", password)

# Ask user for notes
while True:
	notes = input("What Are You Thinking About? ")

	# If user enters quit, then quit the program
	if notes == "quit":
		# First delete all past notes
		pumpkin.delete("notes")
		# Now break the loop
		break

	# If the user didn't quit, then add the note to the database
	else:
		# Add the data to the "notes" table
		pumpkin.add("notes", notes)

		# Fetch all notes from the database
		allNotes = pumpkin.fetch("notes", "value")
		
		# Iterate through all notes and print them to the user
		for note in allNotes:
			print("Note: " + note)

```

## Usage

There isn't much you need to know about PumpkinDB to get started! It's all very simple and self explanatory.

**First Import PumpkinDB**

We need to import PumpkinDB and create a new pumpkin instance in order to use it!
```python
>>> from pumpkindb import *
>>> pumpkin = PumpkinDB()
```

**Create Pumpkin**(Database)

To start using PumpkinDB, you must first create a database.
```python
# pumpkin.create("DB-NAME", "PASSWORD")

>>> pumpkin.create("notes", "password123")
```

**Use Pumpkin**

Then you need tell PumpkinDB which **Pumpkin**(database) to use. 
```python
# pumpkin.use("DB-NAME", "PASSWORD")

>>> pumpkin.use("notes", "password123") 
```

**Add To Pumpkin**

Adding to a database is simple. Data is stored inside a **Pumpkin**. A Pumpkin holds rows of data.
```python
# pumpkin.add("ROW-NAME", value)

# Example 1
>>> pumpkin.add("notes", "Hello, World!")

# Example 2
>>> greeting = "What's up?"
>>> pumpkin.add("greetings", greeting)
```

**Data From Pumpkin**

**pumpkin.fetch()** returns a list. This is pretty sweet because lists are usually easy to handle! Make sure to declare the **return type**, you can ether use "key", "value", "timestamp", "hash", or "*". All these are pretty easy to understand, if you're confused about the return type, then try a simple code snippet and you will understand this.
```python
# pumpkin.fetch("ROW-NAME", "RETURN-TYPE")

# Example 1
>>> pumpkin.fetch("names", "value")
["John", "Robert", "Jane", "Bob"]

>>> pumpkin.fetch("names", "timestamp")
['1574441508.7555654', '1574441514.1020808', '1574441519.7773669']

>>> pumpkin.fetch("names", "hash")
['2c708e2b57c4985...', '55222814c26b4dd...', '4e6fb950b5c05a21a3...']

# Example 2
>>> allNames = pumpkin.fetch("names", "value")
>>> for name in allNames:
>>>		print(name)
John
Robert
Jane
Bob
```

**Fetching All Data**
If you want to fetch **all** data from your Pumpkin, then use: 
```python
>>> pumpkin.fetchall("*")
[
	['names', 'Smith', '1572544716.304211', '16de64826267617659286cc544a4a49ac8825a5965879e20c684591e678317bc'],
	['names', 'Robert', '1572544716.304939', '7dc3cca60cee3e0d9b0e1155a39d7d78ff1748fb85c9bc3525cc192cd62c82b1']
]
```
The ```.fetchall("*")``` function will return a list of data that can be easily parsed and used in your project.

If you want to control what you get in return, then try these options:
```python
# Fetch only the Key names from the data
>>> pumpkin.fetchall("key")
["names", "data", "other-data"]
```

```python
# Fetch only the values of the data
>>> pumpkin.fetchall("value")
["John Smith", "My 1st Data", "My 2nd Data"]
```
```python
# Fetch only the timestamps from the data
>>> pumpkin.fetchall("timestamp")
['1572544716.304211', '1572544716.304939']
```
```python
# Fetch only the sha256 hashes from the data
>>> pumpkin.fetchall("hash")
['16de6482626761765923id9e20efim92de...', '7dc3cca60cee3e0d9b0e149ac88678317bc...']
```

**Deleting A Row**


Deleting rows could never be easier! Just specify the row name you want to delete, and **Poof!*.. Gone!
```python
# pumpkin.delete("ROW-NAME")

# Example 1
>>> pumpkin.delete("junk")

# Example 2
>>> deleteThisRow = "junk"
>>> pumpkin.delete(deleteThisRow)
```

You can also delete a row by the sha256 hash associated with the row. If PumpkinDB detects that you enterd a string that is 64 characters long, it deletes the row by hash instead of key.
```python
# pumpkin.delete("ROW-HASH")

# Example 1
>>> pumpkin.delete("d18a27f466f659d2d010566...")

# Example 2
>>> deleteThisRow = "d18a27f466f659d2d010566..."
>>> pumpkin.delete(deleteThisRow)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
