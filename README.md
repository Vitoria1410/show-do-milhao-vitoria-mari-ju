# Show do Milhão — Python, Supabase e Ranking Web

Projeto interdisciplinar de desenvolvimento de um jogo de perguntas e respostas inspirado no **Show do Milhão**, executado em Python (Google Colab / PyCharm), com persistência em banco de dados online (**Supabase**) e exibição do ranking em tempo real no **GitHub Pages**.

---

## Identificação da equipe
- Mariana Vincente
- Julia Santana
- Vitória Barreto
- Turma: Primeiro IA A
- Repositório: https://github.com/Vitoria1410/show-do-milhao-vitoria-mari-ju
- Site: https://vitoria1410.github.io/show-do-milhao-vitoria-mari-ju/

O enunciado solicita uma dupla; a equipe informada tem três integrantes. Confirmar essa composição com o professor.

---

## 🎮 Regras do Jogo
1. **Identificação:** Solicita um apelido não vazio antes de iniciar.
2. **Perguntas:** 
   - O banco possui pelo menos 18 perguntas revisadas sobre **Python e Inteligência Artificial** (6 fáceis, 6 médias e 6 difíceis).
   - A partida sorteia **9 perguntas sem repetição**, rigorosamente na ordem: 3 fáceis, 3 médias e 3 difíceis.
3. **Premiação Progressiva (Fictícia):**
   - **Fácil:** 1º acerto: R$ 1.000,00 | 2º acerto: R$ 5.000,00 | 3º acerto: R$ 10.000,00
   - **Média:** 4º acerto: R$ 25.000,00 | 5º acerto: R$ 50.000,00 | 6º acerto: R$ 100.000,00
   - **Difícil:** 7º acerto: R$ 200.000,00 | 8º acerto: R$ 500.000,00 | 9º acerto: R$ 1.000.000,00
   - Os valores **não são somados**; cada acerto substitui o valor anterior pelo prêmio da etapa.
4. **Condições de Término:**
   - **Erro:** Encerra a partida imediatamente e mantém o último prêmio alcançado (ou R$ 0,00 se errar a 1ª).
   - **Desistência:** O jogador pode digitar `X` a qualquer momento para parar e garantir o prêmio acumulado.
   - **Vitória Máxima:** Ao acertar as 9 perguntas, conquista R$ 1.000.000,00.
5. **Cronometragem:** Mede a duração da partida da primeira pergunta ao encerramento com `time.perf_counter()`, desconsiderando o tempo do menu e de envio ao banco.

---

## 🗄️ Estrutura do Banco de Dados (Supabase)
O script de criação completo está no arquivo [`database.sql`](database.sql):
- **`jogos`:** `id`, `nome`
- **`perguntas`:** `id`, `enunciado`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `correta`, `dificuldade`, `fonte`
- **`partidas`:** `id` (UUID único), `jogo_id`, `apelido`, `valor_ganho`, `tempo_segundos`, `acertos`, `motivo_encerramento`, `data_hora`
- **`ranking` (View Oficial):** Agrupa por jogo, seleciona apenas a melhor partida de cada apelido e aplica os critérios de desempate:
  1. Maior valor ganho
  2. Menor tempo em segundos
  3. Data mais antiga
  4. ID da partida

---

## ⚙️ Como Configurar e Executar

