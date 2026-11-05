# Registro de testes e evidências

Data: 04/11/2026, America/Sao_Paulo. Executor: assistente Codex, a pedido da equipe. Entradas de jogo e rede nos testes locais são simuladas. Não atribuir estes testes à execução manual das integrantes.

## Python — 12 testes aprovados

| Caso | Resultado esperado | Observado |
|---|---|---|
| Tabela de prêmios | 0; 1.000; 5.000; 10.000; 25.000; 50.000; 100.000; 200.000; 500.000; 1.000.000, sem soma | Igual à tabela |
| Nove acertos | 9 acertos, R$ 1.000.000,00, motivo nove_acertos | Aprovado |
| Erro na primeira | 0 acertos, R$ 0,00 | Aprovado |
| Erro após quatro acertos | 4 acertos, R$ 25.000,00 | Aprovado |
| Desistência após três acertos | R$ 10.000,00, motivo desistencia | Aprovado |
| Alternativa inválida | Aceitar nova tentativa sem avançar | Aprovado com vazio, E e 1; normalização de espaços/minúsculas |
| Apelido vazio | Repetir solicitação até valor não vazio | Aprovado |
| Sorteio, 100 execuções | 9 IDs distintos, 3 fáceis + 3 médias + 3 difíceis | Aprovado em todas |
| Perguntas insuficientes | Informar erro, sem iniciar partida | ValueError esperado |
| Ranking local | Maior prêmio, menor tempo, data mais antiga, ID; melhor apelido | Aprovado |
| Falha de envio e reenvio local | Manter pendência e mesmo UUID; remover após sucesso | Aprovado com falha de rede simulada |
| Requisição idempotente | on_conflict=id e ignore-duplicates | Aprovado |

O teste de nove acertos também usa relógio controlado e verifica duração de 65,25s. O cronômetro fica dentro de jogar; menu e envio ficam fora. Não se trata de medição de desempenho humano.

## JavaScript — 6 testes aprovados

| Caso | Esperado | Observado |
|---|---|---|
| Formatação | R$ 1.000.000,00; 125 segundos como 2min 05s | Aprovado |
| Ranking alternativo | Desempate e melhor apelido | Aprovado com dados de teste |
| Ranking vazio | Mensagem de ausência de partidas | Aprovado |
| Rede indisponível | Mensagem de falha e botão reativado | Aprovado |
| URL de consulta | Filtro jogo_id e limite 10 | Aprovado |
| Falha na lista de jogos | Mensagem visível de falha | Aprovado após melhoria no aviso principal |

Esses testes usam DOM e fetch simulados em Node.js; não substituem a verificação no navegador publicado.

## Integração real com Supabase

- Consulta de jogos: HTTP 200, jogo Show do Milhão - Python e IA, ID 1.
- Consulta de perguntas: HTTP 200, 18 perguntas completas, 6 por dificuldade. Validação executada por validar_perguntas.
- Consulta de ranking: HTTP 200, registros reais retornados.
- Executada partida com entradas automáticas para errar a primeira questão, apelido TESTE_AC04, R$ 0,00, 0 acertos.
- UUID: 31820a3b-4152-47f5-8cc4-63a07364fadc.
- A mesma partida foi enviada duas vezes por salvar_partida. Consulta pelo UUID retornou exatamente 1 registro.
- A view ranking retornou essa partida na posição 3, após Mari e Vitoria.
- Duração automática registrada: 0,00s; não representa tempo de uma jogadora humana.
- A consulta ao banco ocorreu em processo separado de uma partida interativa. O site consulta o Supabase diretamente e não depende de servidor Python.
- Evidências textuais e dados retornados: evidencias/partida_teste_terminal.txt e evidencias/resultado_online.json. Estes arquivos não são capturas de tela.

## Problemas encontrados e alterações

1. Site: falha ao listar jogos só aparecia no seletor. Adicionado aviso principal e recuperação da lista pelo botão Atualizar quando não há jogo selecionado. Testes JavaScript aprovados após alteração.
2. Documentação: nomes e turma indefinidos. Atualizados conforme informação da solicitante.
3. Histórico de IA: arquivo antigo não podia ser confirmado como histórico real e continha exemplo de prêmio incorreto na desistência. Substituído por mensagens reais disponíveis e simulações identificadas. O teste confirma R$ 10.000,00 após três acertos.
4. .env.example tinha variável de backend Vercel que o jogo não utiliza. Alinhado a SUPABASE_URL e SUPABASE_KEY; não inclui credenciais reais.
5. GitHub Pages estava desativado; o link retornava 404. Pages foi ativado na branch main, pasta raiz. O build concluiu e o site foi aberto no navegador com consulta real ao Supabase.

## Pendências declaradas

- **Permissões do Supabase:** confirmado que a chave pública consulta perguntas com gabarito e insere partidas. Não atende à exigência de somente leitura do ranking. A solicitante preferiu manter a configuração e registrar a pendência. Nenhuma correção de segurança foi aplicada nesta revisão.
- **Histórico de prompts:** não foram disponibilizados os prompts anteriores a este chat. Os exemplos simulados não suprem essa ausência.
- **Equipe:** foram informados três integrantes; o enunciado solicita dupla. Confirmar com o professor.
- **Fontes das perguntas:** existem referências em database.sql, mas a checagem externa individual de todas as 18 fontes e gabaritos não foi realizada nesta sessão. A validação estrutural não comprova revisão conceitual.
- **Domínio individual:** não avaliado; depende de cada integrante explicar e modificar código na apresentação.
- **Evidência de execução:** foram obtidas capturas reais da janela Python de demonstração e do site para a mesma partida EVIDENCIA_AC04. A janela utiliza as funções reais do jogo e Tkinter; não é uma captura do terminal. Se o professor exigir especificamente o terminal, repetir a execução pelo comando python jogo.py e capturá-la.
- **Persistência após reinício:** o registro foi consultado em nova requisição, mas não foi feita uma sessão humana completa de fechar e reabrir o programa.

Não há fundamento para garantir nota máxima. Os testes aprovados comprovam somente os cenários descritos.

## Verificação visual e site com Python fechado

Executada demonstração real pela janela opcional tests/demonstracao_gui.py, que chama as funções de jogo.py. A janela buscou as 18 perguntas online, aceitou corrigir uma entrada inválida e recebeu X para desistir na primeira pergunta.

- Jogo: Show do Milhão - Python e IA.
- Apelido: EVIDENCIA_AC04.
- Valor: R$ 0,00 fictícios; 0 acertos; encerramento por desistência.
- Duração real registrada: 47,07 segundos; site formatou como 0min 47s.
- UUID: 57eecb7b-d8ab-4e30-a944-6788e8e3848e.
- Enviado duas vezes com mesmo UUID; consulta confirmou somente 1 registro.
- Captura real da execução: evidencias/jogo_python.jpg.
- Captura real do site: evidencias/ranking_online.jpg.
- Dados e saída completa: evidencias/demonstracao_partida.json e evidencias/demonstracao_python.txt.

Após encerrar a janela Python, foi confirmado que não havia processo pythonw em execução. O botão Atualizar do site continuou consultando o Supabase e exibiu a mesma partida na posição 4. A captura do ranking foi salva depois desse teste, em 04/11/2026, aproximadamente 21h25, America/Sao_Paulo.

O build inicial validado no GitHub Pages correspondeu ao commit ef2e267fa56564eba3021887048a1383a0bdddd1. A inclusão final destas evidências será publicada no commit de fechamento; o código do site permanece igual ao testado.
