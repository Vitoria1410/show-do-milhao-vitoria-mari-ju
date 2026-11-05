# Comparação da entrega com o enunciado AC04

Referência: documento AC04_Show_Milhão_v1.docx fornecido pela solicitante, relido em 04/11/2026. A análise considera o conteúdo do documento, não apenas a tabela de notas. Estado de execução e implantação: TESTES.md.

## Regras e programa Python — critério de 3,0 pontos

| Requisito do professor | Evidência no projeto | Situação |
|---|---|---|
| Jogo executado em Python; jogo no navegador opcional | jogo.py; menu no terminal e notebook Colab | Implementado; teste humano no Colab pela equipe pendente |
| Apelido não vazio; somente apelidos nos resultados | ler_apelido, strip, resultados por apelido | Teste local aprovado |
| Pelo menos 15 perguntas, 5 de cada nível, quatro alternativas e uma correta | 18 perguntas em database.sql, seis por nível; REVISAO_PERGUNTAS.md | Estrutura e gabaritos revisados; fontes registradas |
| Até nove questões sem repetição, ordem 3 fáceis, 3 médias e 3 difíceis | sortear_perguntas usa random.sample | 100 sorteios no teste local aprovados |
| Valores da tabela, sem somar etapas | PREMIOS e calcular_premio | Teste de todos os dez valores aprovado |
| Erro, desistência ou nove acertos; manter último prêmio | jogar | Cenários locais aprovados |
| Entrada inválida permite corrigir a mesma resposta | while de leitura de resposta | Teste local aprovado |
| Mostrar e salvar resultado uma única vez | jogar retorna um resultado; main salva com UUID; reenvio ignora conflito | Fluxo e reenvio testados; gravação anterior confirmada online |
| Menu jogar, ranking e sair; funções separadas | main, obter_perguntas, jogar, calcular_premio, salvar_partida | Implementado |
| Medir com time.perf_counter sem menu ou envio | cronômetro dentro de jogar | Teste com relógio controlado aprovado |

## Banco e integração — critério de 2,0 pontos

| Requisito | Evidência | Situação |
|---|---|---|
| Mesmo projeto online para Python e site | URL do mesmo Supabase em ambos | Verificado na revisão anterior |
| Tabelas e campos mínimos | jogos, perguntas, partidas em database.sql | Conferido |
| jogo_id; valores e duração numéricos; UUID reaproveitado | dicionário da partida e esquema SQL | Conferido e testado |
| Informar falta de perguntas e falha de conexão | validar_perguntas e tratamento de erros | Testes locais aprovados |
| Nunca confirmar envio malsucedido; guardar resultado e oferecer reenvio | salvar_pendente, sincronizar_pendentes e mensagem após sucesso | Testes locais aprovados; reenvio anterior confirmado online |
| Persistir e reabrir para consultar | banco Supabase, leitura do ranking | Leitura posterior confirmada; reabertura no Colab pela equipe pendente |
| Separar acesso público do acesso de escrita/gabarito | migrações e chave privada somente no ambiente do Python | Chave pública bloqueada em seis operações; leitura de jogos/ranking preservada; envio privado no Colab pendente |

## Ranking web — critério de 1,0 ponto

| Requisito | Evidência | Situação |
|---|---|---|
| Posição, jogo, apelido, prêmio, duração e data | tabela HTML e createRow | Implementado e verificado no navegador na revisão anterior |
| Reais no padrão brasileiro; minutos e segundos | Intl.NumberFormat e duration | Testes locais aprovados |
| Filtro por jogo, botão de atualização, top 10 | loadGames, loadRanking e limit=10 | Testes locais e revisão anterior no navegador |
| Ranking por jogo; melhor partida por apelido | view ranking, duas etapas de ROW_NUMBER | Conferido no SQL |
| Desempates por prêmio, tempo, data e ID | ORDER BY explícito nas duas etapas da view | SQL conferido; dados de teste aprovados em Python |
| Consultar online; mensagens de vazio ou erro | fetch na API; sem fallback para tabela bruta | Testes locais aprovados; API atual confirmada online e build do Pages concluído; nova captura pelo usuário pendente |
| Funcionar com Python fechado | site estático consulta Supabase | Confirmado na revisão anterior; preservar na revisão atual |
| Site somente leitura, sem gabarito ou edição | SELECT apenas em jogos/ranking para chave pública; perguntas/partidas bloqueadas | Confirmado online: jogos/ranking HTTP 200; perguntas e leitura/escrita de partidas negadas |

