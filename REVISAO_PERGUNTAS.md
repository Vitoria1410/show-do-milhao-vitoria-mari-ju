# Revisão das perguntas e gabaritos

Revisão assistida por Codex em 04/11/2026. Referências primárias consultadas online; a equipe deve conseguir explicar os conteúdos. Não constitui validação do aprendizado individual.

A numeração abaixo segue a ordem das 18 perguntas em database.sql, e não depende do ID atribuído no banco. Foram mantidas seis perguntas por dificuldade.

| Nº | Dificuldade | Resposta | Justificativa | Fonte |
|---|---|---|---|---|
| 1 | facil | B — print() | print é a função padrão de saída de texto. | [Referência](https://docs.python.org/3/library/functions.html#print) |
| 2 | facil | C — # | O caractere # inicia comentário fora de literais de texto. | [Referência](https://docs.python.org/3/reference/lexical_analysis.html#comments) |
| 3 | facil | C — bool | Comparações como 5 > 2 retornam um booleano. | [Referência](https://docs.python.org/3/library/stdtypes.html#comparisons) |
| 4 | facil | B — Inteligência Artificial | IA é a abreviação em português de inteligência artificial; a referência é o livro Artificial Intelligence: A Modern Approach. | [Referência](https://aima.cs.berkeley.edu/) |
| 5 | facil | D — def | def inicia a definição de uma função. | [Referência](https://docs.python.org/3/reference/compound_stmts.html#function-definitions) |
| 6 | facil | A — Lista (list) | A lista usa colchetes e permite alterar elementos. | [Referência](https://docs.python.org/3/tutorial/datastructures.html) |
| 7 | media | B — A lista é mutável e a tupla é imutável | Listas permitem alterações; tuplas são sequências imutáveis. | [Referência](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range) |
| 8 | media | A — Pandas | O DataFrame do pandas representa dados tabulares. | [Referência](https://pandas.pydata.org/docs/getting_started/intro_tutorials/01_table_oriented.html) |
| 9 | media | B — Ajustar os parâmetros do modelo a partir de exemplos com rótulos conhecidos | Exemplos rotulados orientam o ajuste do modelo supervisionado. | [Referência](https://developers.google.com/machine-learning/intro-to-ml/supervised) |
| 10 | media | C — dict.get() | dict.get retorna um padrão (None se omitido) quando a chave não existe. | [Referência](https://docs.python.org/3/library/stdtypes.html#dict.get) |
| 11 | media | A — Quando o modelo decora os dados de treino e tem baixo desempenho em dados novos | Sobreajuste caracteriza ajuste excessivo ao treino e generalização pior. | [Referência](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html) |
| 12 | media | B — try ... except | try e except estruturam a captura de exceções. | [Referência](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement) |
| 13 | dificil | B — Transformer | O artigo apresenta a arquitetura Transformer baseada em atenção; não afirma ter inventado toda forma de atenção. | [Referência](https://arxiv.org/abs/1706.03762) |
| 14 | dificil | A — Usa a palavra-chave yield e produz valores sob demanda (lazy evaluation) | Uma função com yield pode produzir itens sucessivos sob demanda. | [Referência](https://peps.python.org/pep-0255/) |
| 15 | dificil | B — Garante que apenas uma thread execute bytecode Python por vez em um processo | Com GIL habilitado, uma thread executa bytecode por vez; há compilações free-threaded sem essa restrição. | [Referência](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) |
| 16 | dificil | B — Desvanecimento do gradiente (Vanishing Gradient) | Gradientes que diminuem muito durante a propagação caracterizam vanishing gradient. | [Referência](https://www.deeplearningbook.org/contents/rnn.html) |
| 17 | dificil | C — O(1) | Busca de chave em dict tem custo médio O(1) no CPython, sob as hipóteses usuais de hashing; o pior caso difere. | [Referência](https://wiki.python.org/python/language/TimeComplexity.html) |
| 18 | dificil | A — RAG (Retrieval-Augmented Generation) | RAG combina recuperação de informação e geração condicionada ao contexto recuperado. | [Referência](https://arxiv.org/abs/2005.11401) |

Foram esclarecidos os enunciados de Transformer e GIL, sem mudar as letras dos gabaritos. A migração atualiza perguntas existentes por enunciado, sem apagar perguntas ou partidas. Os exemplos executáveis de Python foram conferidos com o interpretador: print, comentário, comparação booleana, def, lista mutável, tupla imutável, dict.get e yield. As demais respostas foram comparadas às referências acima.
