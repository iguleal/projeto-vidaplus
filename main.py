import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Função para conectar ao banco e criar as tabelas baseadas no DER
def init_db():
    conn = sqlite3.connect('vidaplus.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS PACIENTE 
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT, NOME TEXT, CPF TEXT, TELEFONE TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS MEDICO 
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT, NOME TEXT, CRM TEXT, ESPECIALIDADE TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS CONSULTA 
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT, DATA TEXT, 
                       ID_PACIENTE INTEGER, ID_MEDICO INTEGER,
                       FOREIGN KEY(ID_PACIENTE) REFERENCES PACIENTE(ID),
                       FOREIGN KEY(ID_MEDICO) REFERENCES MEDICO(ID))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS PRONTUARIO 
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT, DESCRICAO TEXT, PRESCRICAO TEXT,
                       ID_CONSULTA INTEGER,
                       FOREIGN KEY(ID_CONSULTA) REFERENCES CONSULTA(ID))''')
    conn.commit()
    conn.close()

init_db()

# Exemplo de Modelo de Dados para Paciente
class Paciente(BaseModel):
    nome: str
    cpf: str
    telefone: str

@app.post("/pacientes")
def cadastrar_paciente(paciente: Paciente):
    conn = sqlite3.connect('vidaplus.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PACIENTE (NOME, CPF, TELEFONE) VALUES (?, ?, ?)", 
                   (paciente.nome, paciente.cpf, paciente.telefone))
    conn.commit()
    conn.close()
    return {"message": "Paciente cadastrado com sucesso!"}

@app.get("/pacientes")
def listar_pacientes():
    conn = sqlite3.connect('vidaplus.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PACIENTE")
    dados = cursor.fetchall()
    conn.close()
    return dados
