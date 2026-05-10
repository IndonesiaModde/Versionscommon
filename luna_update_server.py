from flask import Flask, request

app = Flask(__name__)

# --- DADOS DE ATUALIZAÇÃO (VERSIONINFO) ---
VERSION_DATA = "1.17.1"

# --- DADOS DE ARQUIVOS (FILEINFO) ---
FILE_INFO_DATA = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def handle_update(path):
    # Log simples para você ver no console do Render/Termux
    print(f"[+] Pedido recebido: /{path}")
    
    # Se o jogo pedir a versão ou informações de arquivo
    # Baseado na URL longa: /live/100067...
    if "live" in path:
        # Se o jogo estiver pedindo a lista de arquivos (geralmente após a versão)
        if "fileinfo" in path.lower():
            return FILE_INFO_DATA
        # Por padrão, retorna a versão para liberar o jogo
        return VERSION_DATA
    
    return VERSION_DATA

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

