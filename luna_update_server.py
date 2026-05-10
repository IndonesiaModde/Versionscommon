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

FILEINFO_URL = "https://versionscommon.onrender.com/assets/android/fileinfo"

# ================================
# 🔥 LOG SCANNER COMPLETO
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
# 🧠 5 MODOS DE RESPOSTA
# ================================
def build_response(mode, version):
    if mode == 1:
        return f"versioninfo\n{version}\nupdate=0"

    if mode == 2:
        return (
            f"versioninfo\n{version}\n"
            f"fileinfo={FILEINFO_URL}\n"
            f"update=1"
        )

    if mode == 3:
        return (
            f"versioninfo\n{version}\n"
            f"fileinfo={FILEINFO_URL}\n"
            f"size={APK_SIZE}\n"
            f"md5={APK_MD5}\n"
            "force=1"
        )

    if mode == 4:
        return (
            f"versioninfo\n{version}\n"
            "update=1\n"
            "maintenance=0\n"
            "message=update_available"
        )

    if mode == 5:
        return (
            f"versioninfo\n{version}\n"
            f"fileinfo={FILEINFO_URL}\n"
            "update=1\n"
            "download_retry=1\n"
            "safe_mode=1"
        )

    return f"versioninfo\n{version}\nupdate=0"


# ================================
# VER.PHP
# ================================
@app.route("/live/ver.php", methods=["GET"])
def ver():

    start = time.time()

    client_version = request.args.get("version", "0")

    print(">>> CLIENT VERSION:", client_version)

    # escolha automática do modo (debug simples)
    if client_version != LATEST_VERSION:
        print(">>> UPDATE NECESSÁRIO")
        mode = 3
    else:
        print(">>> CLIENT OK")
        mode = 1

    response_text = build_response(mode, LATEST_VERSION)

    print("\n>>> RESPONSE RAW:\n", response_text)
    print(">>> TIME:", round(time.time() - start, 4), "s")

    return Response(response_text, mimetype="text/plain")


# ================================
# FILEINFO
# ================================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    return Response(
        "gameassetbundles,example,12060,0",
        mimetype="text/plain"
    )


# ================================
# CATCH ALL (DEBUG ROUTER)
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