## Organização e entrega — critério de 1,0 ponto

| Item obrigatório do ZIP | Arquivo ou evidência | Situação |
|---|---|---|
| Todos os arquivos Python e requirements.txt | jogo.py, tests/ e requirements.txt | Incluídos |
| HTML, CSS e JavaScript da versão publicada | index.html, styles.css, app.js, config.js | Incluídos; gerar ZIP do commit publicado |
| SQL de tabelas, ranking e permissões; perguntas com fontes | database.sql, supabase/migrations, REVISAO_PERGUNTAS.md | Incluídos |
| README com nomes, turma, regras, instalação e links | README.md | Incluído com os três nomes informados |
| Configurações sem senhas ou chaves administrativas reais | .env.example; Colab Secrets/getpass; config.js somente chave pública | Verificar também o ZIP final |
| Testes esperados, observados e correções | TESTES.md, tests/, relatório histórico | Incluídos |
| Capturas da mesma partida Python/site | evidencias/jogo_python.jpg e ranking_online.jpg | Capturas reais anteriores em janela Tkinter; novas capturas do Colab após a alteração são recomendadas |
| Link e repositório correspondentes ao ZIP | GitHub Pages e pacote gerado por git archive | Conferir no fechamento do pacote |
| Um ZIP e texto do Moodle | pacote de entrega e MOODLE.txt | Preparar pacote final; envio pelo usuário |
| Dupla e nome Turma_Nome1_Nome2.zip | equipe informada tem três pessoas | Confirmar com o professor; não há conformidade literal com a composição pedida |

## Uso de IA e testes — critério de 1,0 ponto

O arquivo prompts.md inclui prompts reconstruídos, identificados como tal, e pedidos reais disponíveis deste chat. Há objetivos, identificação da ferramenta quando conhecida, arquivos envolvidos, usos e testes. Foram documentados problemas reais e melhorias, incluindo publicação, tratamento de falha, permissões e enunciados das perguntas.

**A exigência de todos os prompts originais em ordem cronológica não está plenamente comprovada.** Reconstruções não demonstram que os textos foram efetivamente enviados. A autoria individual original e os modelos de etapas anteriores também não foram confirmados. Isso permanece uma diferença em relação ao enunciado, mesmo com o arquivo incluído no ZIP.

As fontes e justificativas das perguntas estão registradas em REVISAO_PERGUNTAS.md; a equipe deve conferi-las e conseguir explicar o conteúdo. Os testes executados pelo assistente estão identificados, sem atribuí-los a execução manual das integrantes.

## Domínio individual — critério de 2,0 pontos

Não pode ser validado pelo assistente. Cada integrante deve explicar e modificar uma função de Python durante a apresentação. EXPLICACAO.md oferece uma preparação, mas não substitui a avaliação.

## Conferência final pela equipe

1. Testar uma partida no Colab após configurar SUPABASE_KEY nos Secrets; conferir a confirmação de envio.
2. Atualizar o site e comparar apelido, valor e duração. Capturar as duas telas, sem mostrar a chave.
3. Reexecutar o jogo e consultar o ranking; parar o Python e atualizar o site.
4. Confirmar com o professor os três integrantes e o nome do ZIP.
5. Abrir o ZIP final e conferir os arquivos. Anexar no Moodle, colar os dados de MOODLE.txt e verificar a confirmação do envio.

Esta comparação não atribui nota nem declara concluídos os itens que dependem do professor ou da execução da equipe.
