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
# VERSION CHECK (LEGACY_7 REAL)
# ==============================
@app.route("/live/ver.php", methods=["GET"])
def version_check():
    try:
        client_version = request.args.get("version", "")

        print(">>> CLIENT VERSION:", client_version)

        if client_version != CURRENT_VERSION:
            print(">>> UPDATE NECESSÁRIO")

            response_text = f"""versioninfo
{CURRENT_VERSION}
fileinfo={BASE_URL}/assets/android/fileinfo
size=12345678
md5=d41d8cd98f00b204e9800998ecf8427e"""
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
            "ret": 0,
            "msg": "ok",
            "version": CURRENT_VERSION,
            "force": True,
            "download_url": f"{BASE_URL}/update.apk",
            "url": f"{BASE_URL}/update.apk",
            "file_size": 12345678,
            "size": 12345678
        })

    except Exception as e:
        print(">>> ERRO FILEINFO:", str(e))
        return jsonify({"ret": -1}), 500

# ==============================
# APK DOWNLOAD
# ==============================
@app.route("/update.apk", methods=["GET"])
def download_apk():
    try:
        print(">>> DOWNLOAD APK")
        return Response("APK_PLACEHOLDER", mimetype="application/octet-stream")

    except Exception as e:
        print(">>> ERRO APK:", str(e))
        return Response("error", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
