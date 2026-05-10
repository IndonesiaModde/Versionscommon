from flask import Flask, request, Response, jsonify
import os

app = Flask(__name__)

# ==============================
# CONFIG
# ==============================
GAME_VERSION = "1.17.2"

# ==============================
# LOG PADRÃO
# ==============================
def log_request():
    print("\n==============================")
    print(">>> METHOD:", request.method)
    print(">>> PATH:", request.path)
    print(">>> PARAMS:", dict(request.args))
    print("==============================")

# ==============================
# /live/ver.php (VERSÃO)
# ==============================
@app.route("/live/ver.php", methods=["GET"])
def ver():
    log_request()

    print(">>> USANDO MODO FINAL: LEGACY_7")

    # ⚠️ STRING CRÍTICA (SEM QUEBRA EXTRA)
    response_text = f"versioninfo\n{GAME_VERSION}\nfileinfo=/assets/android/fileinfo"

    # DEBUG BRUTO
    print(">>> RESPONSE RAW:", repr(response_text))

    return Response(
        response_text,
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            "Connection": "keep-alive"
        }
    )

# ==============================
# /assets/android/fileinfo
# ==============================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    print("\n>>> FILEINFO REQUEST RECEBIDA")

    data = {
        "status": "ok",
        "version": GAME_VERSION,
        "url": "https://discord.gg/gXXYjY8k4",  # ⚠️ TROCAR DEPOIS
        "size": "12345678",
        "force": False
    }

    print(">>> RESPONSE FILEINFO:", data)

    return jsonify(data)

# ==============================
# ROOT (OBRIGATÓRIO NO RENDER)
# ==============================
@app.route("/", methods=["GET", "HEAD"])
def home():
    return "OK", 200

# ==============================
# START
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
