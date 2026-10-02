from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "biblioteca_123"

CAMINHO_BANCO = os.path.join(
    os.path.dirname(__file__),
    "biblioteca.db"
)


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():

    conexao = conectar_banco()

    autores = conexao.execute(
        "SELECT * FROM autores ORDER BY nome"
    ).fetchall()

    categorias = conexao.execute(
        "SELECT * FROM categorias ORDER BY nome"
    ).fetchall()

    if request.method == "POST":

        titulo = request.form["titulo"]
        ano = request.form["ano"]
        isbn = request.form["isbn"]
        autor_id = request.form["autor_id"]
        categoria_id = request.form["categoria_id"]

        try:
            conexao.execute("""
                INSERT INTO livros
                (titulo, ano, isbn, autor_id, categoria_id)
                VALUES (?, ?, ?, ?, ?)
            """, (
                titulo,
                ano,
                isbn,
                autor_id,
                categoria_id
            ))

            conexao.commit()

            flash("Livro cadastrado com sucesso!", "sucesso")

            conexao.close()

            return redirect(url_for("livros"))

        except sqlite3.IntegrityError:
            flash("Erro: este ISBN já está cadastrado.", "erro")

    conexao.close()

    return render_template(
        "cadastrar.html",
        autores=autores,
        categorias=categorias
    )


@app.route("/livros")
def livros():

    conexao = conectar_banco()

    livros = conexao.execute("""
        SELECT
            livros.id,
            livros.titulo,
            livros.ano,
            livros.isbn,
            autores.nome AS autor,
            categorias.nome AS categoria
        FROM livros
        INNER JOIN autores
            ON livros.autor_id = autores.id
        INNER JOIN categorias
            ON livros.categoria_id = categorias.id
        ORDER BY livros.id DESC
    """).fetchall()

    conexao.close()

    return render_template(
        "livros.html",
        livros=livros
    )


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    conexao = conectar_banco()

    if request.method == "POST":

        titulo = request.form["titulo"]
        ano = request.form["ano"]
        isbn = request.form["isbn"]
        autor_id = request.form["autor_id"]
        categoria_id = request.form["categoria_id"]

        try:

            conexao.execute("""
                UPDATE livros
                SET titulo = ?,
                    ano = ?,
                    isbn = ?,
                    autor_id = ?,
                    categoria_id = ?
                WHERE id = ?
            """, (
                titulo,
                ano,
                isbn,
                autor_id,
                categoria_id,
                id
            ))

            conexao.commit()
            conexao.close()

            flash("Livro atualizado com sucesso!", "sucesso")

            return redirect(url_for("livros"))

        except sqlite3.IntegrityError:

            flash("Erro: este ISBN já está cadastrado.", "erro")

    livro = conexao.execute("""
        SELECT *
        FROM livros
        WHERE id = ?
    """, (id,)).fetchone()

    autores = conexao.execute(
        "SELECT * FROM autores ORDER BY nome"
    ).fetchall()

    categorias = conexao.execute(
        "SELECT * FROM categorias ORDER BY nome"
    ).fetchall()

    conexao.close()

    if livro is None:
        return "Livro não encontrado", 404

    return render_template(
        "editar.html",
        livro=livro,
        autores=autores,
        categorias=categorias
    )


@app.route("/excluir/<int:id>")
def excluir(id):

    conexao = conectar_banco()

    conexao.execute("""
        DELETE FROM livros
        WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    flash("Livro excluído com sucesso!", "sucesso")

    return redirect(url_for("livros"))


if __name__ == "__main__":
    app.run(debug=True)