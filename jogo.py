# -*- coding: utf-8 -*-
"""Show do Milhão — Python e IA

Jogo de perguntas e respostas integrado com banco Supabase e ranking web.
Recursos implementados (consulte TESTES.md para pendências):
- Mínimo de 15 perguntas (5 fáceis, 5 médias, 5 difíceis)
- Sorteio de 9 perguntas (3 de cada nível)
- Prêmios progressivos até R$ 1.000.000,00
- Medição com time.perf_counter()
- Persistência com UUID e prevenção de duplicidade
- Armazenamento de partidas pendentes em caso de falha de conexão
"""

import json
import os
import random
import time
import uuid
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError


# =====================================================
# CONFIGURAÇÕES
# =====================================================

NOME_JOGO = "Show do Milhão - Python e IA"

NIVEIS = ["facil", "media", "dificil"]

PREMIOS = [
    1000, 5000, 10000,
    25000, 50000, 100000,
    200000, 500000, 1000000
]

# Compatível com Google Colab e ambiente local
PASTA = Path.cwd()

ARQUIVO_RANKING = PASTA / "ranking_local.json"
ARQUIVO_PENDENTES = PASTA / "partidas_pendentes.json"


# =====================================================
# CONEXÃO COM SUPABASE
# =====================================================

class Supabase:

    def __init__(self):
        # Permite carregar das variáveis de ambiente ou usar o ID padrão do projeto
        self.url = os.getenv("SUPABASE_URL", "https://mkgbeemjhvpvjmqbwtfl.supabase.co").strip().rstrip("/")
        self.key = os.getenv("SUPABASE_KEY", "").strip()

        if not self.url or not self.key:
            raise ValueError(
                "Configure a chave do Supabase!\n"
                "Defina a variável SUPABASE_KEY com a chave pública permitida pelas políticas do protótipo do seu projeto."
            )

        if not self.url.startswith("https://"):
            raise ValueError("A URL do Supabase é inválida.")

    def requisicao(
        self,
        metodo,
        tabela,
        parametros=None,
        dados=None,
        preferencia=None
    ):
        url = f"{self.url}/rest/v1/{tabela}"

        if parametros:
            url += "?" + urlencode(parametros)

        cabecalhos = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if preferencia:
            cabecalhos["Prefer"] = preferencia

        corpo = None

        if dados is not None:
            corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")

        requisicao = Request(
            url,
            data=corpo,
            headers=cabecalhos,
            method=metodo
        )

        try:
            with urlopen(requisicao, timeout=15) as resposta:
                conteudo = resposta.read().decode("utf-8")
                if conteudo:
                    return json.loads(conteudo)
                return None

        except HTTPError as erro:
            detalhe = erro.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Erro HTTP {erro.code}: {detalhe}")

        except (URLError, TimeoutError, OSError) as erro:
            raise RuntimeError(f"Falha de conexão: {erro}")

    def testar_conexao(self):
        self.requisicao(
            "GET",
            "jogos",
            {"select": "id", "limit": "1"}
        )

    def buscar_jogo(self):
        jogos = self.requisicao(
            "GET",
            "jogos",
            {
                "select": "id,nome",
                "nome": f"eq.{NOME_JOGO}"
            }
        ) or []

        if jogos:
            return jogos[0]["id"]

        novos = self.requisicao(
            "POST",
            "jogos",
            dados={"nome": NOME_JOGO},
            preferencia="return=representation"
        ) or []

        if novos:
            return novos[0]["id"]

        raise RuntimeError("Não foi possível localizar ou cadastrar o jogo.")

    def buscar_perguntas(self):
        return self.requisicao(
            "GET",
            "perguntas",
            {
                "select": (
                    "id,enunciado,alternativa_a,"
                    "alternativa_b,alternativa_c,"
                    "alternativa_d,correta,dificuldade"
                ),
                "order": "id.asc"
            }
        ) or []

    def salvar_partida(self, partida):
        self.requisicao(
            "POST",
            "partidas",
            {"on_conflict": "id"},
            partida,
            "resolution=ignore-duplicates,return=minimal"
        )

    def buscar_ranking(self, jogo_id):
        return self.requisicao(
            "GET",
            "partidas",
            {
                "select": (
                    "id,jogo_id,apelido,valor_ganho,"
                    "tempo_segundos,acertos,data_hora"
                ),
                "jogo_id": f"eq.{jogo_id}"
            }
        ) or []


