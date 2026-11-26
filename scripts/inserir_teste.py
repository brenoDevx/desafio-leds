
from teste_api import chamar_api, USERNAME, PASSWORD, SURVEY_ID


def main():
    session_key = chamar_api(
        "get_session_key",
        [USERNAME, PASSWORD]
    )

    if not isinstance(session_key, str):
        raise RuntimeError(f"Falha na autenticação: {session_key}")

    # Resposta fictícia de teste
    resposta = {
        "Q4": "Aluno Teste",
        "Q5": "22",
        "Q6": "A003",

        # Linguagens conhecidas
        "Q13_S14": "Y",  # Python
        "Q13_S15": "N",  # Java
        "Q13_S16": "Y",  # JavaScript
        "Q13_S17": "N",  # C/C++
        "Q13_S18": "N",  # PHP
        "Q13_S19": "N",  # Nenhuma

        "Q20": "A001",   # Trabalha: Sim
        "Q21": "Desenvolvimento de software"
    }

    try:
        resultado = chamar_api(
            "add_response",
            [session_key, SURVEY_ID, resposta]
        )

        if resultado is not None and str(resultado).isdigit():
            print("Resposta inserida com sucesso!")
            print(f"ID da resposta: {resultado}")
        else:
            print("Falha ao inserir resposta:", resultado)

    finally:
        chamar_api(
            "release_session_key",
            [session_key]
        )


if __name__ == "__main__":
    main()
