from flask import Flask, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

DATABASE = "database.db"
PLANILHA = "Controle_EquipamentosSRHS.xlsx"



def criar_banco():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            marca TEXT,
            modelo TEXT,
            numero_serie TEXT,
            service_tag TEXT,
            tombamento TEXT,
            especificacoes TEXT,
            locado TEXT,
            setor TEXT,
            responsavel TEXT,
            observacoes TEXT,
            status TEXT DEFAULT 'ATIVO'
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipamento_id INTEGER,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        tipo_movimentacao TEXT,
        de_setor TEXT,
        para_setor TEXT,
        novo_responsavel TEXT,
        usuario TEXT
    )
""")

    conn.commit()
    conn.close()



def importar_planilha():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_excel(PLANILHA)

    df = df.rename(columns={
        "Equipamento": "tipo",
        "Marca": "marca",
        "Modelo": "modelo",
        "Número de Série": "numero_serie",
        "Service TAG (S/N)": "service_tag",
        "Tombamento": "tombamento",
        "Especificações Técnicas": "especificacoes",
        "Locado": "locado",
        "Setor": "setor",
        "Responsável": "responsavel",
        "Observações": "observacoes"
    })

    df["status"] = "ATIVO"

    df.to_sql("equipamentos", conn, if_exists="append", index=False)

    conn.close()

    return "✅ Planilha importada com sucesso!"



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/importar")
def importar():
    mensagem = importar_planilha()
    return mensagem


@app.route("/testar")
def testar():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM equipamentos")
    total = cursor.fetchone()[0]
    conn.close()
    return f"Total de equipamentos no banco: {total}"

@app.route("/equipamentos")
def listar_equipamentos():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            id,
            tipo,
            marca,
            modelo,
            numero_serie,
            service_tag,
            tombamento,
            especificacoes,
            locado,
            setor,
            responsavel,
            observacoes,
            status
        FROM equipamentos
    """)

    equipamentos = cursor.fetchall()
    conn.close()

    return render_template("equipamentos.html", equipamentos=equipamentos)

from flask import request, redirect, url_for

@app.route("/movimentar/<int:id>", methods=["GET", "POST"])
def movimentar(id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    
    cursor.execute("SELECT * FROM equipamentos WHERE id = ?", (id,))
    equipamento = cursor.fetchone()

    if not equipamento:
        conn.close()
        return "Equipamento não encontrado"

    if request.method == "POST":

        tipo_mov = request.form["tipo_movimentacao"]
        para_setor = request.form["para_setor"]
        novo_responsavel = request.form["responsavel"]
        usuario_sistema = request.form["usuario"]

        de_setor = equipamento["setor"]

        
        cursor.execute("""
            UPDATE equipamentos
            SET setor = ?, responsavel = ?
            WHERE id = ?
        """, (para_setor, novo_responsavel, id))

        
        cursor.execute("""
    INSERT INTO movimentacoes
    (equipamento_id, tipo_movimentacao, de_setor, para_setor, novo_responsavel, usuario)
    VALUES (?, ?, ?, ?, ?, ?)
""", (id, tipo_mov, de_setor, para_setor, novo_responsavel, usuario_sistema))

        conn.commit()
        conn.close()

        return redirect(url_for("listar_equipamentos"))

    conn.close()
    return render_template("movimentar.html", equipamento=equipamento)


@app.route("/historico")
def historico():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m.*, e.tipo, e.modelo
        FROM movimentacoes m
        JOIN equipamentos e ON m.equipamento_id = e.id
        ORDER BY m.data DESC
    """)

    registros = cursor.fetchall()
    conn.close()

    return render_template("historico.html", registros=registros)
    

from flask import request, redirect, url_for



@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():

    if request.method == "POST":

        tipo = request.form["tipo"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        numero_serie = request.form["numero_serie"]
        service_tag = request.form["service_tag"]
        tombamento = request.form["tombamento"]
        especificacoes = request.form["especificacoes"]
        locado = request.form["locado"]
        setor = request.form["setor"]
        responsavel = request.form["responsavel"]
        observacoes = request.form["observacoes"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO equipamentos (
                tipo, marca, modelo, numero_serie,
                service_tag, tombamento, especificacoes,
                locado, setor, responsavel, observacoes, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ATIVO')
        """, (
            tipo, marca, modelo, numero_serie,
            service_tag, tombamento, especificacoes,
            locado, setor, responsavel, observacoes
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("listar_equipamentos"))

    return render_template("cadastrar.html")

@app.route("/excluir/<int:id>")
def excluir(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    
    cursor.execute("DELETE FROM movimentacoes WHERE equipamento_id = ?", (id,))
    cursor.execute("DELETE FROM equipamentos WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("listar_equipamentos"))


@app.route("/excluir_historico/<int:id>")
def excluir_historico(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM movimentacoes WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("historico"))


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":

        tipo = request.form["tipo"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        numero_serie = request.form["numero_serie"]
        service_tag = request.form["service_tag"]
        tombamento = request.form["tombamento"]
        especificacoes = request.form["especificacoes"]
        locado = request.form["locado"]
        setor = request.form["setor"]
        responsavel = request.form["responsavel"]
        observacoes = request.form["observacoes"]

        cursor.execute("""
            UPDATE equipamentos SET
                tipo=?,
                marca=?,
                modelo=?,
                numero_serie=?,
                service_tag=?,
                tombamento=?,
                especificacoes=?,
                locado=?,
                setor=?,
                responsavel=?,
                observacoes=?
            WHERE id=?
        """, (tipo, marca, modelo, numero_serie, service_tag,
              tombamento, especificacoes, locado, setor,
              responsavel, observacoes, id))

        conn.commit()
        conn.close()

        return redirect("/equipamentos")

    cursor.execute("SELECT * FROM equipamentos WHERE id=?", (id,))
    equipamento = cursor.fetchone()
    conn.close()

    return render_template("editar.html", equipamento=equipamento)



if __name__ == "__main__":
    criar_banco()
    app.run(host="0.0.0.0", port=5000, debug=True)