from flask import Flask, request, Response
import time

app = Flask(__name__)

LATEST_VERSION = "1.17.2"

# ordem REAL baseada nos seus testes
MODES = [
    "LEGACY_1",  # 🔥 MAIS COMPATÍVEL
    "LEGACY_2",
    "LEGACY_3",
    "LEGACY_4",
    "LEGACY_5",
    "LEGACY_6",
    "LEGACY_7",
    "LEGACY_8",
    "JSON_STRICT"
]

working_mode = None


def build_response(mode):
    if mode == "LEGACY_1":
        return LATEST_VERSION

    elif mode == "LEGACY_2":
        return LATEST_VERSION + "\n"

    elif mode == "LEGACY_3":
        return f"versioninfo\n{LATEST_VERSION}"

    elif mode == "LEGACY_4":
        return f"versioninfo\n{LATEST_VERSION}\nfileinfo=/fileinfo"

    elif mode == "LEGACY_5":
        return f"version={LATEST_VERSION}\nfileinfo=/fileinfo"

    elif mode == "LEGACY_6":
        return f"versioninfo={LATEST_VERSION}\nfileinfo=/fileinfo"

    elif mode == "LEGACY_7":
        return f"versioninfo\n{LATEST_VERSION}\nfileinfo=/assets/android/fileinfo"

    elif mode == "LEGACY_8":
        return f"version={LATEST_VERSION}\nfileinfo=/assets/android/fileinfo"

    elif mode == "JSON_STRICT":
        return '{"status":"ok","version":"' + LATEST_VERSION + '","fileinfo":"/assets/android/fileinfo"}'

    return LATEST_VERSION


@app.route("/live/ver.php", methods=["GET"])
def version_check():
    global working_mode

    print("\n==============================")
    print(">>> METHOD:", request.method)
    print(">>> PATH:", request.path)
    print(">>> PARAMS:", dict(request.args))
    print("==============================")

    # 🚀 já descobriu modo → usa direto
    if working_mode:
        print(f">>> USANDO MODO FIXO: {working_mode}")
        return Response(build_response(working_mode), mimetype="text/plain")

    # 🔍 auto-teste
    for mode in MODES:
        resp = build_response(mode)

        print(f">>> TESTANDO MODO: {mode}")
        print(f">>> RESPOSTA:\n{resp}")

        # ⚠️ regra REAL:
        # evita JSON como prioridade
        if "{" not in resp:
            working_mode = mode
            print(f">>> DEFINIDO COMO FUNCIONAL: {mode}")
            break

    return Response(build_response(working_mode), mimetype="text/plain")


@app.route("/")
def home():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
