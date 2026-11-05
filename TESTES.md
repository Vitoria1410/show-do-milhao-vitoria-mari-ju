# Testes da revisão de permissões

Data: 04/11/2026 (America/Sao_Paulo). Executor: Codex, a pedido da equipe.

## Testes locais

- 15 testes Python aprovados: regras, prêmios, sorteio, entradas, encerramento, ranking, pendências, idempotência, cabeçalhos de chaves modernas/legadas e ocultação de credenciais em erro.
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

A migração ainda precisa ser confirmada online. O resultado das consultas com a chave pública será acrescentado após a implantação.

## Evidências históricas reais

Antes da alteração de permissões foram confirmados: 18 perguntas, envio repetido do mesmo UUID com apenas um registro, ranking no navegador e atualização após fechar o Python. A partida EVIDENCIA_AC04 teve R$ 0,00, duração de 47,07s e apareceu no site como 0min 47s. Capturas e dados estão em evidencias/. O relatório histórico está em evidencias/TESTES_REVISAO_ANTERIOR.md.

Essas evidências históricas não comprovam, por si só, o envio privado após a mudança de permissões. A equipe fará essa confirmação no Colab.

## Pendências não resolvidas por testes automatizados

- Confirmar uma partida no Colab com a chave privada, comparar no site e guardar novas capturas.
- Confirmar com o professor a equipe de três integrantes, pois o enunciado solicita dupla.
- Reconstruções de prompts não comprovam o histórico original completo.
- Demonstrar domínio individual e realizar o envio no Moodle.
