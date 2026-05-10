from flask import Flask, request, Response
import time
import os

app = Flask(__name__)

# ================================
# CONFIG
# ================================
LATEST_VERSION = "1.17.2"

APK_URL = "https://raw.githubusercontent.com/IndonesiaModde/Versionscommon/master/Update.apk"
APK_SIZE = "307889833"
APK_MD5 = "471ebda5ff6f1af2eecc8d43a3a4fda2"

# ================================
# LOG SCANNER COMPLETO
# ================================
@app.before_request
def log_all():
    print("\n" + "=" * 60)
    print("📡 REQUEST SCANNER")

    print("METHOD:", request.method)
    print("PATH:", request.path)
    print("URL:", request.url)

    print("\nPARAMS:")
    for k, v in request.args.items():
        print(f"  {k}: {v}")

    print("\nHEADERS:")
    for k, v in request.headers.items():
        print(f"  {k}: {v}")

    print("IP:", request.remote_addr)
    print("=" * 60 + "\n")


# ================================
# RESPONSE BUILDER (CORRIGIDO)
# ================================
def build_response(version, client_version):
    if client_version == version:
        return f"versioninfo\n{version}\nupdate=0"

    # UPDATE MODE (FIXED)
    return (
        f"versioninfo\n{version}\n"
        f"fileinfo={APK_URL}\n"
        f"size={APK_SIZE}\n"
        f"md5={APK_MD5}\n"
        "force=1\n"
        "update=1\n"
        "mandatory=1"
    )


# ================================
# VER.PHP
# ================================
@app.route("/live/ver.php", methods=["GET"])
def ver():

    start = time.time()

    client_version = request.args.get("version", "0")

    print(">>> CLIENT VERSION:", client_version)

    response_text = build_response(LATEST_VERSION, client_version)

    print("\n>>> RESPONSE RAW:\n", response_text)
    print(">>> TIME:", round(time.time() - start, 4), "s")

    return Response(response_text, mimetype="text/plain")


# ================================
# FILEINFO (CORRIGIDO - NÃO MAIS FAKE)
# ================================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():

    print(">>> FILEINFO REQUEST")

    return Response(
        f"apk,{APK_URL},{APK_SIZE},{APK_MD5}",
        mimetype="text/plain"
    )


# ================================
# CATCH ALL
# ================================
@app.route("/<path:path>")
def catch(path):
    print(">>> UNKNOWN ROUTE:", path)
    return "OK", 200


# ================================
# START
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
