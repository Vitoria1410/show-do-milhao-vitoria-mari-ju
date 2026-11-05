import importlib.util, io, json, tempfile, unittest
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('jogo', REPO / 'jogo.py')
j = importlib.util.module_from_spec(spec)
spec.loader.exec_module(j)
perguntas = [dict(id=n*6+i, enunciado=f'Pergunta {n}-{i}', alternativa_a='A', alternativa_b='B', alternativa_c='C', alternativa_d='D', correta='A', dificuldade=nivel) for n,nivel in enumerate(j.NIVEIS) for i in range(6)]

class Testes(unittest.TestCase):
    def partida(self, entradas):
        with patch('builtins.input', side_effect=entradas), patch.object(j.time, 'perf_counter', side_effect=[100, 165.25]), redirect_stdout(io.StringIO()):
            return j.jogar(perguntas, 'Teste', 1)
    def test_premios(self):
        self.assertEqual([j.calcular_premio(i) for i in range(10)], [0,1000,5000,10000,25000,50000,100000,200000,500000,1000000])
    def test_nove_acertos(self):
        p=self.partida(['A']*9)
        self.assertEqual((p['acertos'],p['valor_ganho'],p['motivo_encerramento'],p['tempo_segundos']), (9,1000000,'nove_acertos',65.25))
    def test_erro_primeira(self):
        p=self.partida(['B']); self.assertEqual((p['acertos'],p['valor_ganho']), (0,0))
    def test_erro_apos_acertos(self):
        p=self.partida(['A']*4+['B']); self.assertEqual((p['acertos'],p['valor_ganho']), (4,25000))
    def test_desistencia(self):
        p=self.partida(['A']*3+['X']); self.assertEqual((p['valor_ganho'],p['motivo_encerramento']), (10000,'desistencia'))
    def test_entrada_invalida(self):
        p=self.partida(['','E','1',' a ']+['A']*8); self.assertEqual(p['acertos'],9)
    def test_apelido_vazio(self):
        with patch('builtins.input',side_effect=['','  ',' Jogadora ']),redirect_stdout(io.StringIO()): self.assertEqual(j.ler_apelido(),'Jogadora')
    def test_sorteio(self):
        for _ in range(100):
            ps=j.sortear_perguntas(perguntas)
            self.assertEqual(len(set(p['id'] for p in ps)),9)
            self.assertEqual([p['dificuldade'] for p in ps],['facil']*3+['media']*3+['dificil']*3)
    def test_perguntas_insuficientes(self):
        with self.assertRaises(ValueError): j.validar_perguntas(perguntas[:10])
    def test_ranking_desempates(self):
        def p(id,nome,valor,tempo,data='2026-11-04T10:00:00Z'): return dict(id=id,apelido=nome,valor_ganho=valor,tempo_segundos=tempo,data_hora=data)
        dados=[p('1','Ana',1000,20),p('2',' ANA ',5000,30),p('3','Bia',5000,10),p('5','Eva',5000,10),p('4','Dani',5000,10),p('6','Fabi',5000,10,'2026-11-03T10:00:00Z')]
        self.assertEqual([p['id'] for p in j.ordenar_ranking(dados)],['6','3','4','5','2'])
    def test_falha_e_reenvio(self):
        from unittest.mock import Mock
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp,patch.object(j,'ARQUIVO_PENDENTES',Path(tmp)/'pendentes.json'),redirect_stdout(io.StringIO()):
            p=self.partida(['B']); j.salvar_pendente(p); j.salvar_pendente(p)
            self.assertEqual(len(j.carregar_arquivo(j.ARQUIVO_PENDENTES)),1)
            db=Mock(); db.salvar_partida.side_effect=RuntimeError('rede indisponivel')
            j.sincronizar_pendentes(db); self.assertEqual(len(j.carregar_arquivo(j.ARQUIVO_PENDENTES)),1)
            db.salvar_partida.side_effect=None; j.sincronizar_pendentes(db)
            self.assertEqual(j.carregar_arquivo(j.ARQUIVO_PENDENTES),[])
            self.assertEqual(db.salvar_partida.call_args_list[0].args[0]['id'],db.salvar_partida.call_args_list[1].args[0]['id'])
    def test_requisicao_idempotente(self):
        with patch.dict('os.environ',SUPABASE_KEY='teste'):
            db=j.Supabase()
        with patch.object(db,'requisicao') as req:
            db.salvar_partida({'id':'mesmo-id'})
            self.assertEqual(req.call_args.args[2],{'on_conflict':'id'})
            self.assertIn('ignore-duplicates',req.call_args.args[4])

if __name__=='__main__': unittest.main(verbosity=2)

