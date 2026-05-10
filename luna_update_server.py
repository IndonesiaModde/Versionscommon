from flask import Flask, request, Response
import json

app = Flask(__name__)

VERSION = "1.17.2"

# 🔥 MUDE AQUI MANUALMENTE
MODE = "JSON_WITH_FILEINFO"

def build_response(mode):
    if mode == "JSON_BASIC":
        return {"version": VERSION}

    if mode == "JSON_STATUS":
        return {"status": "ok", "version": VERSION}

    if mode == "JSON_WITH_FILEINFO":
        return {
            "status": "ok",
            "version": VERSION,
            "fileinfo": "/assets/android/fileinfo"
        }

    if mode == "JSON_CAMEL":
        return {
            "status": "ok",
            "version": VERSION,
            "fileInfo": "/assets/android/fileinfo"
        }

    if mode == "JSON_FULL":
        return {
            "status": "ok",
            "version": VERSION,
            "versioninfo": VERSION,
            "fileinfo": "/assets/android/fileinfo",
            "cdn": "/assets/android/gameassetbundles/"
        }

    if mode == "JSON_EXTREME":
        return {
            "status": "ok",
            "version": VERSION,
            "versioninfo": VERSION,
            "fileinfo": "/assets/android/fileinfo",
            "fileInfo": "/assets/android/fileinfo",
            "assets": "/assets/android/gameassetbundles/",
            "resUrl": "/assets/android/gameassetbundles/"
        }

@app.route("/live/ver.php")
def version():
    print("\n==============================")
    print(f">>> USANDO MODO: {MODE}")

    data = build_response(MODE)
    response_text = json.dumps(data)

    print(f">>> RESPOSTA: {response_text}")

    return Response(response_text, mimetype="application/json")


# FILEINFO
@app.route("/assets/android/fileinfo")
@app.route("/fileinfo")
@app.route("/live/fileinfo")
def fileinfo():
    print(">>> 🔥 FILEINFO CHAMADO 🔥")

    return """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
