import flask
from blockchain import TOP_BLOCK
from utxo import txOut

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/json_rpc', methods=['GET'])
def home():
    return '{ "error" : "Please specify a route" }' 

@app.route('/json_rpc/topblock', methods=['GET'])
def topblock():
    return TOP_BLOCK.to_json()

@app.route('/json_rpc/utxo', methods=['GET'])
def utxo():
    txo = txOut()
    if 'hash' not in request.args:
        txo.hash = request.args['hash']
    else:
        return '{ "error": "No hash field provided. Please specify an txout hash" }'

    if txo.get(self.hash) == False:
        return '{ "error": "couldnt find txout with that hash" }'
    else:
        return tx.to_json()


app.run()