test.pyimport time
import requests
from stellar_base.keypair import Keypair
from stellar_base.address import Address
from stellar_base.builder import Builder

from flask import Flask, render_template, redirect

app = Flask(__name__)

kp1 = Keypair.random()			# Generating the random values of seed and public key
kp2 = Keypair.random()
send_publickey = kp1.address().decode()		# Separating the public key
send_seed = kp1.seed().decode()				# Separating the seed
receive_publickey = kp2.address().decode()
receive_seed = kp2.seed().decode()

url = 'https://friendbot.stellar.org'
req1 = requests.get(url, params={'addr': send_publickey})		# Requesting the amount for the particula public key.
req2 = requests.get(url, params={'addr': receive_publickey})
address1 = Address(address = send_publickey)
address2 = Address(address = receive_publickey)


@app.route("/")
def home():
	return render_template("home.html")


@app.route("/account/")
def generate_account():		# Generates two new users along with their seed and public key.
	time.sleep(4)			# Displays the result after 4 sec.
	address = {
		'send_seed': send_seed,							# Sender's private key.
		'receive_publickey': receive_publickey,			# Receiver's public key.
	}
	return render_template("account.html", address=address)


@app.route("/balance/")
def initial_balance():		# Generates the initial balance for both users.

	address1.get()			# Receiving the balance info in JSON format.
	address2.get()
	for a1 in address1.balances:
		send_initial = a1['balance']		# Retrieving the eaxct balance info fron JSON.
	for a2 in address2.balances:
		receive_initial = a2['balance']

	ibalance = {							# Initial balance.
		'send_initial': send_initial,
		'receive_initial': receive_initial,
	}
	return render_template("account.html", ibalance=ibalance)


@app.route("/transfer/")
def transaction():			# Performs the transaction from one to another thus providing the current balance.
	builder = Builder(secret=send_seed)
	builder.append_payment_op(receive_publickey, '500', 'XLM')		# Assigning of Receiver address, amount & Asset.
	builder.add_text_memo('testing')								# Assigning of a memo or remark.
	builder.sign()
	s = builder.submit()					# Submitting the result of the transaction.
	address1.get()							# Receiving balance info in JSON format
	address2.get()
	for a1 in address1.balances:
		send_current = a1['balance']		# Retrieving the eaxct balance info fron JSON.
	for a2 in address2.balances:
		receive_current = a2['balance']	

	cbalance = {							# Current balance.
		'send_current': send_current,
		'receive_current': receive_current,
	}
	return render_template("transaction.html", cbalance=cbalance)


if __name__ == '__main__':
	app.run(debug=True)