# =====================================================
# ARQUIVOS LOCAIS (PERSISTÊNCIA E PENDÊNCIAS)
# =====================================================

def carregar_arquivo(caminho):
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        if isinstance(dados, list):
            return dados
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return []


def salvar_arquivo(caminho, dados):
    temporario = caminho.with_name(caminho.name + ".tmp")
    temporario.write_text(
        json.dumps(dados, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )
    temporario.replace(caminho)


def salvar_ranking_local(partida):
    ranking = carregar_arquivo(ARQUIVO_RANKING)
    ranking = [p for p in ranking if p.get("id") != partida["id"]]
    ranking.append(partida)
    salvar_arquivo(ARQUIVO_RANKING, ranking)


def salvar_pendente(partida):
    pendentes = carregar_arquivo(ARQUIVO_PENDENTES)
    if not any(p.get("id") == partida["id"] for p in pendentes):
        pendentes.append(partida)
    salvar_arquivo(ARQUIVO_PENDENTES, pendentes)


def remover_pendente(id_partida):
    pendentes = carregar_arquivo(ARQUIVO_PENDENTES)
    pendentes = [p for p in pendentes if p.get("id") != id_partida]
    salvar_arquivo(ARQUIVO_PENDENTES, pendentes)


# =====================================================
# FORMATAÇÃO E VALIDAÇÃO
# =====================================================

def dinheiro(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def ler_apelido():
    while True:
        apelido = input("\nDigite seu apelido: ").strip()
        if apelido:
            return apelido[:30]
        print("O apelido não pode ficar vazio! Tente novamente.")


def calcular_premio(acertos):
    if acertos == 0:
        return 0
    return PREMIOS[acertos - 1]


def validar_perguntas(perguntas):
    for nivel in NIVEIS:
        quantidade = sum(
            1 for p in perguntas
            if str(p.get("dificuldade", "")).lower() == nivel
        )
        if quantidade < 5:
            raise ValueError(
                f"São necessárias pelo menos 5 perguntas de nível {nivel}. "
                f"Encontradas: {quantidade}."
            )

    campos = [
        "enunciado",
        "alternativa_a",
        "alternativa_b",
        "alternativa_c",
        "alternativa_d",
        "correta",
        "dificuldade"
    ]

    for pergunta in perguntas:
        for campo in campos:
            if not pergunta.get(campo):
                raise ValueError(f"Pergunta incompleta no campo: {campo}.")

        if str(pergunta["correta"]).strip().upper() not in ("A", "B", "C", "D"):
            raise ValueError("Existe uma pergunta com gabarito inválido no banco.")


def obter_perguntas(db):
    print("\nConsultando banco de perguntas online no Supabase...")
    perguntas = db.buscar_perguntas()

    if not perguntas:
        raise ValueError("Nenhuma pergunta encontrada no Supabase.")

    validar_perguntas(perguntas)
    print(f"Sucesso: {len(perguntas)} perguntas válidas carregadas!")
    return perguntas


# =====================================================
# SORTEIO DE 9 PERGUNTAS (3 de cada nível)
# =====================================================

def sortear_perguntas(perguntas):
    sorteadas = []
    for nivel in NIVEIS:
        grupo = [
            p for p in perguntas
            if str(p["dificuldade"]).lower() == nivel
        ]
        if len(grupo) < 3:
            raise ValueError(f"Perguntas insuficientes no nível {nivel}.")
        sorteadas.extend(random.sample(grupo, 3))
    return sorteadas


# =====================================================
# EXECUÇÃO DA PARTIDA
# =====================================================

def jogar(perguntas, apelido, jogo_id):
    sorteadas = sortear_perguntas(perguntas)

    acertos = 0
    motivo = "nove_acertos"

    print("\n" + "=" * 55)
    print("             SHOW DO MILHÃO")
    print("=" * 55)
    print(f"\nBoa sorte, {apelido}!")
    print("Digite X caso queira desistir e parar com o prêmio atual.")

    # Medição exata da partida (time.perf_counter)
    inicio = time.perf_counter()

    for numero, pergunta in enumerate(sorteadas, start=1):
        print("\n" + "=" * 55)
        print(f"PERGUNTA {numero}/9 — DIFICULDADE: {pergunta['dificuldade'].upper()}")
        print(f"VALOR DESTA ETAPA: {dinheiro(PREMIOS[numero - 1])}")
        print(f"PRÊMIO GARANTIDO: {dinheiro(calcular_premio(acertos))}")

        print("\n" + pergunta["enunciado"])
        print("A)", pergunta["alternativa_a"])
        print("B)", pergunta["alternativa_b"])
        print("C)", pergunta["alternativa_c"])
        print("D)", pergunta["alternativa_d"])

        while True:
            resposta = input("\nSua resposta [A/B/C/D ou X para parar]: ").strip().upper()
            if resposta in ("A", "B", "C", "D", "X"):
                break
            print("Entrada inválida! Digite apenas A, B, C, D ou X.")

        if resposta == "X":
            motivo = "desistencia"
            print("\nVocê optou por parar e garantiu seu prêmio acumulado.")
            break

        correta = str(pergunta["correta"]).strip().upper()

        if resposta != correta:
            motivo = "resposta_errada"
            print("\nQue pena! Você errou!")
            print(f"A resposta correta era a alternativa ({correta}).")
            break

        acertos += 1
        print("\nCERTA RESPOSTA! PARABÉNS!")
        print(f"Você acumulou: {dinheiro(calcular_premio(acertos))}")

    duracao = round(time.perf_counter() - inicio, 2)

    partida = {
        "id": str(uuid.uuid4()),
        "jogo_id": jogo_id,
        "apelido": apelido,
        "valor_ganho": calcular_premio(acertos),
        "tempo_segundos": duracao,
        "acertos": acertos,
        "motivo_encerramento": motivo,
        "data_hora": datetime.now(timezone.utc).isoformat()
    }

    print("\n" + "=" * 55)
    print("                 FIM DE JOGO!")
    print("=" * 55)
    print(f"Jogador: {apelido}")
    print(f"Acertos: {acertos}/9")
    print(f"Prêmio Final: {dinheiro(partida['valor_ganho'])}")
    print(f"Tempo da partida: {duracao}s")

    return partida


# =====================================================
# RANKING (ORDENAÇÃO E DESEMPATE EXATO)
# =====================================================

def ordenar_ranking(partidas):
    # Regra: Maior valor -> Menor tempo -> Data mais antiga -> ID
    partidas.sort(
        key=lambda p: (
            -int(p["valor_ganho"]),
            float(p["tempo_segundos"]),
            p["data_hora"],
            p["id"]
        )
    )

    melhores = {}
    for partida in partidas:
        apelido_chave = partida["apelido"].strip().casefold()
        if apelido_chave not in melhores:
            melhores[apelido_chave] = partida

    return list(melhores.values())[:10]


def consultar_ranking(db, jogo_id):
    print("\nConsultando ranking online no Supabase...")
    partidas = db.buscar_ranking(jogo_id)

    melhores = ordenar_ranking(partidas)

    print("\n" + "=" * 60)
    print("          TOP 10 — RANKING SHOW DO MILHÃO")
    print("=" * 60)

    if not melhores:
        print("Ainda não existem partidas registradas para este jogo.")
        return

    for posicao, jogador in enumerate(melhores, start=1):
        tempo = int(float(jogador["tempo_segundos"]))
        minutos = tempo // 60
        segundos = tempo % 60

        print(f"\n{posicao}º LUGAR — {jogador['apelido']}")
        print(f"  Prêmio: {dinheiro(int(jogador['valor_ganho']))}")
        print(f"  Tempo:  {minutos}min {segundos:02d}s ({jogador['tempo_segundos']}s)")
        print(f"  Data:   {jogador['data_hora'][:10]}")
        print("-" * 45)


# =====================================================
# SINCRONIZAÇÃO DE PARTIDAS PENDENTES
# =====================================================

def sincronizar_pendentes(db):
    pendentes = carregar_arquivo(ARQUIVO_PENDENTES)

    if not pendentes:
        print("\nNenhuma partida pendente de sincronização.")
        return

    print(f"\nTentando sincronizar {len(pendentes)} partida(s) pendente(s)...")

    sucessos = 0
    for partida in list(pendentes):
        try:
            db.salvar_partida(partida)
            remover_pendente(partida["id"])
            sucessos += 1
            print(f"✓ Partida de {partida['apelido']} ({dinheiro(partida['valor_ganho'])}) enviada!")
        except RuntimeError as erro:
            print(f"✗ Falha ao enviar partida de {partida['apelido']}: {erro}")
            print("As partidas restantes permanecerão no arquivo para nova tentativa.")
            break

    print(f"Sincronização concluída: {sucessos} enviada(s).")


# =====================================================
# MENU PRINCIPAL
# =====================================================

def main():
    print("\n" + "=" * 55)
    print("       SHOW DO MILHÃO — PYTHON E IA")
    print("=" * 55)

    # Permite informar a chave caso não esteja em variável de ambiente
    if not os.getenv("SUPABASE_KEY"):
        chave = input("Digite a chave pública do Supabase: ").strip()
        if chave:
            os.environ["SUPABASE_KEY"] = chave

    try:
        db = Supabase()
        print("\nTestando conexão com o Supabase...")
        db.testar_conexao()
        print("Conexão online estabelecida com sucesso!")

        jogo_id = db.buscar_jogo()
        print(f"Jogo identificado no banco (ID: {jogo_id})!")

    except (ValueError, RuntimeError) as erro:
        print("\n[ERRO DE CONEXÃO]")
        print(erro)
        return

    # Ao abrir, sincroniza pendentes se houver
    sincronizar_pendentes(db)

    while True:
        print("\n" + "=" * 40)
        print("            MENU")
        print("=" * 40)
        print("1 - Iniciar nova partida")
        print("2 - Consultar ranking (Top 10)")
        print("3 - Sincronizar partidas pendentes")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            try:
                perguntas = obter_perguntas(db)
                apelido = ler_apelido()
                partida = jogar(perguntas, apelido, jogo_id)

                # 1. Salva localmente primeiro
                salvar_ranking_local(partida)
                salvar_pendente(partida)

                # 2. Tenta enviar ao Supabase
                try:
                    db.salvar_partida(partida)
                    remover_pendente(partida["id"])
                    print("\n✓ Partida registrada no Supabase com sucesso!")
                except RuntimeError as erro:
                    print("\n[AVISO DE CONEXÃO]")
                    print(f"Falha ao enviar para o banco: {erro}")
                    print("A partida foi salva localmente e poderá ser reenviada pela opção 3.")

            except (RuntimeError, ValueError, OSError) as erro:
                print(f"\nNão foi possível concluir a partida: {erro}")

        elif opcao == "2":
            try:
                consultar_ranking(db, jogo_id)
            except RuntimeError as erro:
                print(f"\nErro ao consultar ranking: {erro}")

        elif opcao == "3":
            sincronizar_pendentes(db)

        elif opcao == "0":
            print("\nObrigado por jogar o Show do Milhão! Até a próxima.")
            break

        else:
            print("\nOpção inválida! Escolha 1, 2, 3 ou 0.")


if __name__ == "__main__":
    main()
