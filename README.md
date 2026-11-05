# Show do Milhão — Python, Supabase e ranking web

Jogo didático no terminal, com perguntas e resultados no Supabase e ranking estático no GitHub Pages. Os prêmios são fictícios.

## Equipe

- Mariana Vincente
- Julia Santana
- Vitória Barreto
- Turma: Primeiro IA A

O enunciado solicita dupla; a composição de três integrantes deve ser confirmada com o professor.

- Repositório: https://github.com/Vitoria1410/show-do-milhao-vitoria-mari-ju
- Site: https://vitoria1410.github.io/show-do-milhao-vitoria-mari-ju/
- Colab: https://colab.research.google.com/github/Vitoria1410/show-do-milhao-vitoria-mari-ju/blob/main/Jogar_no_Colab.ipynb

## Regras

Informe um apelido não vazio. Cada partida sorteia nove perguntas sem repetição: três fáceis, três médias e três difíceis. O banco inicial contém dezoito perguntas de Python básico, seis por dificuldade, com quatro alternativas e um gabarito por pergunta. Os desafios difíceis combinam listas, funções, dicionários e laços; não exigem conhecimentos de redes neurais.

| Acertos | Prêmio fictício |
|---|---|
| 0 | R$ 0,00 |
| 1 | R$ 1.000,00 |
| 2 | R$ 5.000,00 |
| 3 | R$ 10.000,00 |
| 4 | R$ 25.000,00 |
| 5 | R$ 50.000,00 |
| 6 | R$ 100.000,00 |
| 7 | R$ 200.000,00 |
| 8 | R$ 500.000,00 |
| 9 | R$ 1.000.000,00 |

Cada acerto substitui o valor anterior; não há soma. A partida termina no primeiro erro, por desistência com X ou ao completar nove acertos. O jogador mantém o último prêmio alcançado. Entradas inválidas permitem nova tentativa na mesma questão.

O menu oferece jogar, consultar ranking, sincronizar pendências e sair. O tempo usa time.perf_counter(), excluindo menu e envio. Falhas de envio mantêm uma pendência local. O reenvio reutiliza o mesmo UUID e não deve criar outra partida.

## Banco e permissões

Para um projeto novo, execute database.sql no SQL Editor do Supabase. O arquivo cria jogos, perguntas, partidas, a view ranking e as permissões, além das perguntas com fontes.

Para atualizar o projeto existente, aplique somente os arquivos em supabase/migrations, em ordem. As migrações preservam os resultados existentes. A integração GitHub configurada em main pode aplicá-las automaticamente; a confirmação real de aplicação deve ser consultada em TESTES.md. Caso a integração falhe, execute os mesmos arquivos pelo SQL Editor.

A chave pública de config.js tem acesso somente à lista de jogos e à view ranking. As tabelas perguntas e partidas ficam bloqueadas para anon e authenticated. A view expõe somente os campos do ranking, usando o proprietário para ler os resultados. O acesso privado do Python usa a role service_role, por chave privada em um ambiente controlado. Não há autenticação dos jogadores: eles usam apenas apelidos.

Uma chave Secret ou service_role possui privilégios elevados. Ela não está no repositório, no notebook salvo nem no ZIP. Configure-a apenas no ambiente de execução ou nos Secrets do Colab. Não a use no site nem a compartilhe com o professor em arquivos. As instruções de instalação permitem que cada responsável configure seu próprio projeto.

O ranking seleciona a melhor partida de cada apelido por jogo, ordenando por maior valor, menor tempo, data mais antiga e ID. Depois limita a dez jogadores. O site consulta o Supabase diretamente e funciona com o Python fechado.

## Executar no Colab

1. Abra o link Colab acima ou importe Jogar_no_Colab.ipynb.
2. No seu Supabase, vá a Settings → API Keys. Use a Secret key; se houver somente chaves legadas, use service_role. Não copie essa chave para o chat ou para o JavaScript.
3. No Colab, abra o ícone de chave e adicione um secret chamado SUPABASE_KEY. Cole a chave privada no valor e habilite o acesso do notebook a esse secret.
4. Execute a primeira célula. Ela lê a chave sem exibi-la. Se Secrets não estiver disponível, solicita uma entrada oculta com getpass.
5. Execute a segunda célula. Ela baixa jogo.py do repositório e abre o menu.
6. Jogue usando um apelido de teste, atualize o site e capture o resultado da mesma partida nas duas telas. Não capture a tela dos Secrets.
7. Saia pelo menu, execute novamente e consulte o ranking. Interrompa o Python e atualize o site para verificar a persistência e a independência do ranking.

O notebook distribuído não contém células executadas ou credenciais. A execução real no Colab pela equipe ainda precisa ser confirmada em TESTES.md.

## Executar no computador

Requer Python 3 e acesso à internet. O jogo usa somente a biblioteca padrão; requirements.txt não exige pacotes externos.

```sh
python jogo.py
```

Sem variável de ambiente, o jogo solicita a chave privada com entrada oculta. Também aceita SUPABASE_KEY, SUPABASE_SECRET_KEY ou SUPABASE_SERVICE_ROLE_KEY no ambiente; nunca coloque seus valores reais em arquivos da entrega. A URL pode ser alterada por SUPABASE_URL.

.env.example contém apenas nomes e valores de exemplo. Ele não é carregado automaticamente.

## Testes e evidências

```sh
python -m unittest discover -s tests -p "test_*.py" -v
node tests/testar_site.cjs
```

Node.js é necessário somente para os testes JavaScript, não para jogar ou abrir o site. TESTES.md registra resultados observados e limites. COMPARACAO_ENUNCIADO.md compara os requisitos do documento do professor. REVISAO_PERGUNTAS.md contém fontes e justificativas dos gabaritos.

evidencias/ contém capturas reais da mesma partida e os respectivos dados. A captura Python anterior foi obtida na janela opcional tests/demonstracao_gui.py, que executa as funções de jogo.py; não é uma captura do terminal ou do Colab. Essa janela agora também requer a chave privada no ambiente. O teste no Colab deverá produzir evidências da execução atual após a alteração de permissões.

## Registro de IA e apresentação

prompts.md reúne reconstruções identificadas e pedidos reais disponíveis deste chat. Reconstruções não comprovam um histórico original completo; essa limitação permanece declarada. Não há credenciais privadas nos prompts.

EXPLICACAO.md ajuda a estudar as funções. Cada integrante deve explicar e modificar código Python na avaliação individual; os testes automatizados não comprovam esse domínio.

## Entrega

O ZIP deve conter a mesma versão publicada no repositório, incluindo código Python, requirements.txt, código do site, SQL, perguntas com gabaritos e fontes, prompts.md, README, testes e evidências. O arquivo MOODLE.txt contém o texto de identificação e links. Confirme a composição da equipe e o nome do arquivo com o professor, porque o enunciado prevê dois integrantes.

Os links não substituem o ZIP. O envio e a confirmação final no Moodle são realizados pela equipe.
