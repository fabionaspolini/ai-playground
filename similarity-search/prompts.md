## Atualizar tabela comparativa do README.md

```
Analise todos os arquivos com o prefixo "similarity_", eles possuem ao final os resultados comentados no formato de rankde 1 a 9. Os resultado úteis, estão com o marcado "<----- Útil (rank)".

Todos os casos de testes são iguais, 9  itens numa base de conhecido, e 3 testes comparando frases, apenas o método de similaridade de cada arquivo que é diferente.

Você deve montar uma tabela no arquivo @file:README.md exibindo  o rank de cada algoritmo, e ao final montar uma conclusão de qual se saiu melhor.
```

## Criar

```
Agora vamos criar um novo script chamado "similarity_tests.py".

Esse script servirá para facilitar testes comparativos gerais. Analise os arquivos informados, e crie esse novo algoritmo de "similarity_tests.py" baseado em tudo que é feito nos outros.

Agrupe código duplicado em rotinas para reuso.

Ao final, o novo algoritimo deve ser capaz de gerar a mesma bateria de testes para todos os algoritimos, e com modelo `SentenceTransformer` diferentes.

Teste com BM25 é o único estático, os demais arquivos dependem de embeddins gerados, e cada modelo gera um resultado diferente.
Use os modelos para gera os testes:
- `sentence-transformers/all-MiniLM-L6-v2`
- `paraphrase-multilingual-MiniLM-L12-v2`
- `neuralmind/bert-base-portuguese-cased`
- `BAAI/bge-m3`

INPUT: Retire as frases de `base_conhecimento` e da query do usuário de dentro do arquivo python, e crie um arquivo `dataset_credenciais.json`.
O dataset deve ter a lista de base de conhecimento, uma lista de queries do usuário e um lista para indicar as respostas consideradas úteis. 

O script "similarity_tests.py" deve ter uma variavél com o nome do dataset de input para processar.

OUTPUT:
Ao término da comparação, deve ser gerado um arquivo markdown com o resultado do teste.
O nome do arquivo deve ser igual ao dataset, mas com sugixo "_result" e extensão ".md".

No arquivo deve ter uma tabela no onde:
- Linhas são os modelos e algoritimos (uma coluna pra cada informação).
- Colunas são as queries.
- O valores são os rank de cada resposta útil (concatene o rank separando por vígula. Exemplo: 1, 3, 5, 6).
- Deve ser adicionada uma ultima coluna, com a média dos rank úteis. 
- Coluna indicando o tempo de processamento total das queries.
- Criar colunas para indicar consumo de CPU e memória médio para processar as queries.

Geração de estatísticas:
- A contabilização de tempo, uso de cpu e memória atual, deve ser apenas da parte que executar a query. 
```