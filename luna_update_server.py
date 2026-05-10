from flask import Flask, request, Response, send_file
import os

app = Flask(__name__)

BASE_DIR = "assets/android/gameassetbundles"

VERSION = "1.17.1"

FILEINFO = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

# 🔍 LOGGER GLOBAL
@app.before_request
def log_request():
    print("\n==============================")
    print(f">>> METHOD: {request.method}")
    print(f">>> PATH: {request.path}")
    print(f">>> FULL URL: {request.url}")

    print(">>> QUERY PARAMS:")
    for k, v in request.args.items():
        print(f"   {k} = {v}")

    print(">>> HEADERS:")
    for k, v in request.headers.items():
        print(f"   {k}: {v}")

    print("==============================\n")


# 🔹 VERSION ENDPOINT
@app.route("/live/ver.php")
def version():
    print(">>> RESPONDENDO VERSIONINFO")

    response_text = f"""versioninfo
{VERSION}

fileinfo
{FILEINFO}
"""

    return Response(
        response_text,
        status=200,
        mimetype="text/plain; charset=utf-8"
    )


# 🔹 ASSETS
@app.route("/assets/android/gameassetbundles/<path:filepath>")
def serve_asset(filepath):
    full_path = os.path.join(BASE_DIR, filepath)

    print(f">>> ASSET REQUEST: {filepath}")
    print(f">>> FULL PATH: {full_path}")

    if not os.path.exists(full_path):
        print(">>> ERRO: ARQUIVO NÃO EXISTE ❌")
        return "Not Found", 404

    size = os.path.getsize(full_path)
    print(f">>> TAMANHO REAL: {size} bytes")

    return send_file(full_path, as_attachment=False)


# 🔹 CAPTURA QUALQUER COISA QUE NÃO EXISTE
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    print(f">>> ENDPOINT DESCONHECIDO: /{path}")
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
