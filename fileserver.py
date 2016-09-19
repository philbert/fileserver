import os
import json
import random

from flask import Flask
from flask import request
from flask import send_from_directory

from two1.wallet import Wallet
from two1.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

# directory of the digital content we'd like to sell
dir_path = '/home/twenty/sellfiles'

# get a list of the files in the directory
file_list = os.listdir(dir_path)

# simple content model: dictionary of files w/ random prices
files = {}
for file_id in range(len(file_list)):
    files[file_id+1] = file_list[file_id], random.randrange(1000, 3000)


# endpoint to look up files to buy
@app.route('/files')
def file_lookup():
    return json.dumps(files)


# return the price of the selected file
def get_price_from_request(request):
    id = int(request.args.get('selection'))
    return files[id][1]


# machine-payable endpoint that returns selected file if payment made
@app.route('/buy')
@payment.required(get_price_from_request)
def buy_file():

    # extract selection from client request
    sel = int(request.args.get('selection'))

    # check if selection is valid
    if(sel < 1 or sel > len(file_list)):
        return 'Invalid selection.'
    else:
        return send_from_directory(dir_path, file_list[int(sel)-1])

if __name__ == '__main__':
    # app.debug = True
    app.run(host='::')
