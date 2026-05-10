from flask import Flask, request, Response, jsonify
import json

app = Flask(__name__)

LATEST_VERSION = "1.17.2"

# memória simples (cache)
working_mode = None


def log_request():
    print("\n==============================")
    print(">>> METHOD:", request.method)
    print(">>> PATH:", request.path)
    print(">>> URL:", request.url)
    print(">>> PARAMS:")
    for k, v in request.args.items():
        print(f"   {k} = {v}")
    print("==============================")


def build_response(mode):
    if mode == "LEGACY_1":
        return Response(LATEST_VERSION, mimetype="text/plain")

    elif mode == "LEGACY_2":
        return Response(LATEST_VERSION + "\n", mimetype="text/plain")

    elif mode == "LEGACY_3":
        return Response(f"versioninfo\n{LATEST_VERSION}", mimetype="text/plain")

    elif mode == "LEGACY_4":
        return Response(f"versioninfo\n{LATEST_VERSION}\nfileinfo=/fileinfo", mimetype="text/plain")

    elif mode == "LEGACY_5":
        return Response(f"version={LATEST_VERSION}\nfileinfo=/fileinfo", mimetype="text/plain")

    elif mode == "LEGACY_6":
        return Response(f"versioninfo={LATEST_VERSION}\nfileinfo=/fileinfo", mimetype="text/plain")

    elif mode == "LEGACY_7":
        return Response(f"versioninfo\n{LATEST_VERSION}\nfileinfo=/assets/android/fileinfo", mimetype="text/plain")

    elif mode == "LEGACY_8":
        return Response(f"version={LATEST_VERSION}\nfileinfo=/assets/android/fileinfo", mimetype="text/plain")

    elif mode == "JSON_STRICT":
        return Response(
            json.dumps({
                "status": "ok",
                "version": LATEST_VERSION,
                "fileinfo": "/assets/android/fileinfo"
            }),
            mimetype="application/json"
        )

    return Response("invalid", mimetype="text/plain")


@app.route("/live/ver.php", methods=["GET"])
def version_check():
    global working_mode

    log_request()

    modes = [
        "LEGACY_1",
        "LEGACY_2",
        "LEGACY_3",
        "LEGACY_4",
        "LEGACY_5",
        "LEGACY_6",
        "LEGACY_7",
        "LEGACY_8",
        "JSON_STRICT"
    ]

    # se já encontrou um modo válido
    if working_mode:
        print(f">>> USANDO MODO FIXO: {working_mode}")
        return build_response(working_mode)

    # testa automaticamente
    for mode in modes:
        print(f">>> TESTANDO MODO: {mode}")
        resp = build_response(mode)

        # aqui você pode forçar um modo manualmente depois
        # por enquanto só retorna o primeiro (igual teu antigo)
        
        print(f">>> DEFINIDO COMO FUNCIONAL: {mode}")
        return resp

    return Response("error", mimetype="text/plain")


@app.route("/")
def home():
    return "Server Online"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
