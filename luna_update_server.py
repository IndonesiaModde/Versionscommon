from flask import Flask, request, Response, jsonify
import time
import os

app = Flask(__name__)

# ================================
# CONFIG REAL (100% ORIGINAL)
# ================================
LATEST_VERSION = "1.17.2"

FILEINFO_URL = "https://versionscommon.onrender.com/assets/android/fileinfo"

APK_URL = "https://seuservidor.com/ff.apk"  # ⚠️ TROCAR PELO LINK REAL
APK_SIZE = "307889833"
APK_MD5 = "471ebda5ff6f1af2eecc8d43a3a4fda2"

# Dados reais dos arquivos (Mantido para suporte)
FILE_INFO_RAW = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

# ================================
# 🔥 ALL LOG SCANNER (100% ORIGINAL)
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
# SUPORTE A SLASHES EXTRAS (NOVO BYPASS)
# ================================
@app.route("/<path:path>", methods=["GET", "POST", "HEAD"])
def catch_all(path):
    # Se o jogo mandar barras extras, redirecionamos para as funções corretas
    if "ver.php" in path.lower():
        return ver()
    if "fileinfo" in path.lower():
        return fileinfo()
    return home()

# ================================
# VER.PHP (100% ORIGINAL COM MELHORIA)
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
# FILEINFO (100% ORIGINAL COM MELHORIA)
# ================================
@app.route("/assets/android/fileinfo", methods=["GET"])
def fileinfo():
    print("\n>>> FILEINFO REQUEST RECEIVED")
    # Para o Unity, o ideal é retornar texto puro como o original da Luna
    return Response(FILE_INFO_RAW, mimetype="text/plain")

# ================================
# START SERVER
# ================================
if __name__ == "__main__":
    # Suporte automático para porta do Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
