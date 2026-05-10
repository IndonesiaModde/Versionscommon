from flask import Flask, request, Response, send_file
import os
import json

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

# 🔥 JSONs diferentes pra testar
JSON_FORMATS = [
    ("JSON_BASIC", lambda v: {
        "version": v
    }),

    ("JSON_STATUS", lambda v: {
        "status": "ok",
        "version": v
    }),

    ("JSON_WITH_FILEINFO", lambda v: {
        "status": "ok",
        "version": v,
        "fileinfo": "/assets/android/fileinfo"
    }),

    ("JSON_CAMELCASE", lambda v: {
        "status": "ok",
        "version": v,
        "fileInfo": "/assets/android/fileinfo"
    }),

    ("JSON_FULL", lambda v: {
        "status": "ok",
        "version": v,
        "versioninfo": v,
        "fileinfo": "/assets/android/fileinfo",
        "cdn": "/assets/android/gameassetbundles/"
    }),

    ("JSON_MULTI_KEYS", lambda v: {
        "status": "ok",
        "version": v,
        "versioninfo": v,
        "fileinfo": "/assets/android/fileinfo",
        "fileInfo": "/assets/android/fileinfo",
        "assets": "/assets/android/gameassetbundles/",
        "resUrl": "/assets/android/gameassetbundles/"
    }),

    ("JSON_NESTED", lambda v: {
        "status": "ok",
        "data": {
            "version": v,
            "fileinfo": "/assets/android/fileinfo"
        }
    }),
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
# 🔹 VERSION AUTO TEST (JSON)
# ==============================
@app.route("/live/ver.php")
def version():
    global request_count

    format_name, formatter = JSON_FORMATS[request_count % len(JSON_FORMATS)]
    request_count += 1

    data = formatter(VERSION)
    response_text = json.dumps(data)

    print(f">>> TESTANDO JSON: {format_name}")
    print(f">>> RESPOSTA: {response_text}")

    return Response(
        response_text,
        status=200,
        mimetype="application/json"
    )


# ==============================
# 🔹 FILEINFO
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

    print(f">>> ASSET REQUEST: {filepath}")

    if not os.path.exists(full_path):
        print(">>> ❌ NÃO EXISTE")
        return "Not Found", 404

    return send_file(full_path)


# ==============================
# 🔹 CATCH ALL
# ==============================
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    print(f">>> ❓ ROTA DESCONHECIDA: /{path}")
    return "OK", 200


# ==============================
# 🚀 START
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
