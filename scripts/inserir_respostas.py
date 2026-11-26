
import csv
from teste_api import chamar_api, USERNAME, PASSWORD, SURVEY_ID

ARQUIVO = "data/respostas.csv"


def main():
    with open(ARQUIVO, newline="", encoding="utf-8") as arquivo:
        respostas = list(csv.DictReader(arquivo))

    session_key = chamar_api(
        "get_session_key",
        [USERNAME, PASSWORD]
    )

    if not isinstance(session_key, str):
        raise RuntimeError("Falha na autenticação.")

    sucessos = 0
    falhas = 0

    try:
        for numero, resposta in enumerate(respostas, start=1):

            # Remove campos vazios antes do envio
            dados = {
                campo: valor
                for campo, valor in resposta.items()
                if valor.strip()
            }

            try:
                resultado = chamar_api(
                    "add_response",
                    [session_key, SURVEY_ID, dados]
                )

                if resultado is not None and str(resultado).isdigit():
                    sucessos += 1
                    print(
                        f"[{numero}/{len(respostas)}] "
                        f"Resposta inserida. ID: {resultado}"
                    )
                else:
                    falhas += 1
                    print(
                        f"[{numero}/{len(respostas)}] "
                        f"Falha: {resultado}"
                    )

            except Exception as erro:
                falhas += 1
                print(f"[{numero}/{len(respostas)}] Erro: {erro}")

    finally:
        chamar_api(
            "release_session_key",
            [session_key]
        )

    print("\n========== RESULTADO ==========")
    print(f"Total processado: {len(respostas)}")
    print(f"Sucessos: {sucessos}")
    print(f"Falhas: {falhas}")


if __name__ == "__main__":
    main()
