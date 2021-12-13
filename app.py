#!/usr/bin/env python3

from flask import Flask
from flask import request, escape, render_template

import brawl

app = Flask(__name__)

SUCCESS = 200

@app.route("/")
def index():
	player_id = str(escape(request.args.get('player_id', '')))

	val = ''
	if player_id:
		val = brawl.process_request(player_id)
		if val[1] == SUCCESS:
			val = val[0][1] + val[0][0].__html__()
		else:
			val = val[0]
	else:
		brawl.process_request('')

	return render_template('index.html') + val

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


