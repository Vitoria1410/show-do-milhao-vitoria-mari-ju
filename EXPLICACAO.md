# Guia para explicar o programa

O jogo roda em Python no terminal. O Supabase guarda perguntas, jogos e partidas. O site HTML/CSS/JavaScript consulta o ranking diretamente no Supabase; por isso não depende do programa Python aberto.

## Funções que a equipe deve conseguir explicar

- `calcular_premio(acertos)`: retorna zero quando não houve acertos; nos demais casos busca `PREMIOS[acertos - 1]`. Subtrai um porque listas começam no índice zero. Não soma os valores.
- `sortear_perguntas(perguntas)`: percorre os níveis na ordem fácil, média e difícil. Filtra as perguntas de cada grupo e usa `random.sample(grupo, 3)` para escolher três sem repetir. A lista final tem nove perguntas.
- `ler_apelido()`: repete a leitura enquanto o texto, após `strip()`, estiver vazio.
- `jogar()`: mostra uma pergunta por vez. Repete apenas a leitura se a alternativa for inválida. `X` encerra por desistência; erro encerra imediatamente; nove acertos completam o jogo. Retorna um dicionário com o resultado.
- `time.perf_counter()`: lê um relógio apropriado para calcular intervalos. Subtrair a leitura inicial da final dá a duração da partida. O menu e o envio ocorrem fora dessa função.
- `Supabase.requisicao()`: monta a URL e os cabeçalhos HTTP, serializa dados em JSON e trata falhas HTTP ou de conexão.
- `salvar_partida()`: envia o mesmo UUID nos reenvios, com conflito pelo campo `id` ignorado. Assim, repetir o envio não cria outra partida.
- `salvar_pendente()` e `sincronizar_pendentes()`: preservam resultados em JSON para tentar novamente sem jogar outra vez. Após confirmação de envio, removem a pendência.
- `ordenar_ranking()`: ordena por prêmio decrescente e depois tempo, data e ID crescentes. Só mantém a primeira, portanto melhor, partida de cada apelido no conjunto consultado para aquele jogo.

## Banco e site

`jogos` identifica cada jogo. `perguntas` contém alternativas e gabarito. `partidas` preserva cada tentativa, ligada por `jogo_id`. A view `ranking` usa `ROW_NUMBER()` primeiro para escolher a melhor tentativa de cada apelido em cada jogo e depois para atribuir a posição.

No site, `loadGames()` busca a lista de jogos. `loadRanking()` busca as dez primeiras posições do jogo selecionado. `createRow()` usa `textContent` para mostrar os apelidos como texto. `Intl.NumberFormat` formata reais e o cálculo da duração divide os segundos por 60.

## Exercícios de preparação individual

1. Explicar por que três acertos valem R$ 10.000,00 e não a soma de 1.000 + 5.000 + 10.000.
2. Mostrar onde mudar uma mensagem de entrada inválida e testar a alteração.
3. Explicar a diferença entre `break`, `return` e uma nova repetição de `while`.
4. Demonstrar por que `random.sample` não escolhe a mesma pergunta duas vezes dentro do grupo.
5. Explicar por que o UUID precisa ser o mesmo no reenvio.
6. Comparar dois jogadores empatados em prêmio e identificar o vencedor pelo tempo.

As permissões públicas foram corrigidas: o navegador lê apenas jogos e ranking. O Python usa uma credencial privada de execução, configurada no ambiente ou nos Secrets do Colab, sem autenticar o jogador. A confirmação de uma partida privada no Colab cabe à equipe. Reconstruções de prompts não comprovam o histórico original completo, e a composição de três integrantes deve ser confirmada com o professor. Consulte TESTES.md e COMPARACAO_ENUNCIADO.md.
