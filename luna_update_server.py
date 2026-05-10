from flask import Flask, request, Response
import time
import os
import json

app = Flask(__name__)

# ================================
# CONFIG
# ================================
LATEST_VERSION = "1.17.1"

FILEINFO_URL = "https://versionscommon.onrender.com/assets/android/fileinfo"

APK_SIZE = "307889833"
APK_MD5 = "471ebda5ff6f1af2eecc8d43a3a4fda2"

FILE_INFO_RAW = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0"""

# ================================
# 🔥 FULL LOG SCANNER (GLOBAL)
# ================================
@app.before_request
def log_all_requests():
    start = time.time()
    request.start_time = start

    print("\n" + "=" * 70)
    print("📡 REQUEST CAPTURED")

    print("METHOD:", request.method)
    print("PATH:", request.path)
    print("URL:", request.url)
    print("IP:", request.remote_addr)

    print("\nQUERY PARAMS:")
    print(dict(request.args))

    print("\nHEADERS:")
    for k, v in request.headers.items():
        print(f"{k}: {v}")

    if request.data:
        print("\nBODY:")
        print(request.data.decode(errors="ignore"))

    print("=" * 70 + "\n")

# ================================
# ROOT
# ================================
@app.route("/", methods=["GET", "HEAD"])
def home():
    return "OK", 200

# ================================
# VERSION CHECK (/live/ver.php)
# ================================
@app.route("/live/ver.php", methods=["GET"])
def ver():
    start = time.time()

    client_version = request.args.get("version", "0")

    print(">>> CLIENT VERSION:", client_version)

    if client_version != LATEST_VERSION:
        print(">>> UPDATE NECESSÁRIO")

        response = (
            "versioninfo\n"
            f"{LATEST_VERSION}\n"
            f"fileinfo={FILEINFO_URL}\n"
            f"size={APK_SIZE}\n"
            f"md5={APK_MD5}\n"
            "force=1\n"
            "update=1\n"
            "mandatory=1"
        )
    else:
        print(">>> CLIENT ATUALIZADO")

        response = (
            "versioninfo\n"
            f"{LATEST_VERSION}\n"
            "update=0"
        )

    elapsed = round(time.time() - start, 4)

    print("\n>>> RESPONSE RAW:\n", response)
    print(">>> RESPONSE TIME:", elapsed, "s")

    return Response(response, mimetype="text/plain")

# ================================
# FILEINFO
# ================================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    print(">>> FILEINFO REQUEST")
    return Response(FILE_INFO_RAW, mimetype="text/plain")

# ================================
# CATCH-ALL (DEBUG TOTAL DE ROTAS)
# ================================
@app.route("/<path:path>", methods=["GET", "POST", "HEAD"])
def catch_all(path):
    print("\n>>> UNKNOWN ROUTE HIT:", path)

    return Response(
        f"unknown route: {path}",
        mimetype="text/plain",
        status=404
    )

# ================================
# ERROR HANDLER GLOBAL
# ================================
@app.errorhandler(Exception)
def error_handler(e):
    print(">>> ERROR:", str(e))
    return Response("internal error", status=500)

# ================================
# START SERVER
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
