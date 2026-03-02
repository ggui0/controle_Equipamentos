# controle_Equipamentos

**🖥️ Sistema Web de Controle de Equipamentos**


Sistema web desenvolvido para gerenciamento de equipamentos de TI, permitindo cadastro, movimentação, histórico e exportação de dados de forma organizada e escalável.

O projeto evoluiu de uma planilha Excel tradicional para uma aplicação web completa utilizando Flask.

**📌 Sobre o Projeto**

• Este sistema foi criado para substituir o controle manual via planilhas por uma aplicação web com:

• Interface dinâmica

• Banco de dados estruturado

• Histórico de movimentações

• Exportação de relatórios

**Filtros avançados estilo Excel**

🚀 Funcionalidades

✔ Importação de planilha Excel
✔ Cadastro de equipamentos
✔ Edição em tempo real
✔ Exclusão de registros
✔ Movimentação entre setores
✔ Histórico completo de movimentações
✔ Paginação automática
✔ Filtro dinâmico por coluna
✔ Exportação para Excel, PDF e impressão
✔ Organização modular com Flask Blueprints



**🛠 Tecnologias Utilizadas**

🔹 Backend

• Python 3.14

• Flask

• SQLite3

• Pandas

• OpenPyXL

🔹 Frontend

• HTML5

• CSS3

• JavaScript

• jQuery

• DataTables

• DataTables Buttons



O sistema utiliza SQLite3 com as seguintes tabelas:

**# equipamentos**

 • Armazena os dados principais dos ativos.

**# movimentacoes**

 • Registra todas as transferências, retiradas e devoluções para controle histórico.

 📊 Evolução do Projeto
Planilha Excel
      ↓
Automação via Terminal
      ↓
Sistema Flask básico
      ↓
Banco SQLite
      ↓
Interface dinâmica com DataTables
      ↓
Arquitetura modular com Blueprints

 **🔐 Possiveis Próximas Implementações**

  • Sistema de login e autenticação

  • Controle de permissões (admin / usuário)

  • Deploy em servidor VPS

  • Dashboard com métricas

  • API REST

  • Migração para PostgreSQL
  
 **📈 Objetivo**

Desenvolver uma aplicação escalável e profissional para controle de ativos de TI, utilizando boas práticas de organização, separação de responsabilidades e estrutura modular.


**🧮 Módulo de Automação via Planilha (Versão Inicial do Sistema)**

Antes da versão web, o projeto começou como um sistema de automação em Python para manipulação direta da planilha Excel.

Esse módulo foi responsável por:

Ler dados da planilha .xlsx

Validar inconsistências

Evitar duplicidade de tombamento

Gerar relatórios automáticos

Permitir cadastro via terminal

Permitir exclusão controlada

Atualizar a planilha automaticamente


**📂 Arquivo**

automacao.py

🛠 Tecnologias Utilizadas

• Python

• Pandas

• OpenPyXL

• Excel (.xlsx)

**🔎 Funcionalidades Implementadas**
📥 Leitura da Planilha

def carregar_dados():
    return pd.read_excel(CAMINHO)

Carrega automaticamente todos os registros da planilha.

Converte em DataFrame para manipulação estruturada.

**⚠️ Validação de Dados**

Verificação de Equipamentos sem Tombamento
def verificar_sem_tombamento(df):

Identifica registros com:

• Tombamento vazio

• Null

• "nan"

• Espaços em branco

**🚫 Prevenção de Duplicidade**

Valida:

•Tombamento duplicado

•Número de série duplicado

•Evita inconsistências antes da gravação no Excel.

**📊 Geração de Relatórios Automatizados**

def gerar_relatorio(df):

Cria automaticamente um arquivo:

Relatorio_Equipamentos.xlsx

Com abas:

• Resumo Geral

• Equipamentos sem tombamento

• Total por tipo

• Total por setor

• Status de locação

Tudo gerado programaticamente.

**➕ Cadastro via Terminal**

def cadastrar_equipamento(df):

Permite:

Inserir novo equipamento

Validar duplicidade

Salvar diretamente na planilha

Atualizar arquivo Excel automaticamente

**🗑 Exclusão Controlada**

def excluir_equipamento(df):

Fluxo:

• Solicita tombamento

• Verifica existência

•Mostra dados encontrados

• Solicita confirmação

• Remove da planilha

• Atualiza Excel

**🧠 Estrutura do Sistema (Modo Terminal)**
===== SISTEMA DE CONTROLE DE EQUIPAMENTOS =====

1 - Gerar Relatório
2 - Cadastrar Equipamento
3 - Verificar Equipamentos Sem Tombamento
4 - Excluir Equipamento
0 - Sair

Interface totalmente via CLI (Command Line Interface).

**📈 Importância no Projeto**

Essa etapa foi essencial porque:

• Validou regras de negócio

• Criou estrutura de dados consistente

• Definiu campos obrigatórios

• Estruturou lógica de movimentação

• Serviu de base para migração para banco SQLite

• Facilitou transição para sistema web

**🔄 Evolução do Projeto**
Planilha manual
      ↓
Automação via Python (Terminal)
      ↓
Validação e relatórios automatizados
      ↓
Migração para SQLite
      ↓
Sistema Web Flask
💡 Impacto Técnico

Esse módulo demonstrou:

• Manipulação de dados com Pandas

• Tratamento de inconsistências

• Escrita estruturada em Excel

• Organização de código procedural

• Implementação de regras de negócio

• Primeira etapa de transformação digital do processo

**👨‍💻 Autor**

Desenvolvido por Guilherme Pietro
