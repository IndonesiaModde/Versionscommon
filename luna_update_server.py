from flask import Flask, request, Response, send_file
import os

app = Flask(__name__)

# 📁 pasta base dos assets
BASE_DIR = "assets/android/gameassetbundles"

# 🔢 versão (mude aqui quando quiser testar)
VERSION = "1.17.2"

# 📄 fileinfo (igual você já tem)
FILEINFO = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

# ==============================
# 🔍 LOG GLOBAL
# ==============================
@app.before_request
def log_request():
    print("\n==============================")
    print(f">>> METHOD: {request.method}")
    print(f">>> PATH: {request.path}")
    print(f">>> URL: {request.url}")

    if request.args:
        print(">>> PARAMS:")
        for k, v in request.args.items():
            print(f"   {k} = {v}")

    print("==============================\n")


# ==============================
# 🔹 1. VERSION (CORRETO AGORA)
# ==============================
@app.route("/live/ver.php")
def version():
    print(">>> RESPONDENDO VERSÃO SIMPLES")

    # ⚠️ IMPORTANTE: só versão
    return Response(
        VERSION,
        status=200,
        mimetype="text/plain"
    )


# ==============================
# 🔹 2. FILEINFO (SEPARADO)
# ==============================
@app.route("/assets/android/fileinfo")
def fileinfo():
    print(">>> ENVIANDO FILEINFO")

    return Response(
        FILEINFO,
        status=200,
        mimetype="text/plain"
    )


# ==============================
# 🔹 3. ASSETS (DOWNLOAD REAL)
# ==============================
@app.route("/assets/android/gameassetbundles/<path:filepath>")
def serve_asset(filepath):
    full_path = os.path.join(BASE_DIR, filepath)

    print(f">>> ASSET: {filepath}")
    print(f">>> PATH: {full_path}")

    if not os.path.exists(full_path):
        print(">>> ERRO: NÃO EXISTE ❌")
        return "Not Found", 404

    size = os.path.getsize(full_path)
    print(f">>> TAMANHO: {size} bytes")

    return send_file(full_path, as_attachment=False)


# ==============================
# 🔹 CAPTURA QUALQUER OUTRA ROTA
# ==============================
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    print(f">>> ROTA DESCONHECIDA: /{path}")
    return "OK", 200


# ==============================
# 🚀 START
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
