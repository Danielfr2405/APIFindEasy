from flask import Flask, request, redirect, render_template  # necessário instalar o flask (pip install -U Flask)
from validaDados import findPattern # Importa a função findPattern que está dentro do arquivo validaDados.py

app = Flask(__name__)


@app.route("/")
def home():
    return  redirect("https://tdn.totvs.com/pages/releaseview.action?pageId=497910397")


@app.route('/validaDados', methods=['GET'])
def retorno():
    oJson = findPattern()
    return oJson, 200


if __name__ == '__main__':
    app.run()
