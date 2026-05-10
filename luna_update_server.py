from flask import Flask, request, Response, jsonify
import time

app = Flask(__name__)

# ================================
# CONFIG
# ================================
LATEST_VERSION = "1.17.2"
FILEINFO_URL = "https://versionscommon.onrender.com/assets/android/fileinfo"

APK_URL = "https://seuservidor.com/ff.apk"
APK_SIZE = "307889833"
APK_MD5 = "471ebda5ff6f1af2eecc8d43a3a4fda2"

# ================================
# 🔥 ALL LOG SCANNER
# ================================
@app.before_request
def full_request_log():
    print("\n" + "=" * 60)
    print("📡 INCOMING REQUEST CAPTURED")

    print("\n>>> METHOD:", request.method)
    print(">>> PATH:", request.path)
    print(">>> FULL URL:", request.url)

    print("\n>>> QUERY PARAMS:")
    for k, v in request.args.items():
        print(f"   {k} = {v}")

    print("\n>>> HEADERS:")
    for k, v in request.headers.items():
        print(f"   {k}: {v}")

    print("\n>>> REMOTE IP:", request.remote_addr)

    print("=" * 60 + "\n")

# ================================
# ROOT
# ================================
@app.route("/", methods=["GET", "HEAD"])
def home():
    return "OK", 200

# ================================
# VER.PHP (LEGACY_7)
# ================================
@app.route("/live/ver.php", methods=["GET"])
def ver():
    start = time.time()

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
            print(">>> CLIENT ATUALIZADO")

            response_text = (
                "versioninfo\n"
                f"{LATEST_VERSION}\n"
                "update=0"
            )

        print("\n>>> RESPONSE RAW:\n", response_text)

        elapsed = round(time.time() - start, 4)
        print(f"\n>>> RESPONSE TIME: {elapsed}s")

        return Response(response_text, mimetype="text/plain")

    except Exception as e:
        print(">>> ERROR:", str(e))
        return "error", 500

# ================================
# FILEINFO
# ================================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    print("\n>>> FILEINFO REQUEST RECEIVED")

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
