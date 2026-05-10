from flask import Flask, request, Response

app = Flask(__name__)

LATEST_VERSION = "1.17.2"

# 🔥 MODO DEFINIDO (sem auto-teste agora)
WORKING_MODE = "LEGACY_7"


def build_response():
    if WORKING_MODE == "LEGACY_7":
        return f"versioninfo\n{LATEST_VERSION}\nfileinfo=/assets/android/fileinfo"


# ================================
# 🔹 VERSION CHECK
# ================================
@app.route("/live/ver.php", methods=["GET"])
def version_check():
    print("\n==============================")
    print(">>> METHOD:", request.method)
    print(">>> PATH:", request.path)
    print(">>> PARAMS:", dict(request.args))
    print("==============================")

    resp = build_response()

    print(">>> USANDO MODO FIXO: LEGACY_7")
    print(">>> RESPOSTA:\n" + resp)

    return Response(resp, mimetype="text/plain")


# ================================
# 🔹 FILEINFO (🔥 ESSENCIAL)
# ================================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    print("\n==============================")
    print(">>> FILEINFO REQUEST RECEBIDA")
    print("==============================")

    # 🔥 versão compatível (texto simples)
    resp = f"""version={LATEST_VERSION}
url=https://discord.gg/gXXYjY8k4
force=1
"""

    print(">>> RESPOSTA FILEINFO:\n" + resp)

    return Response(resp, mimetype="text/plain")


# ================================
# 🔹 TESTE ROOT
# ================================
@app.route("/")
def home():
    return "SERVER OK", 200


# ================================
# 🔹 START
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
