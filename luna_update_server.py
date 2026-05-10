from flask import Flask, request, Response

app = Flask(__name__)

LATEST_VERSION = "1.17.2"

MODES = [
    "LEGACY_7",  # 🔥 PRIORIDADE REAL
    "LEGACY_8",
    "LEGACY_6",
    "LEGACY_5",
    "LEGACY_4",
    "LEGACY_3",
    "LEGACY_2",
    "LEGACY_1"
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


@app.route("/live/ver.php", methods=["GET"])
def version_check():
    global working_mode

    print("\n==============================")
    print(">>> PARAMS:", dict(request.args))
    print("==============================")

    # já encontrou → usa direto
    if working_mode:
        print(f">>> USANDO MODO FINAL: {working_mode}")
        return Response(build_response(working_mode), mimetype="text/plain")

    # 🔥 agora escolhe o MAIS COMPLETO
    for mode in MODES:
        resp = build_response(mode)

        print(f">>> TESTANDO: {mode}")
        print(resp)

        if "fileinfo" in resp:
            working_mode = mode
            print(f">>> DEFINIDO COMO CORRETO: {mode}")
            break

    return Response(build_response(working_mode), mimetype="text/plain")


@app.route("/")
def home():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
