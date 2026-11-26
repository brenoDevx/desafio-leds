
import csv
import random
from faker import Faker

fake = Faker("pt_BR")
random.seed(42)
Faker.seed(42)

ARQUIVO = "data/respostas.csv"
QUANTIDADE = 15

ESCOLARIDADE = ["A001", "A002", "A003", "A004", "A005"]

LINGUAGENS = [
    "Q13_S14",
    "Q13_S15",
    "Q13_S16",
    "Q13_S17",
    "Q13_S18"
]

AREAS = [
    "Desenvolvimento de software",
    "Suporte técnico",
    "Análise de dados",
    "Infraestrutura de TI",
    "Administração",
    "Educação",
    "Comércio",
    "Engenharia"
]


def gerar_aluno():
    trabalha = random.choice(["A001", "A002"])

    # Escolhe de zero a cinco linguagens
    linguagens_escolhidas = random.sample(
        LINGUAGENS,
        k=random.randint(0, len(LINGUAGENS))
    )

    # Monta os campos de múltipla escolha
    linguagens = {
        campo: ("Y" if campo in linguagens_escolhidas else "")
        for campo in LINGUAGENS
    }

    # Nenhuma é exclusiva das demais alternativas
    linguagens["Q13_S19"] = (
        "Y" if not linguagens_escolhidas else ""
    )

    aluno = {
        "Q4": fake.name(),
        "Q5": random.randint(17, 45),
        "Q6": random.choice(ESCOLARIDADE),
        **linguagens,
        "Q20": trabalha,
        "Q21": (
            random.choice(AREAS)
            if trabalha == "A001"
            else ""
        )
    }

    return aluno


def main():
    respostas = [
        gerar_aluno()
        for _ in range(QUANTIDADE)
    ]

    campos = [
        "Q4", "Q5", "Q6",
        "Q13_S14", "Q13_S15", "Q13_S16",
        "Q13_S17", "Q13_S18", "Q13_S19",
        "Q20", "Q21"
    ]

    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(respostas)

    print(f"{len(respostas)} respostas geradas!")
    print(f"Arquivo salvo em: {ARQUIVO}")


if __name__ == "__main__":
    main()
