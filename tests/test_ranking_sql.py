"""Executa a consulta da view em SQLite, sem depender de credenciais.

Valida a lógica SQL comum de janelas; não simula as permissões do PostgreSQL.
"""
from pathlib import Path
import re
import sqlite3
import unittest

class TestesRankingSQL(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:')
        self.db.row_factory=sqlite3.Row
        self.db.executescript('''CREATE TABLE jogos(id INTEGER PRIMARY KEY,nome TEXT);
        CREATE TABLE partidas(id TEXT PRIMARY KEY,jogo_id INTEGER,apelido TEXT,valor_ganho NUMERIC,tempo_segundos NUMERIC,data_hora TEXT);
        INSERT INTO jogos VALUES(1,'Jogo A'),(2,'Jogo B');''')
        sql=(Path(__file__).resolve().parents[1]/'database.sql').read_text(encoding='utf-8-sig')
        view=re.search(r'CREATE OR REPLACE VIEW public\.ranking AS.*?FROM partidas_filtradas;',sql,re.S).group()
        self.db.executescript(view.replace('CREATE OR REPLACE VIEW','CREATE VIEW').replace('public.',''))
        self.addCleanup(self.db.close)
    def inserir(self,id,apelido,valor,tempo,jogo=1,data='2026-11-04T12:00:00Z'):
        self.db.execute('INSERT INTO partidas VALUES(?,?,?,?,?,?)',(id,jogo,apelido,valor,tempo,data))
    def ranking(self,jogo):
        return self.db.execute('SELECT * FROM ranking WHERE jogo_id=? ORDER BY posicao LIMIT 10',(jogo,)).fetchall()
    def test_jogos_separados_e_melhor_apelido(self):
        self.inserir('1','Ana',1000,20)
        self.inserir('2',' ANA ',5000,30)
        self.inserir('3','Ana',1000000,10,jogo=2)
        self.assertEqual([r['partida_id'] for r in self.ranking(1)],['2'])
        self.assertEqual([r['partida_id'] for r in self.ranking(2)],['3'])
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM partidas').fetchone()[0],3)
    def test_desempate_por_tempo_data_e_id(self):
        self.inserir('1','Lento',5000,30)
        self.inserir('4','D',5000,10)
        self.inserir('3','C',5000,10)
        self.inserir('5','Antigo',5000,10,data='2026-11-03T12:00:00Z')
        self.inserir('6','Maior prêmio',10000,60)
        self.assertEqual([r['partida_id'] for r in self.ranking(1)],['6','5','3','4','1'])
    def test_top_dez_apos_classificacao(self):
        for i in range(1050): self.inserir(str(i),'Jogador'+str(i),1000,i+1)
        self.inserir('recorde','Recordista',1000000,50)
        rows=self.ranking(1)
        self.assertEqual(len(rows),10)
        self.assertEqual(rows[0]['apelido'],'Recordista')
        self.assertEqual([r['posicao'] for r in rows],list(range(1,11)))

if __name__=='__main__':unittest.main(verbosity=2)
