from flask import Flask, request, Response
import os

app = Flask(__name__)

VERSION = "1.17.1"

FILEINFO = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET", "POST"])
def catch_all(path):
    ua = request.headers.get("User-Agent", "Unknown")

    print(f"\n>>> {request.method} /{path}")
    print(f">>> UA: {ua}")

    response_text = f"""versioninfo
{VERSION}

fileinfo
{FILEINFO}
"""

    return Response(
        response_text,
        status=200,
        mimetype="text/plain; charset=utf-8"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
