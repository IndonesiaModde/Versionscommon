from flask import Flask, request, Response, jsonify

app = Flask(__name__)

# ==============================
# CONFIG
# ==============================
CURRENT_VERSION = "1.17.0"
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
# ROOT (evita erro no Render)
# ==============================
@app.route("/", methods=["GET", "HEAD"])
def home():
    return "OK", 200

# ==============================
# VERSION CHECK (LEGACY_7)
# ==============================
@app.route("/live/ver.php", methods=["GET"])
def version_check():
    try:
        client_version = request.args.get("version", "")

        print(">>> USANDO MODO FINAL: LEGACY_7")

        # resposta padrão (sempre manda update)
        response_text = f"""versioninfo
{CURRENT_VERSION}
fileinfo={BASE_URL}/assets/android/fileinfo"""

        print(">>> RESPONSE RAW:", repr(response_text))

        return Response(response_text, mimetype="text/plain")

    except Exception as e:
        print(">>> ERRO:", str(e))
        return Response("error", status=500)

# ==============================
# FILEINFO (JSON)
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
# START
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
