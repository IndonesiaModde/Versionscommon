from flask import Flask, request, Response
import time
import os

app = Flask(__name__)

# ================================
# CONFIG PRINCIPAL
# ================================
LATEST_VERSION = "1.17.2"

APK_URL = "https://raw.githubusercontent.com/IndonesiaModde/Versionscommon/master/Update.apk"
APK_SIZE = "307889833"
APK_MD5 = "471ebda5ff6f1af2eecc8d43a3a4fda2"

FILEINFO_URL = "https://versionscommon.onrender.com/assets/android/fileinfo"


# ================================
# CLEANER (REMOVE LIXO DO METADATA)
# ================================
def clean(text):
    if not text:
        return "0"
    return str(text).replace("\x00", "").strip()


def clean_url(url):
    if not url:
        return ""

    url = url.replace("\x00", "")

    # corta lixo duplicado de URL
    if "https://" in url:
        url = url[url.find("https://"):]

    # evita concatenação de strings quebradas
    url = url.split("fileinfo")[0]
    url = url.split("versioninfo")[0]

    return url.strip()


# ================================
# 🔥 LOG SCANNER COMPLETO
# ================================
@app.before_request
def log_all():

    print("\n" + "=" * 70)
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
    print("=" * 70 + "\n")


# ================================
# VER.PHP (LEGACY FIXED)
# ================================
@app.route("/live/ver.php", methods=["GET"])
def ver():

    start = time.time()

    client_version = clean(request.args.get("version", "0"))

    print(">>> CLIENT VERSION:", client_version)

    if client_version != LATEST_VERSION:

        print(">>> UPDATE NECESSÁRIO")

        response_text = (
            "versioninfo\n"
            f"{LATEST_VERSION}\n"
            f"fileinfo={APK_URL}\n"
            f"size={APK_SIZE}\n"
            f"md5={APK_MD5}\n"
            "force=1\n"
            "update=1\n"
            "mandatory=1"
        )

    else:

        print(">>> CLIENT ATUALIZADO")

        response_text = (
            "versioninfo\n"
            f"{LATEST_VERSION}\n"
            "update=0"
        )

    print("\n>>> RESPONSE RAW:\n", response_text)
    print(">>> TIME:", round(time.time() - start, 4), "s")

    return Response(response_text, mimetype="text/plain")


# ================================
# FILEINFO (LIMPO)
# ================================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():

    print(">>> FILEINFO REQUEST")

    return Response(
        "gameassetbundles,clean,12060,0\nmain,ok,2000,0",
        mimetype="text/plain"
    )


# ================================
# DEBUG CATCH-ALL
# ================================
@app.route("/<path:path>", methods=["GET", "POST"])
def catch(path):

    print(">>> UNKNOWN ROUTE:", path)

    return "OK", 200


# ================================
# START SERVER
# ================================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    print("🚀 SERVER STARTED ON PORT:", port)

    app.run(host="0.0.0.0", port=port)
