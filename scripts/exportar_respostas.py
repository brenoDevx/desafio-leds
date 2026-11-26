
import base64
import csv
import os

from teste_api import chamar_api, USERNAME, PASSWORD, SURVEY_ID


def main():
    session_key = chamar_api(
        "get_session_key",
        [USERNAME, PASSWORD]
    )

    if not session_key:
        print("Erro ao autenticar na API.")
        return

    try:
        resultado = chamar_api(
            "export_responses",
            [
                session_key,
                SURVEY_ID,
                "csv",
                "pt",
                "all",
                "code"
            ]
        )

        if not resultado:
            print("Nenhuma resposta encontrada.")
            return

        idioma = chamar_api(
            "get_survey_properties",
            [session_key, SURVEY_ID, ["language"]]
        )

        print("Configuração de idioma da pesquisa:", idioma)

        print("Tipo do retorno:", type(resultado))
        print("Conteúdo retornado pela API:", resultado)

        if isinstance(resultado, dict):
            print("A API retornou um dicionário. Verifique a mensagem acima.")
            return

        conteudo = base64.b64decode(resultado)

        os.makedirs("data", exist_ok=True)

        with open(
            "data/respostas_exportadas.csv",
            "wb"
        ) as arquivo:
            arquivo.write(conteudo)

        print("Exportação concluída!")
        print("Arquivo: data/respostas_exportadas.csv")

    finally:
        chamar_api("release_session_key", [session_key])


if __name__ == "__main__":
    main()
