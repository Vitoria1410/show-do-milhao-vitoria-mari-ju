# Prompts reconstruídos a partir das funcionalidades do projeto

Data de elaboração deste documento: 04/11/2026.

## Declaração sobre este registro

Este documento reúne prompts reconstruídos a partir das funcionalidades do Show do Milhão, com auxílio do Codex. Os textos descrevem pedidos compatíveis com a implementação e servem para explicar o processo de desenvolvimento. São reconstruções posteriores, e não transcrições confirmadas dos pedidos originais. A sequência segue as etapas lógicas do projeto.

O documento distingue reconstruções, pedidos reais deste chat e verificações efetivamente realizadas. As reconstruções não comprovam o histórico completo exigido no enunciado. Datas de envio, autoria individual e ferramentas originais só são atribuídas quando confirmadas.

A identificação da equipe consta no README. Não foi atribuída a nenhuma integrante a autoria dos exemplos; dados pessoais foram omitidos deste registro de prompts.

## Exemplo 1 — Planejamento do jogo

- Natureza: prompt reconstruído, sem confirmação de envio original.
- Data de elaboração do exemplo: 04/11/2026. Data de envio original: desconhecida.
- Integrante responsável pelo envio: não identificado.
- Ferramenta de elaboração deste exemplo: Codex. Ferramenta/modelo do desenvolvimento original: desconhecidos.
- Objetivo proposto: organizar regras, funções e fluxo do programa.
- Uso efetivo da resposta a este exemplo: nenhum; este pedido não foi executado como uma nova etapa de implementação.
- Arquivos/funções a que se refere: `jogo.py`, `main`, `jogar`, `calcular_premio`, `sortear_perguntas`.
- Verificação proposta: comparar o planejamento com o enunciado e conferir todos os valores dos prêmios.

### Texto completo do prompt reconstruído

```text
Preciso planejar um jogo inspirado no Show do Milhão para um trabalho de Python. O jogo principal será executado no terminal e terá um menu com iniciar partida, consultar ranking e sair. Organize o programa em funções simples que uma pessoa iniciante consiga explicar.

Antes de começar, solicite um apelido não vazio. O banco terá pelo menos 15 perguntas: 5 fáceis, 5 médias e 5 difíceis. Cada pergunta terá quatro alternativas e apenas uma correta. Cada partida deverá sortear 9 perguntas sem repetição, nesta ordem: 3 fáceis, 3 médias e 3 difíceis.

Os prêmios após cada acerto serão 1000, 5000, 10000, 25000, 50000, 100000, 200000, 500000 e 1000000 reais fictícios. Cada valor substitui o anterior; não some os prêmios. A partida termina no primeiro erro, por desistência ou após nove acertos. O jogador mantém o último prêmio alcançado; sem acertos, recebe zero.

Descreva o fluxo do menu, as funções necessárias e os campos que deverão ser salvos. Explique onde usar listas, dicionários, condições e repetições. Diferencie o jogo Python, o banco online e o site que exibirá o ranking.
```

## Exemplo 2 — Implementação das regras em Python

- Natureza: prompt reconstruído, sem confirmação de envio original.
- Data de elaboração do exemplo: 04/11/2026. Data de envio original: desconhecida.
- Integrante responsável pelo envio: não identificado.
- Ferramenta de elaboração deste exemplo: Codex. Ferramenta/modelo original: desconhecidos.
- Objetivo proposto: implementar a partida com validações e cronômetro.
- Uso efetivo da resposta a este exemplo: nenhum; o exemplo foi documentado, sem gerar uma nova implementação do jogo.
- Arquivos/funções a que se refere: `jogo.py`, `ler_apelido`, `validar_perguntas`, `sortear_perguntas`, `jogar`, `calcular_premio`.
- Verificações propostas: nove acertos, erro na primeira, erro após alguns acertos, desistência, apelido vazio, alternativa inválida e sorteio sem repetição.

### Texto completo do prompt reconstruído

