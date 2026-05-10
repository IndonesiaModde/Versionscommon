from flask import Flask, request, Response, jsonify

app = Flask(__name__)

CURRENT_VERSION = "1.17.2"
BASE_URL = "https://versionscommon.onrender.com"

@app.before_request
def log_request():
    print("\n==============================")
    print(">>> METHOD:", request.method)
    print(">>> PATH:", request.path)
    print(">>> PARAMS:", dict(request.args))
    print("==============================")

@app.route("/", methods=["GET", "HEAD"])
def home():
    return "OK", 200

# ==============================
# VERSION CHECK
# ==============================
@app.route("/live/ver.php", methods=["GET"])
def version_check():
    try:
        client_version = request.args.get("version", "")

        print(">>> CLIENT VERSION:", client_version)

        # só manda update se for menor
        if client_version != CURRENT_VERSION:
            print(">>> UPDATE NECESSÁRIO")

            response_text = f"""versioninfo
{CURRENT_VERSION}
fileinfo={BASE_URL}/assets/android/fileinfo"""
        else:
            print(">>> CLIENTE ATUALIZADO")

            response_text = f"""versioninfo
{CURRENT_VERSION}"""

        print(">>> RESPONSE RAW:", repr(response_text))

        return Response(response_text, mimetype="text/plain")

    except Exception as e:
        print(">>> ERRO:", str(e))
        return Response("error", status=500)

# ==============================
# FILEINFO
# ==============================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    try:
        print(">>> FILEINFO REQUEST RECEBIDA")

        return jsonify({
            "status": "ok",
            "version": CURRENT_VERSION,
            "url": f"{BASE_URL}/update.apk",
            "size": "12345678",
            "force": True
        })

    except Exception as e:
        print(">>> ERRO FILEINFO:", str(e))
        return jsonify({"error": "internal"}), 500

# ==============================
# APK DOWNLOAD (IMPORTANTE)
# ==============================
@app.route("/update.apk", methods=["GET"])
def download_apk():
    try:
        print(">>> DOWNLOAD APK")

        return Response("APK AQUI", mimetype="application/octet-stream")

    except Exception as e:
        print(">>> ERRO APK:", str(e))
        return Response("error", status=500)

# ==============================
# START
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
