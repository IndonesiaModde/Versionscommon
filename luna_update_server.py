from flask import Flask, request
import json
import os

app = Flask(__name__)

# --- DADOS DE RESPOSTA (IGUAL AO ANTERIOR) ---
VERSION_DATA = "1.17.1"
FILE_INFO_DATA = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def super_logger(path):
    print("\n" + "="*50)
    print(f"[!] NOVA REQUISIÇÃO RECEBIDA")
    print(f"    URL: /{path}")
    print(f"    MÉTODO: {request.method}")
    print(f"    IP: {request.remote_addr}")
    
    print("\n[+] CABEÇALHOS (HEADERS):")
    for key, value in request.headers.items():
        print(f"    {key}: {value}")
        
    if request.args:
        print("\n[+] PARÂMETROS DA URL (GET):")
        for key, value in request.args.items():
            print(f"    {key}: {value}")
            
    if request.data:
        print("\n[+] DADOS BRUTOS (BODY):")
        try:
            print(f"    {request.data.decode('utf-8')}")
        except:
            print(f"    [Dados Binários: {len(request.data)} bytes]")
            
    print("="*50 + "\n")

    # Respostas baseadas no que você já configurou
    if "live" in path:
        if "fileinfo" in path.lower():
            return FILE_INFO_DATA
        return VERSION_DATA
    
    return VERSION_DATA

if __name__ == "__main__":
    # Suporte automático para porta do Render ou porta 8000 local
    port = int(os.environ.get("PORT", 8000))
    print(f"--- LUNA SUPER LOG SERVER ONLINE NA PORTA {port} ---")
    app.run(host='0.0.0.0', port=port)