```text
Implemente as regras do Show do Milhão em Python, usando funções claras e bibliotecas padrão. Receba as perguntas como uma lista de dicionários para separar a lógica da partida da conexão com o banco.

Crie uma função para validar se existem pelo menos cinco perguntas por dificuldade e se cada pergunta contém enunciado, quatro alternativas e gabarito válido. Sorteie três perguntas de cada dificuldade com random.sample, mantendo a ordem fácil, média e difícil.

Crie uma função calcular_premio(acertos) que retorne zero para nenhum acerto e o valor correspondente da lista de prêmios para os demais casos. Não some os valores das etapas.

Na leitura das alternativas, aceite A, B, C e D, desconsiderando espaços e diferenças entre letras maiúsculas e minúsculas. Aceite X para desistir. Se a entrada for inválida, solicite outra resposta para a mesma pergunta. Se o jogador errar, encerre imediatamente e mantenha o prêmio já conquistado.

Meça a duração da primeira pergunta até o encerramento com time.perf_counter(), excluindo o menu e o envio ao banco. Ao terminar, mostre um resumo e retorne um dicionário com UUID, jogo_id, apelido, valor_ganho, tempo_segundos, acertos, motivo_encerramento e data_hora. Explique o código para que eu consiga modificá-lo durante uma apresentação.
```

## Exemplo 3 — Banco online e perguntas

- Natureza: prompt reconstruído, sem confirmação de envio original.
- Data de elaboração do exemplo: 04/11/2026. Data de envio original: desconhecida.
- Integrante responsável pelo envio: não identificado.
- Ferramenta de elaboração deste exemplo: Codex. Ferramenta/modelo original: desconhecidos.
- Objetivo proposto: modelar tabelas, elaborar perguntas e planejar permissões.
- Uso efetivo da resposta a este exemplo: nenhum; nenhuma alteração de banco decorre deste documento.
- Arquivos a que se refere: `database.sql` e `.env.example`.
- Verificações propostas: estrutura das tabelas, distribuição por dificuldade, revisão conceitual dos gabaritos e tentativa de acesso com credencial pública.

### Texto completo do prompt reconstruído

```text
Prepare um script SQL para um projeto Supabase de um Show do Milhão em Python. Crie as tabelas jogos, perguntas e partidas. Jogos deve ter id e nome. Perguntas deve ter id, enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, correta e dificuldade. Inclua também um campo fonte para registrar a referência usada na revisão.

Partidas deve ter id UUID único, jogo_id como referência a jogos, apelido, valor_ganho numérico, tempo_segundos numérico, acertos, motivo_encerramento e data_hora. Todas as partidas devem ser preservadas, mesmo quando um jogador conseguir uma pontuação melhor depois.

Sugira 18 perguntas sobre Python e inteligência artificial, seis por dificuldade, cada uma com quatro alternativas e uma única correta. Para cada pergunta, informe o gabarito, uma justificativa curta e uma fonte verificável. Não declare que as fontes foram conferidas se isso não ocorreu.

Planeje separadamente o acesso do jogo Python e o acesso do site. A chave pública usada no navegador deverá permitir somente a leitura das informações necessárias ao ranking e à lista de jogos, sem consultar gabaritos nem inserir, atualizar ou excluir partidas. Não inclua credenciais reais no SQL, no JavaScript ou nos exemplos. Explique quais configurações precisam ser aplicadas e verificadas no Supabase para essa separação funcionar.
```

## Exemplo 4 — Integração e reenvio sem duplicação

- Natureza: prompt reconstruído, sem confirmação de envio original.
- Data de elaboração do exemplo: 04/11/2026. Data de envio original: desconhecida.
- Integrante responsável pelo envio: não identificado.
- Ferramenta de elaboração deste exemplo: Codex. Ferramenta/modelo original: desconhecidos.
- Objetivo proposto: buscar perguntas e salvar resultados com tratamento de falhas.
- Uso efetivo da resposta a este exemplo: nenhum; a integração existente não foi reescrita por este pedido reconstruído.
- Arquivos/funções a que se refere: `jogo.py`, `Supabase.requisicao`, `buscar_perguntas`, `salvar_partida`, `salvar_pendente`, `sincronizar_pendentes`.
- Verificações propostas: indisponibilidade de rede, preservação da pendência, reenvio do mesmo UUID e consulta para confirmar um único registro.

### Texto completo do prompt reconstruído

