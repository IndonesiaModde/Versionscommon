from flask import Flask, request, Response
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

# modos focados em formatos LEGACY (sem JSON)
test_mode = 0

MODES = [
    ("LEGACY_1", lambda: f"{VERSION}"),
    
    ("LEGACY_2", lambda: f"{VERSION}\n"),
    
    ("LEGACY_3", lambda: f"""versioninfo
{VERSION}"""),
    
    ("LEGACY_4", lambda: f"""versioninfo
{VERSION}
fileinfo=/fileinfo"""),
    
    ("LEGACY_5", lambda: f"""version={VERSION}
fileinfo=/fileinfo"""),
    
    ("LEGACY_6", lambda: f"""versioninfo={VERSION}
fileinfo=/fileinfo"""),
    
    ("LEGACY_7", lambda: f"""versioninfo
{VERSION}
fileinfo=/assets/android/fileinfo"""),
    
    ("LEGACY_8", lambda: f"""version={VERSION}
fileinfo=/assets/android/fileinfo"""),
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

    response_text = func()

    print(f">>> TESTANDO MODO: {mode_name}")
    print(">>> RESPOSTA:")
    print(response_text)

    test_mode = (test_mode + 1) % len(MODES)

    return Response(response_text, mimetype="text/plain")


@app.route("/fileinfo", methods=["GET"])
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    log_request()
    print(">>> 📦 ENVIANDO FILEINFO")

    return Response(FILEINFO, mimetype="text/plain")


@app.route("/assets/<path:subpath>", methods=["GET"])
def assets(subpath):
    log_request()
    print(f">>> 📁 REQUEST ASSET: {subpath}")

    # ainda mock (sem arquivos reais)
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
