from flask import Flask, request, jsonify, Response
import os

app = Flask(__name__)

VERSION = "1.17.2"

FILEINFO = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

# controle de testes automáticos
test_mode = 0

MODES = [
    ("PLAIN", lambda: VERSION),
    ("PLAIN_NEWLINE", lambda: VERSION + "\n"),
    ("JSON_BASIC", lambda: jsonify({"version": VERSION})),
    ("JSON_STATUS", lambda: jsonify({"status": "ok", "version": VERSION})),
    ("JSON_FULL", lambda: jsonify({
        "status": "ok",
        "version": VERSION,
        "fileinfo": "/fileinfo",
        "assets": "/assets/android/"
    })),
    ("RAW_BLOCK", lambda: f"versioninfo\n{VERSION}")
]


def log_request():
    print("\n==============================")
    print(f">>> METHOD: {request.method}")
    print(f">>> PATH: {request.path}")
    print(f">>> URL: {request.url}")
    print(">>> PARAMS:")
    for k, v in request.args.items():
        print(f"   {k} = {v}")
    print("==============================")


@app.route("/live/ver.php", methods=["GET"])
def version():
    global test_mode
    log_request()

    mode_name, func = MODES[test_mode]

    print(f">>> TESTANDO MODO: {mode_name}")

    response = func()

    print(f">>> RESPOSTA: {response}")

    test_mode = (test_mode + 1) % len(MODES)

    return response


@app.route("/fileinfo", methods=["GET"])
def fileinfo():
    log_request()
    print(">>> ENVIANDO FILEINFO")

    return Response(FILEINFO, mimetype="text/plain")


@app.route("/assets/<path:subpath>", methods=["GET"])
def assets(subpath):
    log_request()
    print(f">>> REQUEST ASSET: {subpath}")

    # Simulação (você ainda não colocou arquivos reais)
    return Response("OK", mimetype="text/plain")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def fallback(path):
    log_request()
    print(f">>> ❓ ROTA DESCONHECIDA: {path}")
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
