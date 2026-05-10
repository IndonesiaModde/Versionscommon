from flask import Flask, request, Response, send_file
import os

app = Flask(__name__)

BASE_DIR = "assets/android/gameassetbundles"

VERSION = "1.17.1"

FILEINFO = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

# 🔹 VERSION ENDPOINT
@app.route("/live/ver.php")
def version():
    print(">>> VERSION REQUEST")

    response_text = f"""versioninfo
{VERSION}

fileinfo
{FILEINFO}
"""

    return Response(response_text, mimetype="text/plain")


# 🔹 ASSETS (CDN FAKE REAL)
@app.route("/assets/android/gameassetbundles/<path:filepath>")
def serve_asset(filepath):
    full_path = os.path.join(BASE_DIR, filepath)

    print(f">>> ASSET REQUEST: {filepath}")
    print(f">>> PATH: {full_path}")

    if not os.path.exists(full_path):
        print(">>> FILE NOT FOUND ❌")
        return "Not Found", 404

    return send_file(full_path, as_attachment=False)


# 🔹 DEBUG CATCH
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    print(f">>> UNKNOWN REQUEST: {path}")
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
