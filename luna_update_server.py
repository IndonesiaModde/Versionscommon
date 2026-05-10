from flask import Flask, request, Response, jsonify

app = Flask(__name__)

# ================================
# CONFIG REAL
# ================================
LATEST_VERSION = "1.17.2"

FILEINFO_URL = "https://versionscommon.onrender.com/assets/android/fileinfo"

APK_URL = "https://github.com/IndonesiaModde/Versionscommon/blob/master/Update.apk"  # ⚠️ TROCAR PELO LINK REAL
APK_SIZE = "307889833"
APK_MD5 = "471ebda5ff6f1af2eecc8d43a3a4fda2"

# ================================
# LOG UNIVERSAL
# ================================
@app.before_request
def log_request():
    print("\n==============================")
    print(">>> METHOD:", request.method)
    print(">>> PATH:", request.path)
    print(">>> PARAMS:", dict(request.args))
    print("==============================")

# ================================
# ROOT (ANTI HEALTHCHECK)
# ================================
@app.route("/", methods=["GET", "HEAD"])
def home():
    return "OK", 200

# ================================
# VER.PHP (LEGACY_7 FINAL)
# ================================
@app.route("/live/ver.php", methods=["GET"])
def ver():
    try:
        client_version = request.args.get("version", "0")

        print(">>> CLIENT VERSION:", client_version)

        if client_version != LATEST_VERSION:
            print(">>> UPDATE NECESSÁRIO")

            response_text = (
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
            print(">>> JÁ ATUALIZADO")

            response_text = (
                "versioninfo\n"
                f"{LATEST_VERSION}\n"
                "update=0"
            )

        print(">>> RESPONSE RAW:", repr(response_text))

        return Response(response_text, mimetype="text/plain")

    except Exception as e:
        print(">>> ERRO:", str(e))
        return "error", 500

# ================================
# FILEINFO (DOWNLOAD INFO)
# ================================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    print("\n>>> FILEINFO REQUEST RECEBIDA")

    return jsonify({
        "status": "ok",
        "version": LATEST_VERSION,
        "url": APK_URL,
        "size": APK_SIZE,
        "md5": APK_MD5,
        "force": True
    })

# ================================
# START SERVER
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
