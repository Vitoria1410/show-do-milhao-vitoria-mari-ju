# Testes da revisão de permissões

Data: 04/11/2026 (America/Sao_Paulo). Executor: Codex, a pedido da equipe.

## Testes locais

- 18 testes Python aprovados: regras, prêmios, sorteio, entradas, encerramento, ranking, pendências, idempotência, cabeçalhos de chaves modernas/legadas e ocultação de credenciais em erro.
- Três dos 18 testes Python executam a consulta SQL real da view em SQLite em memória: separação por jogo e melhor apelido, desempates e top 10 após classificar mais de mil partidas. Esses testes validam a lógica SQL comum e não substituem a verificação das permissões no PostgreSQL.
- 9 testes JavaScript aprovados: formatação, renderização como texto, estado vazio, rede indisponível, filtro/top 10, erro ao listar jogos, ausência de consulta à tabela bruta, cabeçalho moderno e rejeição de chaves administrativas no site.
- Exemplos Python das perguntas revisadas executados com sucesso; fontes e justificativas das 18 perguntas estão em REVISAO_PERGUNTAS.md.
- Notebook Colab validado estruturalmente, sem saídas nem credenciais. Execução pela equipe no Colab ainda não confirmada.

## Alterações verificadas no código

- Python lê a chave privada do ambiente ou solicita com getpass, sem ecoar o valor.
- Chaves sb_secret e sb_publishable são enviadas somente em apikey; tokens legados também usam Authorization.
- Site consulta somente jogos e ranking; não tenta ler partidas se a view falhar.
- Python consulta a view ranking para evitar limitar partidas brutas antes de selecionar a melhor de cada apelido.
- SQL revoga acesso público às perguntas e partidas, mantém leitura pública de jogos/ranking e preserva acesso privado do Python.
- Migrações não apagam perguntas ou partidas. O script completo não contém mais DELETE de perguntas.

## Verificação online desta revisão

A integração Supabase no GitHub concluiu com status success para o commit 8bb2cbafc3f7fd1139b0a8638f9061356f7d4ddb. O GitHub Pages também concluiu o build dessa versão. Os testes reais com a chave pública retornaram:

| Operação | Esperado | Observado |
|---|---|---|
| Ler jogos | Permitido | HTTP 200 |
| Ler ranking do jogo 1 | Permitido | HTTP 200, resultados existentes preservados |
| Ler perguntas e gabaritos | Negado | HTTP 401, permission denied for table perguntas |
| Ler tabela bruta de partidas | Negado | HTTP 401, permission denied for table partidas |
| Inserir partida | Negado | HTTP 401, permission denied for table partidas |
| Inserir jogo | Negado | HTTP 401, permission denied for table jogos |
| Alterar partida | Negado | HTTP 401, permission denied for table partidas |
| Excluir partida | Negado | HTTP 401, permission denied for table partidas |

As tentativas de inserir usaram corpo vazio. As tentativas de alterar/excluir usaram um UUID inexistente, sem tocar resultados reais. Os oito testes passaram. Evidência: evidencias/permissoes_publicas.json. HTTP 401 e 403 são aceitos como bloqueio; neste projeto o PostgREST retornou 401 com mensagem explícita de falta de permissão.

O envio usando a chave privada não foi executado pelo assistente nesta revisão, porque nenhuma credencial privada foi recebida. A equipe fará a confirmação no Colab. Os testes locais validaram a composição dos cabeçalhos e o fluxo de salvamento com credenciais fictícias, sem atribuir a isso uma gravação privada real.

A ferramenta de controle do navegador foi interrompida porque não conseguiu determinar a URL atual no Windows com confiança suficiente para aplicar sua política. Nenhuma nova interação visual foi tentada depois desse bloqueio. A atualização foi verificada por consultas HTTP e build do Pages; a nova captura visual ficará a cargo da execução da equipe. As capturas anteriores permanecem identificadas como históricas.

## Evidências históricas reais

Antes da alteração de permissões foram confirmados: 18 perguntas, envio repetido do mesmo UUID com apenas um registro, ranking no navegador e atualização após fechar o Python. A partida EVIDENCIA_AC04 teve R$ 0,00, duração de 47,07s e apareceu no site como 0min 47s. Capturas e dados estão em evidencias/. O relatório histórico está em evidencias/TESTES_REVISAO_ANTERIOR.md.

Essas evidências históricas não comprovam, por si só, o envio privado após a mudança de permissões. A equipe fará essa confirmação no Colab.

## Pendências não resolvidas por testes automatizados

- Confirmar uma partida no Colab com a chave privada, comparar no site e guardar novas capturas.
- Confirmar com o professor a equipe de três integrantes, pois o enunciado solicita dupla.
- Reconstruções de prompts não comprovam o histórico original completo.
- Demonstrar domínio individual e realizar o envio no Moodle.
