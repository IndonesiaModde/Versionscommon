from flask import Flask, request, Response, jsonify

app = Flask(__name__)

CURRENT_VERSION = "1.17.2"
BASE_URL = "https://versionscommon.onrender.com"

# ==============================
# LOG GLOBAL
# ==============================
@app.before_request
def log_request():
    print("\n==============================")
    print(">>> METHOD:", request.method)
    print(">>> PATH:", request.path)
    print(">>> PARAMS:", dict(request.args))
    print("==============================")

# ==============================
# ROOT (Render não reclamar)
# ==============================
@app.route("/", methods=["GET", "HEAD"])
def home():
    return "OK", 200

# ==============================
# VERSION CHECK (LEGACY_7 FIXO)
# ==============================
@app.route("/live/ver.php", methods=["GET"])
def version_check():
    try:
        client_version = request.args.get("version", "")

        print(">>> CLIENT VERSION:", client_version)

        if client_version != CURRENT_VERSION:
            print(">>> UPDATE NECESSÁRIO")

            # 🔥 TESTA RELATIVO (mais compatível)
            response_text = f"""versioninfo
{CURRENT_VERSION}
fileinfo=/assets/android/fileinfo"""
        else:
            print(">>> CLIENTE ATUALIZADO")

            response_text = f"""versioninfo
{CURRENT_VERSION}"""

        print(">>> RESPONSE RAW:", repr(response_text))

        return Response(
            response_text,
            status=200,
            mimetype="text/plain",
            headers={
                "Connection": "keep-alive"
            }
        )

    except Exception as e:
        print(">>> ERRO:", str(e))
        return Response("error", status=500)

# ==============================
# FILEINFO (FORMATO FORTE)
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
        }), 200, {
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }

    except Exception as e:
        print(">>> ERRO FILEINFO:", str(e))
        return jsonify({"ret": -1}), 500

# ==============================
# APK DOWNLOAD (SIMULAÇÃO)
# ==============================
@app.route("/update.apk", methods=["GET"])
def download_apk():
    try:
        print(">>> DOWNLOAD APK")

        # ⚠️ aqui você pode depois colocar o APK real
        return Response(
            "APK_PLACEHOLDER",
            mimetype="application/octet-stream",
            headers={
                "Content-Disposition": "attachment; filename=update.apk"
            }
        )

    except Exception as e:
        print(">>> ERRO APK:", str(e))
        return Response("error", status=500)

# ==============================
# START
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