### 1. Configurar o Supabase
1. Acesse seu projeto no [Supabase Dashboard](https://supabase.com).
2. Vá em **SQL Editor** > **New Query**.
3. Copie todo o conteúdo do arquivo [`database.sql`](database.sql) e clique em **Run**.
4. Em **Project Settings** > **API**, copie:
   - **Project URL:** `https://mkgbeemjhvpvjmqbwtfl.supabase.co`
   - **anon public key:** Chave pública configurada para este protótipo. Ver a pendência de permissões abaixo.

### 2. Executar o Jogo em Python (`jogo.py`)
O código utiliza apenas a biblioteca padrão do Python (`urllib`, `json`, `time`, etc.), sem necessidade de `pip install`.

**Opção A — No Computador (Terminal ou PyCharm):**
```bash
python jogo.py
```
Quando solicitado, informe a chave pública do Supabase (ou configure a variável de ambiente `SUPABASE_KEY`).

**Opção B — No Google Colab:**
Na primeira célula do Colab:
```python
import os
os.environ["SUPABASE_URL"] = "https://mkgbeemjhvpvjmqbwtfl.supabase.co"
os.environ["SUPABASE_KEY"] = "sua_chave_anon_aqui"
```
E na célula seguinte, execute o conteúdo de [`jogo.py`](jogo.py).

### 3. Executar e Publicar o Site no GitHub Pages
1. No arquivo [`config.js`](config.js), insira sua chave `anonKey` (ou insira diretamente pelo botão ⚙️ no site).
2. No repositório do GitHub:
   - Vá em **Settings** > **Pages**.
   - Em **Build and deployment > Source**, selecione `Deploy from a branch`.
   - Escolha a branch `main` (ou `master`) e a pasta `/ (root)`.
   - Clique em **Save**. O site estará disponível em minutos!

---

## 📂 Arquivos do Repositório
- [`jogo.py`](jogo.py): Código-fonte completo do jogo em Python.
- [`requirements.txt`](requirements.txt): Documentação das dependências (bibliotecas nativas).
- [`database.sql`](database.sql): Script SQL com tabelas, RLS, View de ranking e 18 perguntas revisadas.
- [`index.html`](index.html), [`styles.css`](styles.css), [`app.js`](app.js), [`config.js`](config.js): Código do site de ranking web.
- [`prompts.md`](prompts.md): Registro cronológico de todos os prompts de IA, testes e correções.
- [`.env.example`](.env.example): Exemplo seguro de variáveis de ambiente sem segredos expostos.


## Verificações reais e pendências

Leia TESTES.md. Os testes locais exercitam entradas simuladas e não substituem a apresentação individual. A integração foi consultada no Supabase real; uma partida automática TESTE_AC04, com prêmio zero, foi enviada duas vezes com o mesmo UUID e permaneceu com um único registro. Seu tempo de 0,00s decorre da entrada automática e não representa uma partida humana.

**Permissões pendentes:** a chave pública atual consegue consultar os gabaritos e inserir partidas. Isso contraria a exigência de acesso do site somente à leitura do ranking. A equipe optou por manter a configuração nesta revisão. O site só efetua consultas, mas isso não impede o uso da chave fora dele. Não apresentar a segurança como requisito concluído. A correção requer separar o acesso de escrita/leitura de perguntas do Python do acesso público ao ranking, com orientação do professor. Nunca colocar chave administrativa no frontend ou no ZIP.

**Histórico de IA pendente:** os prompts reais anteriores a este chat não foram recuperados. prompts.md distingue a transcrição disponível de exemplos simulados e não garante a completude do histórico do projeto.

**Evidências:** os registros automatizados estão em evidencias/. Capturas da mesma partida no terminal e no site ainda devem ser conferidas, conforme TESTES.md. Não confundir saídas em texto com capturas de tela.

## Rodar os testes locais

Na raiz do projeto, com Python 3 instalado:

```sh
python -m unittest discover -s tests -p "test_*.py" -v
```

O teste JavaScript usa Node.js, opcional para validar o site:

```sh
node tests/testar_site.cjs
```

Os testes automatizados usam entradas e rede simuladas, exceto o teste de integração identificado em TESTES.md. Eles não inserem partidas ao rodar a suíte local.

## Configuração local

O arquivo .env.example é um modelo e não é carregado automaticamente. No PowerShell, defina as variáveis da sessão antes de executar o jogo:

```powershell
$env:SUPABASE_URL = "https://SEU-PROJETO.supabase.co"
$env:SUPABASE_KEY = "SUA_CHAVE_DE_CLIENTE_PERMITIDA"
python jogo.py
```

Alternativamente, informe a chave pública quando o jogo solicitar. Nunca compartilhe uma chave privada na gravação ou na apresentação.

## Apresentação individual

Cada integrante precisa conseguir explicar e modificar uma função. Estudem calcular_premio e os índices da lista, sortear_perguntas e random.sample, jogar e suas condições de parada, além de salvar_partida e a reutilização do UUID. A avaliação de domínio individual depende da apresentação e não pode ser comprovada por estes testes.