```text
Conecte o jogo Python à API REST do Supabase usando urllib.request e json. Busque perguntas no banco online e salve os resultados na tabela partidas. Carregue a configuração do ambiente, sem colocar senhas ou chaves privadas no código distribuído.

Trate erros HTTP, tempo limite e falha de conexão. Nunca mostre uma confirmação de salvamento antes de receber uma resposta de sucesso do serviço.

Gere o UUID uma única vez para cada partida e reutilize esse mesmo identificador em todas as tentativas de envio. Implemente a gravação de modo que reenviar o mesmo resultado não crie uma segunda partida.

Se o envio falhar, mantenha o resultado disponível durante a execução e ofereça uma opção de tentar novamente sem obrigar a pessoa a repetir o jogo. Se usar um arquivo local de pendências, explique quando ele é atualizado e quando o resultado pode ser removido dele. Mantenha a falha de conexão separada das regras da partida.

Mostre como testar uma falha seguida de recuperação e como consultar o banco para verificar que há somente um registro com aquele UUID. Não descreva resultados de teste como confirmados sem executá-los.
```

## Exemplo 5 — Site do ranking no GitHub Pages

- Natureza: prompt reconstruído, sem confirmação de envio original.
- Data de elaboração do exemplo: 04/11/2026. Data de envio original: desconhecida.
- Integrante responsável pelo envio: não identificado.
- Ferramenta de elaboração deste exemplo: Codex. Ferramenta/modelo original: desconhecidos.
- Objetivo proposto: criar uma página estática ligada aos resultados reais do banco.
- Uso efetivo da resposta a este exemplo: nenhum; o site publicado já existia e este texto não comprova como ele foi criado.
- Arquivos a que se refere: `index.html`, `styles.css`, `app.js`, `config.js` e a view `ranking` em `database.sql`.
- Verificações propostas: link público, atualização, filtro, formatação, empates, estado vazio e funcionamento com o Python fechado.

### Texto completo do prompt reconstruído

```text
Crie um site estático de ranking para o projeto Show do Milhão, com HTML, CSS e JavaScript, compatível com o GitHub Pages. Use um visual inspirado em um programa de perguntas, com fundo azul, destaques amarelos e uma tabela legível. O jogo principal roda em Python; esta página será somente para consultar o ranking.

Consulte dados reais do mesmo projeto Supabase usado pelo jogo. Não use jogadores fixos no HTML nem uma imagem para simular o ranking. O site deve continuar funcionando com o programa Python fechado.

Mostre posição, nome do jogo, apelido, valor ganho, tempo da partida e data. Formate dinheiro fictício como R$ 1.000.000,00 e duração em minutos e segundos. Inclua filtro por jogo, botão Atualizar, indicação de carregamento e mensagens para ranking vazio ou falha de consulta.

Exiba os dez primeiros jogadores do jogo selecionado, considerando somente a melhor partida de cada apelido naquele jogo. Ordene por maior prêmio, menor tempo, data mais antiga e ID da partida. Essa mesma ordem deve ser usada para selecionar a melhor tentativa de cada jogador. Não misture os rankings de jogos diferentes.

Use somente uma chave pública com permissões restritas ao ranking. Não inclua chaves administrativas nem acesso aos gabaritos. Mostre apelidos com textContent, sem interpretá-los como HTML. Explique como publicar a pasta raiz da branch main no GitHub Pages e como comparar uma partida salva no Python com o resultado mostrado na página.
```

## Exemplo 6 — Correção e refinamento do site

- Natureza: prompt reconstruído, sem confirmação de envio original.
- Data de elaboração do exemplo: 04/11/2026. Data de envio original: desconhecida.
- Integrante responsável pelo envio: não identificado.
- Ferramenta de elaboração deste exemplo: Codex. Ferramenta/modelo original: desconhecidos.
- Objetivo proposto: tornar falhas de carregamento compreensíveis e permitir recuperação.
- Uso efetivo da resposta a este exemplo: nenhum. Uma melhoria desse tipo foi realizada na revisão real, mas esse texto não é apresentado como o pedido histórico que a gerou.
- Arquivos/funções a que se refere: `app.js`, `loadGames`, `loadRanking`, `init` e tratamento do botão Atualizar.
- Verificações propostas: interromper a consulta inicial, observar o aviso e tentar carregar novamente depois da recuperação da conexão.

### Texto completo do prompt reconstruído

```text
Revise o tratamento de falhas do site de ranking. Se a lista de jogos não puder ser carregada, mostre um aviso claro na área principal, além do texto no seletor. Não deixe o usuário apenas com uma tabela vazia ou uma mensagem permanente de carregamento.

Faça o botão Atualizar tentar carregar novamente a lista de jogos quando não houver um jogo selecionado. Quando houver um jogo válido, o botão deve atualizar o ranking desse jogo. Reative o botão ao terminar uma consulta que falhou e não mostre dados antigos como se fossem uma atualização bem-sucedida.

Teste a consulta com sucesso, ranking vazio, falha de rede e recuperação. Registre o que foi executado e diferencie testes com rede simulada da consulta real ao Supabase. Preserve as regras de desempate e não exponha detalhes de credenciais nas mensagens.
```

