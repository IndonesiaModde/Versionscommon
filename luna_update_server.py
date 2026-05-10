from flask import Flask, request
import os

app = Flask(__name__)

# Dados de resposta
VERSION_DATA = "1.17.1"
FILE_INFO_DATA = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET", "POST", "HEAD"])
def catch_all(path):
    # O Flask às vezes limpa as barras extras, mas vamos garantir
    # Log para monitoramento
    ua = request.headers.get("User-Agent", "Desconhecido")
    print(f"\n>>> REQUISIÇÃO: {request.method} /{path}")
    print(f">>> USER-AGENT: {ua}")
    
    # Se o jogo estiver pedindo a versão ou arquivos
    # Verificamos se o caminho contém 'live' ou 'ver.php'
    full_path = path.lower()
    
    if "ver.php" in full_path or "version" in full_path:
        print(f">>> ENVIANDO VERSÃO: {VERSION_DATA}")
        return VERSION_DATA
        
    if "fileinfo" in full_path:
        print(">>> ENVIANDO FILEINFO DATA")
        return FILE_INFO_DATA

    # Caso padrão para qualquer outra requisição do jogo
    return VERSION_DATA

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
