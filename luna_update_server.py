from flask import Flask, request, Response, send_file
import os

app = Flask(__name__)

BASE_DIR = "assets/android/gameassetbundles"
VERSION = "1.17.2"

FILEINFO = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

# 🔁 formatos diferentes pra testar automaticamente
VERSION_FORMATS = [
    ("PLAIN", lambda v: v),
    ("NEWLINE", lambda v: v + "\n"),
    ("KEY_VALUE", lambda v: f"version={v}"),
    ("VERSIONINFO_BLOCK", lambda v: f"versioninfo\n{v}"),
    ("VERSIONINFO_EQUAL", lambda v: f"versioninfo={v}"),
    ("JSON_SIMPLE", lambda v: f'{{"version":"{v}"}}'),
    ("JSON_VERSIONINFO", lambda v: f'{{"versioninfo":"{v}"}}'),
    ("STATUS_STYLE", lambda v: f"status=ok&version={v}"),
]

request_count = 0

# ==============================
# 🔍 LOG
# ==============================
@app.before_request
def log_request():
    print("\n==============================")
    print(f">>> METHOD: {request.method}")
    print(f">>> PATH: {request.path}")
    print(f">>> URL: {request.url}")

    if request.args:
        print(">>> PARAMS:")
        for k, v in request.args.items():
            print(f"   {k} = {v}")

    print("==============================\n")


# ==============================
# 🔹 VERSION AUTO TEST
# ==============================
@app.route("/live/ver.php")
def version():
    global request_count

    format_name, formatter = VERSION_FORMATS[request_count % len(VERSION_FORMATS)]
    request_count += 1

    response_text = formatter(VERSION)

    print(f">>> TESTANDO FORMATO: {format_name}")
    print(f">>> RESPOSTA: {repr(response_text)}")

    return Response(
        response_text,
        status=200,
        mimetype="text/plain"
    )


# ==============================
# 🔹 FILEINFO (várias rotas)
# ==============================
@app.route("/live/fileinfo")
@app.route("/live/fileinfo.php")
@app.route("/fileinfo")
@app.route("/fileinfo.php")
@app.route("/assets/android/fileinfo")
def fileinfo():
    print(">>> 🔥 FILEINFO REQUISITADO 🔥")

    return Response(FILEINFO, mimetype="text/plain")


# ==============================
# 🔹 ASSETS
# ==============================
@app.route("/assets/android/gameassetbundles/<path:filepath>")
def serve_asset(filepath):
    full_path = os.path.join(BASE_DIR, filepath)

    print(f">>> ASSET: {filepath}")

    if not os.path.exists(full_path):
        print(">>> ERRO: NÃO EXISTE ❌")
        return "Not Found", 404

    size = os.path.getsize(full_path)
    print(f">>> TAMANHO: {size} bytes")

    return send_file(full_path, as_attachment=False)


# ==============================
# 🔹 CATCH ALL
# ==============================
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    print(f">>> ROTA DESCONHECIDA: /{path}")
    return "OK", 200


# ==============================
# 🚀 START
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