## Exemplo 7 — Testes e preparação da entrega

- Natureza: prompt reconstruído, sem confirmação de envio original.
- Data de elaboração do exemplo: 04/11/2026. Data de envio original: desconhecida.
- Integrante responsável pelo envio: não identificado.
- Ferramenta de elaboração deste exemplo: Codex. Ferramenta/modelo original: desconhecidos.
- Objetivo proposto: confrontar a versão final com os requisitos e organizar as evidências.
- Uso efetivo da resposta a este exemplo: nenhum; os resultados reais da revisão anterior estão documentados separadamente em `TESTES.md` no projeto.
- Arquivos a que se refere: `README.md`, `TESTES.md`, `requirements.txt`, `.env.example`, pasta `tests/`, pasta `evidencias/` e pacote ZIP.
- Verificações propostas: abrir o ZIP, executar o código extraído, conferir o commit e testar o site publicado.

### Texto completo do prompt reconstruído

```text
Compare o projeto Show do Milhão com as instruções da atividade AC04 e prepare um registro honesto de testes. Confira nove acertos com prêmio máximo sem soma, erro na primeira questão, erro depois de alguns acertos, desistência, apelido vazio, alternativa inválida e sorteio sem repetição na ordem das dificuldades.

Teste salvamento no banco, falha de conexão, preservação do resultado e reenvio sem duplicação. Confira o ranking por jogo, a melhor partida por apelido e os desempates por prêmio, tempo, data e ID. Diferencie o que foi testado localmente, o que foi consultado online e o que não pôde ser verificado.

Registre resultados esperados, resultados observados e correções. Obtenha capturas reais do jogo Python e do site para a mesma partida, identificando jogo, apelido, prêmio fictício e duração. Não fabrique capturas, histórico de prompts ou resultados de testes.

Organize um ZIP com os arquivos Python, requirements.txt, HTML, CSS, JavaScript, script SQL, perguntas com gabaritos e fontes, registro de IA, README e evidências. Não inclua arquivos .env reais nem chaves administrativas. Confira se a versão do repositório corresponde à entregue e se o link público funciona com o Python fechado. Aponte qualquer requisito ainda pendente, sem garantir uma nota que dependa da avaliação do professor.
```

## Problemas reais identificados na revisão disponível

Esta seção é distinta dos prompts reconstruídos. Refere-se à revisão efetivamente realizada em 04/11/2026 e registrada nos arquivos do projeto.

1. **Publicação:** o GitHub Pages estava desativado e o link retornava 404. Foi ativado; a página foi aberta e atualizada com consulta real ao Supabase.
2. **Aviso de falha do site:** a falha ao listar jogos não atualizava o aviso principal. Foi acrescentada uma mensagem e o botão Atualizar passou a tentar carregar a lista novamente quando necessário. O teste JavaScript correspondente passou.
3. **Documentação de prêmios:** um relato antigo de exemplo indicava R$ 25.000,00 para desistência na quarta pergunta após três acertos. O valor correto é R$ 10.000,00. O teste da regra confirmou esse valor.
4. **Permissões:** na primeira revisão, a chave pública acessava gabaritos e inseria partidas. Após o pedido real de correção, foram aplicadas migrações pelo GitHub. Consultas reais passaram a negar perguntas e escrita/leitura de partidas para a chave pública, mantendo jogos e ranking disponíveis. Os resultados estão em TESTES.md. A execução privada no Colab ainda deve ser confirmada pela equipe.
5. **Organização do registro de IA:** as reconstruções foram separadas dos pedidos reais deste chat e dos resultados de testes. Essa distinção permite avaliar o documento sem atribuir a exemplos a condição de registro histórico confirmado.

## Testes reais disponíveis no projeto

Na revisão anterior à elaboração deste documento, foram executados 12 testes locais de Python e 6 de JavaScript, todos aprovados nos cenários descritos em `TESTES.md`. Também foram realizadas consultas ao Supabase, envio repetido do mesmo UUID sem duplicação e captura de uma partida real no Python e no site. Esses testes não foram produzidos por executar os prompts reconstruídos acima.

