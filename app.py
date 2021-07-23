import os
from flask import Flask, request, redirect, render_template  # necessário instalar o flask (pip install -U Flask)
from validaDados import findPattern # Importa a função findPattern que está dentro do arquivo validaDados.py
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resource={r"/*": {"origins": "*"}})


@app.route("/")
def home():
    return  redirect("https://tdn.totvs.com/pages/releaseview.action?pageId=497910397")


@app.route('/validaDados', methods=['GET'])
def retorno():
#     oJson = findPattern()
#     return oJson, 200
    return "<h1> Hellow World!!! </h1>"


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
#     app.run()
    main()
