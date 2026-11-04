# Registro de Prompts de Inteligência Artificial

Este documento atende às exigências do projeto acadêmico do **Show do Milhão**, contendo os prompts enviados em ordem cronológica, a identificação dos integrantes, ferramentas utilizadas, objetivo, análise crítica do código gerado, limitações encontradas e correções aplicadas.

---

## Integrantes da Dupla
- **Integrante 1:** Mariana Souza / Mariana (ou nome completo)
- **Integrante 2:** Vitória / Juliana (ou nome completo)
- **Turma:** [Inserir Turma]
- **Disciplina:** Programação em Python / Banco de Dados

---

## Registro Cronológico de Prompts

### Prompt 1 — Estruturação do Jogo em Python e Regras de Negócio
- **Data:** [Inserir Data, ex: 03/11/2026]
- **Integrante Responsável:** Integrante 1
- **Ferramenta / Modelo:** Google Gemini / ChatGPT
- **Objetivo:** Criar a estrutura inicial do jogo do Show do Milhão em Python com suporte a 9 perguntas divididas em 3 níveis de dificuldade (fácil, média, difícil), pontuação progressiva sem soma de valores e encerramento por erro, desistência ou vitória.
- **Texto Completo do Prompt:**
> "Crie um jogo do Show do Milhão em Python utilizando apenas bibliotecas nativas. O jogo deve conter um menu inicial, solicitar um apelido não vazio, sortear 9 perguntas sem repetição (sendo 3 fáceis, 3 médias e 3 difíceis), calcular prêmios progressivos de R$ 1.000 até R$ 1.000.000 sem somar etapas anteriores, permitir desistência digitando X e medir a duração da partida com time.perf_counter()."
- **Arquivos/Funções Envolvidos:** `jogo.py` (`jogar`, `sortear_perguntas`, `calcular_premio`, `ler_apelido`).
- **Como a resposta foi utilizada/modificada:** A IA sugeriu usar `time.time()`, mas alteramos para `time.perf_counter()` conforme exigido no edital para maior precisão de cronometragem. Também foi adicionada a verificação rigorosa de letras maiúsculas e minúsculas com `.strip().upper()`.
- **Problema/Limitação encontrada e correção:** O código inicial somava os prêmios a cada acerto. Corrigimos a função `calcular_premio(acertos)` para indexar a lista `PREMIOS[acertos - 1]`, retornando o valor fixo acumulado daquela etapa e R$ 0,00 caso não haja acertos.
- **Teste realizado:** Partida iniciada, erro proposital na primeira questão (resultado conferido: R$ 0,00); desistência na 4ª pergunta (resultado conferido: R$ 25.000,00 mantidos).

---

### Prompt 2 — Integração com Supabase via API REST Nativa e Tratamento de Falhas
- **Data:** [Inserir Data, ex: 04/11/2026]
- **Integrante Responsável:** Integrante 2
- **Ferramenta / Modelo:** Google Antigravity / Gemini
- **Objetivo:** Conectar o script Python ao Supabase sem depender de pacotes externos do pip, implementar gravação com UUID e sincronização em caso de falha de conexão.
- **Texto Completo do Prompt:**
> "Como conectar o jogo em Python ao Supabase sem instalar pacotes externos, usando apenas urllib.request? Preciso consultar perguntas, verificar se o jogo existe na tabela jogos, cadastrar se não existir, salvar a partida com UUID único evitando duplicidade, e salvar num arquivo local se a conexão cair para sincronizar depois."
- **Arquivos/Funções Envolvidos:** `jogo.py` (`class Supabase`, `salvar_pendente`, `sincronizar_pendentes`).
- **Como a resposta foi utilizada/modificada:** Adotada a classe `Supabase` que realiza requisições HTTP REST com os cabeçalhos `apikey`, `Authorization` e `Prefer: resolution=ignore-duplicates`. Criamos as funções de gravação local em `partidas_pendentes.json`.
- **Problema/Limitação encontrada e correção:** Quando a requisição POST falhava no Supabase por instabilidade de rede, o programa travava com exceção não tratada e o jogador perdia a partida. Implementamos o bloco `try/except (URLError, TimeoutError, OSError)` que mantém a partida no arquivo `partidas_pendentes.json` e avisa o jogador que seus pontos estão salvos e podem ser sincronizados pelo menu (opção 3).
- **Teste realizado:** Simulação de rede desconectada ao término da partida. O jogo informou a falha, gravou no arquivo JSON e, ao restabelecer a conexão e acionar o menu 3, a partida foi enviada com sucesso ao banco sem duplicar.

