import pandas as pd

CAMINHO = "Controle_EquipamentosSRHS.xlsx"



def carregar_dados():
    return pd.read_excel(CAMINHO)



def verificar_sem_tombamento(df):
    coluna = "Tombamento"

    df_sem = df[
        df[coluna].isna() |
        (df[coluna].astype(str).str.strip() == "") |
        (df[coluna].astype(str).str.lower() == "nan")
    ]

    print(f"\nTotal sem tombamento detectado: {len(df_sem)}")
    return df_sem


def tombamento_duplicado(df, tombamento):
    return tombamento in df["Tombamento"].astype(str).values


def numero_serie_duplicado(df, numero_serie):
    return numero_serie in df["Número de Série"].astype(str).values




def gerar_relatorio(df):

    print("\n========== RELATÓRIO ==========")

    df_sem_tombamento = verificar_sem_tombamento(df)

    total_geral = pd.DataFrame({
        "Descrição": ["Total de Equipamentos"],
        "Valor": [len(df)]
    })

    total_por_tipo = df["Equipamento"].value_counts().reset_index()
    total_por_tipo.columns = ["Equipamento", "Quantidade"]

    total_por_setor = df["Setor"].value_counts().reset_index()
    total_por_setor.columns = ["Setor", "Quantidade"]

    total_locado = df["Locado"].value_counts().reset_index()
    total_locado.columns = ["Status Locado", "Quantidade"]

    with pd.ExcelWriter("Relatorio_Equipamentos.xlsx", engine="openpyxl") as writer:
        total_geral.to_excel(writer, sheet_name="Resumo Geral", index=False)
        df_sem_tombamento.to_excel(writer, sheet_name="Sem Tombamento", index=False)
        total_por_tipo.to_excel(writer, sheet_name="Por Tipo", index=False)
        total_por_setor.to_excel(writer, sheet_name="Por Setor", index=False)
        total_locado.to_excel(writer, sheet_name="Status Locado", index=False)

    print("\n✅ Relatorio_Equipamentos.xlsx gerado com sucesso!")




def cadastrar_equipamento(df):

    print("\n=== CADASTRO DE NOVO EQUIPAMENTO ===")

    equipamento = input("Tipo (Desktop/Monitor/Laptop): ")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    numero_serie = input("Número de Série: ")
    service_tag = input("Service TAG (S/N): ")
    tombamento = input("Tombamento: ")
    especificacoes = input("Especificações Técnicas: ")
    locado = input("Locado (SIM/NÃO): ")
    setor = input("Setor: ")
    responsavel = input("Responsável: ")
    observacoes = input("Observações: ")

    if tombamento_duplicado(df, tombamento):
        print("\n ERRO: Tombamento já existe!")
        return df

    if numero_serie and numero_serie_duplicado(df, numero_serie):
        print("\n ERRO: Número de Série já existe!")
        return df

    novo = {
        "Equipamento": equipamento,
        "Marca": marca,
        "Modelo": modelo,
        "Número de Série": numero_serie,
        "Service TAG (S/N)": service_tag,
        "Tombamento": tombamento,
        "Especificações Técnicas": especificacoes,
        "Locado": locado,
        "Setor": setor,
        "Responsável": responsavel,
        "Observações": observacoes
    }

    df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
    df.to_excel(CAMINHO, index=False)

    print("\n✅ Equipamento cadastrado com sucesso!")
    return df



def excluir_equipamento(df):

    print("\n=== EXCLUIR EQUIPAMENTO ===")

    tombamento = input("Digite o Tombamento do equipamento que deseja excluir: ").strip()

    filtro = df["Tombamento"].astype(str).str.strip() == tombamento

    if not filtro.any():
        print("\n❌ Nenhum equipamento encontrado com esse tombamento.")
        return df

    equipamento = df[filtro]

    print("\nEquipamento encontrado:")
    print(equipamento)

    confirmar = input("\nTem certeza que deseja excluir? (S/N): ")

    if confirmar.upper() == "S":
        df = df[~filtro]
        df.to_excel(CAMINHO, index=False)
        print("\n✅ Equipamento excluído com sucesso!")
    else:
        print("\nOperação cancelada.")

    return df




def main():

    print("\n===== SISTEMA DE CONTROLE DE EQUIPAMENTOS =====")

    df = carregar_dados()

    print("\n1 - Gerar Relatório")
    print("2 - Cadastrar Equipamento")
    print("3 - Verificar Equipamentos Sem Tombamento")
    print("4 - Excluir Equipamento")
    print("0 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        gerar_relatorio(df)

    elif opcao == "2":
        df = cadastrar_equipamento(df)

    elif opcao == "3":
        verificar_sem_tombamento(df)

    elif opcao == "4":
        df = excluir_equipamento(df)

    elif opcao == "0":
        print("Encerrando sistema...")

    else:
        print("Opção inválida!")


if __name__ == "__main__":
    main()