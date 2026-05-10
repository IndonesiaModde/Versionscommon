from flask import Flask, request, Response, jsonify
import os

app = Flask(__name__)

# ================================
# CONFIG REAL (BYPASS LUNA)
# ================================
# Versão atualizada para 1.17.2 conforme seu código
LATEST_VERSION = "1.17.1"

# URLs do servidor
FILEINFO_URL = "https://versionscommon.onrender.com/assets/android/fileinfo"
APK_URL = "https://seuservidor.com/ff.apk" 
APK_SIZE = "307889833"
APK_MD5 = "471ebda5ff6f1af2eecc8d43a3a4fda2"

# Dados reais dos arquivos para o Fileinfo
FILE_INFO_RAW = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

# ================================
# LOG UNIVERSAL (SUPER SCANNER)
# ================================
@app.before_request
def log_request():
    print("\n" + "="*40)
    print(f">>> {request.method} -> {request.path}")
    if request.args: print(f">>> PARAMS: {dict(request.args)}")
    print("="*40)

# ================================
# ROTAS (SUPORTE A SLASHES EXTRAS)
# ================================

@app.route("/", methods=["GET", "HEAD"])
def home():
    return "LUNA SERVER V5 ONLINE", 200

# Usamos um capturador universal para lidar com as barras extras do APK
@app.route("/<path:path>", methods=["GET", "POST"])
def catch_all(path):
    # 1. VER.PHP (TRATAMENTO DE VERSÃO)
    if "ver.php" in path.lower():
        return ver_handler()
        
    # 2. FILEINFO (TRATAMENTO DE ARQUIVOS)
    if "fileinfo" in path.lower():
        return fileinfo_handler()
        
    return home()

def ver_handler():
    try:
        client_version = request.args.get("version", "0")
        print(f">>> CLIENT VERSION: {client_version}")

        if client_version != LATEST_VERSION:
            print(">>> STATUS: UPDATE NECESSÁRIO")
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
            print(">>> STATUS: JÁ ATUALIZADO")
            response_text = f"versioninfo\n{LATEST_VERSION}\nupdate=0"

        print(f">>> RESPONSE RAW:\n{response_text}")
        return Response(response_text, mimetype="text/plain")

    except Exception as e:
        print(f">>> ERRO: {str(e)}")
        return "error", 500

def fileinfo_handler():
    print(">>> FILEINFO REQUEST RECEBIDA")
    # Retorna os dados brutos dos arquivos que o jogo espera
    return Response(FILE_INFO_RAW, mimetype="text/plain")

# ================================
# START SERVER
# ================================
if __name__ == "__main__":
    # Suporte automático para porta do Render ou porta 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