## Perguntas, gabaritos e fontes

O script `database.sql` contém 18 perguntas, com gabaritos e referências. Na revisão final, as respostas foram comparadas a fontes primárias consultadas online e os exemplos Python foram executados. As justificativas, fontes e dois esclarecimentos de enunciado estão em REVISAO_PERGUNTAS.md. A equipe deve conferir e compreender o conteúdo para a apresentação.

## Sugestão de declaração ao professor

“Este documento apresenta prompts reconstruídos a partir das funcionalidades do projeto, acompanhados de pedidos reais deste chat e resultados de testes. As reconstruções explicam possíveis orientações de desenvolvimento e não são apresentadas como transcrições confirmadas do histórico original.”
## Pedidos reais deste chat

Os textos abaixo são transcrições de pedidos efetivamente enviados neste chat em 04/11/2026. Responsável: integrante solicitante, sem autoria individual confirmada. Ferramenta: Codex; modelo exato não confirmado. São pedidos de revisão do projeto, sem atribuição de autoria da implementação inicial.

### Pedido real 1 — Leitura dos requisitos

```text
é isso, le as instruçõe
```

Objetivo: ler o enunciado da atividade. Uso da resposta: requisitos usados como referência para a revisão. Arquivo envolvido: documento AC04 fornecido pela solicitante. Teste: não se aplica à leitura; os testes posteriores constam em TESTES.md.

### Pedido real 2 — Conferência da entrega

```text
pois confira, tenho q enviar até as 23
```

Objetivo: conferir o repositório contra os requisitos antes do prazo informado. Uso da resposta: inspeção do código e identificação de pendências. Arquivos envolvidos: jogo.py, app.js, database.sql, README.md e prompts.md. Verificação: revisão estática seguida dos testes locais e online descritos em TESTES.md.

### Pedido real 3 — Referência ao enunciado

```text
mas lê o arquivo q o professor passou com as instruções
```

Objetivo: reforçar que a avaliação deveria seguir o documento fornecido. Uso da resposta: requisitos do documento mantidos como referência da conferência. Arquivos envolvidos: enunciado AC04 e documentação do projeto. Teste específico: não se aplica; pedido de leitura e interpretação.

### Pedido real 4 — Correspondência da versão e funcionamento online

```text
O repositório deve conter o código da versão entregue. O site deve abrir pelo link e consultar o ranking online, mesmo com o programa Python fechado. Os links complementam o ZIP e não substituem o anexo.
```

Objetivo: reforçar a correspondência entre repositório, site e pacote. Uso da resposta: ativação do GitHub Pages e geração do ZIP a partir do commit publicado. Arquivos envolvidos: site estático, README.md, TESTES.md e evidências. Teste realizado: abertura do site publicado, atualização do ranking após encerrar a janela Python e conferência do conteúdo do ZIP.

Este recorte documenta os pedidos acima; não declara abranger todos os pedidos realizados durante o projeto.


## Pedido real desta revisão — permissões, ZIP e Colab

- Data: 04/11/2026.
- Responsável: integrante solicitante; autoria individual não confirmada.
- Ferramenta: Codex; modelo exato não confirmado.
- Objetivo: corrigir permissões, atualizar o ZIP e comparar com o enunciado.
- Arquivos envolvidos: jogo.py, app.js, database.sql, supabase/migrations, Jogar_no_Colab.ipynb, README.md, TESTES.md e COMPARACAO_ENUNCIADO.md.
- Uso da resposta: preparação de migrações sem exclusão de dados, separação de credenciais e notebook sem chave incorporada.
- Testes: resultados locais e de implantação registrados em TESTES.md. Não foi atribuída execução no Colab ao assistente.

Texto integral do pedido:

```text
vamo mudar a permissao do supabase ent, pega o prompts.md e ja coloca no zip e ja confere e compara se ta igual oque o professor pede nno arquivo,  vou testar o jogo no google colab
```

Autorização real subsequente:

```text
faz isso, eu te dou permissao
```

Na revisão anterior, a solicitante havia escolhido manter as permissões e registrar a pendência. O pedido acima substitui essa escolha. A descrição anterior é histórica; o estado atual da implantação está em TESTES.md.

Resultado real desta revisão: 18 testes Python e 9 JavaScript aprovados; oito consultas de permissões aprovadas online. Migrações e build do GitHub Pages concluídos. Nenhuma chave privada foi inserida nos arquivos ou fornecida ao assistente.
