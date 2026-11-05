"""Janela opcional para demonstrar as funções reais de jogo.py.

O jogo principal continua sendo `python jogo.py`, no terminal.
Esta janela usa tkinter (biblioteca padrão) para registrar uma evidência visual.
Não incorpora nenhuma chave privada; utiliza a chave pública de config.js.
"""
import importlib.util
import io
import json
import os
from pathlib import Path
import queue
import re
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from contextlib import redirect_stdout
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('jogo', BASE / 'jogo.py')
jogo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jogo)
saidas = queue.Queue()
entradas = queue.Queue()
registro = io.StringIO()

class Saida:
    def write(self, texto):
        registro.write(texto)
        saidas.put(texto)
    def flush(self):
        pass

def ler(prompt=''):
    Saida().write(prompt)
    resposta = entradas.get()
    Saida().write(resposta + '\n')
    return resposta

def executar():
    try:
        config = (BASE / 'config.js').read_text(encoding='utf-8')
        os.environ['SUPABASE_KEY'] = re.search(r'anonKey:\s*"([^"]+)"', config).group(1)
        with redirect_stdout(Saida()), patch('builtins.input', side_effect=ler):
            print('DEMONSTRAÇÃO REAL — funções de jogo.py em janela Tkinter')
            print('Partida de teste identificada pelo apelido EVIDENCIA_AC04.')
            print('Dados reais do Supabase; esta janela não é o terminal.')
            db = jogo.Supabase()
            perguntas = jogo.obter_perguntas(db)
            jogo_id = db.buscar_jogo()
            partida = jogo.jogar(perguntas, 'EVIDENCIA_AC04', jogo_id)
            print('Jogo:', jogo.NOME_JOGO)
            db.salvar_partida(partida)
            db.salvar_partida(partida)
            registros = db.requisicao('GET', 'partidas', {'select': 'id', 'id': f'eq.{partida["id"]}'})
            print('Envio confirmado no Supabase.')
            print('UUID:', partida['id'])
            print('Envios do mesmo UUID: 2; registros encontrados:', len(registros))
            pasta = BASE / 'evidencias'
            pasta.mkdir(exist_ok=True)
            (pasta / 'demonstracao_python.txt').write_text(registro.getvalue(), encoding='utf-8')
            (pasta / 'demonstracao_partida.json').write_text(json.dumps(partida, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception as erro:
        Saida().write('\nFalha na demonstração: ' + str(erro) + '\n')

root = tk.Tk()
root.title('Show do Milhão — demonstração real Python')
root.geometry('1000x760')
tk.Label(root, text='Show do Milhão — execução das funções reais de jogo.py', font=('Arial', 16, 'bold')).pack(pady=8)
texto = ScrolledText(root, font=('Consolas', 11), wrap='word', bg='#101d33', fg='#eef4ff')
texto.pack(fill='both', expand=True, padx=10)
barra = tk.Frame(root)
barra.pack(fill='x', padx=10, pady=10)
tk.Label(barra, text='Resposta (A/B/C/D ou X):').pack(side='left')
entrada = tk.Entry(barra, font=('Arial', 13))
entrada.pack(side='left', fill='x', expand=True, padx=8)
def enviar(event=None):
    entradas.put(entrada.get())
    entrada.delete(0, 'end')
entrada.bind('<Return>', enviar)
tk.Button(barra, text='Enviar resposta', command=enviar).pack(side='right')
def atualizar():
    while not saidas.empty():
        texto.insert('end', saidas.get())
        texto.see('end')
    root.after(80, atualizar)
root.after(80, atualizar)
threading.Thread(target=executar, daemon=True).start()
entrada.focus_set()
root.mainloop()
