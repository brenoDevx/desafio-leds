
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("LIMESURVEY_URL")
USERNAME = os.getenv("LIMESURVEY_USERNAME")
PASSWORD = os.getenv("LIMESURVEY_PASSWORD")
SURVEY_ID = int(os.getenv("LIMESURVEY_SURVEY_ID"))

def chamar_api(metodo, parametros):
    payload = {
        "method": metodo,
        "params": parametros,
        "id": 1
    }

    response = requests.post(
        API_URL,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    resultado = response.json()

    if resultado.get("error"):
        raise RuntimeError(resultado["error"])

    return resultado.get("result")


def main():
    session_key = chamar_api(
        "get_session_key",
        [USERNAME, PASSWORD]
    )

    if not isinstance(session_key, str):
        raise RuntimeError(
            f"Falha na autenticação: {session_key}"
        )

    print("Autenticação realizada com sucesso!")

    try:
        fieldmap = chamar_api(
            "get_fieldmap",
            [session_key, SURVEY_ID]
        )

        print("\nCampos encontrados na pesquisa:\n")

        for campo, informacoes in fieldmap.items():
            print(campo, "->", informacoes)

    finally:
        chamar_api(
            "release_session_key",
            [session_key]
        )

        print("\nSessão encerrada.")


if __name__ == "__main__":
    main()
