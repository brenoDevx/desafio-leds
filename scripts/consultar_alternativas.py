
from dotenv import load_dotenv
from teste_api import chamar_api, USERNAME, PASSWORD

def main():
    session_key = chamar_api(
        "get_session_key",
        [USERNAME, PASSWORD]
    )

    try:
        perguntas = {
            6: "Escolaridade",
            20: "Situação profissional"
        }

        for question_id, nome in perguntas.items():
            print(f"\n{'=' * 40}")
            print(f"PERGUNTA: {nome}")
            print(f"{'=' * 40}")

            resultado = chamar_api(
                "get_question_properties",
                [
                    session_key,
                    question_id,
                    ["answeroptions"]
                ]
            )

            print(resultado)

    finally:
        chamar_api(
            "release_session_key",
            [session_key]
        )


if __name__ == "__main__":
    main()