---

### Prompt 3 — Modelagem do Banco de Dados e View de Ranking com Critérios de Desempate
- **Data:** [Inserir Data, ex: 04/11/2026]
- **Integrante Responsável:** Integrante 1 e Integrante 2
- **Ferramenta / Modelo:** Antigravity / Gemini
- **Objetivo:** Criar o script SQL para tabelas `jogos`, `perguntas`, `partidas` e a view `ranking` com a regra exata de desempate e 1 melhor partida por apelido.
- **Texto Completo do Prompt:**
> "Gere um script SQL para PostgreSQL/Supabase com as tabelas perguntas, jogos e partidas. Crie uma view de ranking que agrupe por jogo_id, filtre apenas a melhor partida de cada apelido (sem repetir o mesmo jogador no ranking) e ordene por: 1º maior valor_ganho, 2º menor tempo_segundos, 3º data_hora mais antiga e 4º id da partida. Inclua também 18 perguntas sobre Python e IA com 4 alternativas, uma correta e fontes."
- **Arquivos/Funções Envolvidos:** `database.sql` (`CREATE VIEW public.ranking`).
- **Como a resposta foi utilizada/modificada:** Usamos Common Table Expressions (`WITH melhor_partida_por_jogador AS (...)`) e a função analítica `ROW_NUMBER() OVER (PARTITION BY p.jogo_id, LOWER(TRIM(p.apelido)) ORDER BY valor_ganho DESC, tempo_segundos ASC, data_hora ASC, p.id ASC)`.
- **Problema/Limitação encontrada e correção:** Um mesmo jogador que jogasse várias vezes estava aparecendo múltiplas vezes no ranking. Corrigimos adicionando a partição por `LOWER(TRIM(p.apelido))` e filtrando `rn = 1`, garantindo que apenas o melhor recorde de cada apelido seja listado.
- **Teste realizado:** Inserção de duas partidas para o mesmo apelido 'MARI' com tempos e valores diferentes. A view exibiu apenas a partida de maior valor ganho.

---

### Prompt 4 — Criação do Site de Ranking Web Compatível com GitHub Pages
- **Data:** [Inserir Data, ex: 04/11/2026]
- **Integrante Responsável:** Integrante 2
- **Ferramenta / Modelo:** Antigravity / Gemini
- **Objetivo:** Construir a interface web estática (HTML, CSS e JavaScript puro) para ser hospedada no GitHub Pages, com filtro por jogo, formatação em R$ e minutos/segundos.
- **Texto Completo do Prompt:**
> "Crie a página web de ranking em HTML, CSS e JS compatível com GitHub Pages (sem backend Node/Vercel). O site deve consultar a API do Supabase diretamente pelo browser usando a anon key, permitir selecionar o jogo através de um select, listar as colunas Posição, Jogo, Apelido, Prêmio, Tempo e Data, formatar moedas em pt-BR e tempos em minutos e segundos, com layout temático do Show do Milhão."
- **Arquivos/Funções Envolvidos:** `index.html`, `styles.css`, `app.js`, `config.js`.
- **Como a resposta foi utilizada/modificada:** Integrado suporte nativo ao Supabase REST API e fallback resiliente caso a view ainda não esteja criada no banco.
- **Problema/Limitação encontrada e correção:** O código anterior do repositório dependia de uma rota serverless da Vercel (`/api/ranking`), o que resultava em erro 404 ao hospedar no GitHub Pages. Foi refatorado para consulta direta pelo cliente usando a chave pública `anon`.
- **Teste realizado:** Abertura local no navegador e teste de requisição HTTP para a API REST do Supabase.
