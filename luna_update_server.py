from flask import Flask, request, Response

app = Flask(__name__)

# CONFIG
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
# ROTA PRINCIPAL (VER.PHP)
# ==============================
@app.route("/live/ver.php", methods=["GET"])
def ver():
    log_request()

    print(">>> USANDO MODO FINAL: LEGACY_7")

    response_text = f"""versioninfo
{GAME_VERSION}
fileinfo=/assets/android/fileinfo"""

    return Response(response_text, mimetype="text/plain")

# ==============================
# FILEINFO (OBRIGATÓRIO)
# ==============================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    print("\n>>> FILEINFO REQUEST RECEBIDA")

    return {
        "status": "ok",
        "version": GAME_VERSION,
        "url": "https://discord.gg/gXXYjY8k4",
        "size": "12345678",
        "force": True
    }

# ==============================
# ROTA ROOT (EVITA ERRO NO RENDER)
# ==============================
@app.route("/", methods=["GET", "HEAD"])
def home():
    return "OK", 200

# ==============================
# START
# ==============================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
