# Relatório de Testes de Similaridade

**Dataset:** dataset_investimentos.json

**Queries testadas:** 5


## Resultados Detalhados


Os valores por query, são os **ranks** de onde cada resposta útil foi calculada pelo algoritmo.

| Modelo | Algoritmo | Query 1 | Query 2 | Query 3 | Query 4 | Query 5 | Rank Médio | Tempo Total (s) | Tempo Médio (s) |
|--------|-----------|--------|--------|--------|--------|--------|-----------|-----------------|-----------------|
| N/A (lexical) | BM25 | 3, 4, 7, 12, 13, 26, 45, 82, 94, 100 | 1, 8, 20, 29, 48, 73, 78, 80, 81, 99 | 1, 7, 29, 35, 36, 46, 49, 60, 66, 86 | 1, 2, 3, 4, 5, 8, 24, 32, 50, 55 | 1, 2, 7, 12, 17, 32, 44, 69, 91, 94 | **37.42** | 0.001 | 0.000 |
| sentence-transformers/all-MiniLM-L6-v2 | Cosine Similarity | 1, 2, 4, 5, 20, 64, 69, 83, 89, 92 | 1, 3, 16, 30, 54, 58, 59, 72, 84, 88 | 1, 8, 15, 16, 35, 45, 57, 68, 91, 99 | 1, 2, 3, 4, 14, 19, 26, 61, 69, 80 | 1, 2, 11, 12, 14, 15, 32, 49, 56, 76 | **37.52** | 0.041 | 0.008 |
| sentence-transformers/all-MiniLM-L6-v2 | FAISS Cosine | 1, 2, 4, 5, 20, 64, 69, 83, 89, 92 | 1, 3, 16, 30, 54, 58, 59, 72, 84, 88 | 1, 8, 15, 16, 35, 45, 57, 68, 91, 99 | 1, 2, 3, 4, 14, 19, 26, 61, 69, 80 | 1, 2, 11, 12, 14, 15, 32, 49, 56, 76 | **37.52** | 0.037 | 0.007 |
| sentence-transformers/all-MiniLM-L6-v2 | FAISS Euclidean | 1, 2, 4, 5, 20, 64, 69, 83, 89, 92 | 1, 3, 16, 30, 54, 58, 59, 72, 84, 88 | 1, 8, 15, 16, 35, 45, 57, 68, 91, 99 | 1, 2, 3, 4, 14, 19, 26, 61, 69, 80 | 1, 2, 11, 12, 14, 15, 32, 49, 56, 76 | **37.52** | 0.043 | 0.009 |
| sentence-transformers/all-MiniLM-L6-v2 | ChromaDB | 1, 2, 4, 5, 20, 64, 69, 83, 89, 92 | 1, 3, 16, 30, 54, 58, 59, 72, 84, 88 | 1, 8, 15, 16, 35, 45, 57, 68, 91, 99 | 1, 2, 3, 4, 14, 19, 26, 61, 69, 80 | 1, 2, 11, 12, 14, 15, 32, 49, 56, 76 | **37.52** | 0.048 | 0.010 |
| paraphrase-multilingual-MiniLM-L12-v2 | Cosine Similarity | 3, 4, 18, 23, 29, 33, 47, 59, 65, 91 | 1, 5, 6, 16, 20, 59, 65, 77, 79, 100 | 2, 16, 17, 19, 29, 42, 43, 48, 60, 71 | 1, 2, 5, 10, 14, 23, 30, 42, 73, 80 | 1, 2, 3, 4, 7, 11, 16, 22, 23, 77 | **31.86** | 0.061 | 0.012 |
| paraphrase-multilingual-MiniLM-L12-v2 | FAISS Cosine | 3, 4, 18, 23, 29, 33, 47, 59, 65, 91 | 1, 5, 6, 16, 20, 59, 65, 77, 79, 100 | 2, 16, 17, 19, 29, 42, 43, 48, 60, 71 | 1, 2, 5, 10, 14, 23, 30, 42, 73, 80 | 1, 2, 3, 4, 7, 11, 16, 22, 23, 77 | **31.86** | 0.059 | 0.012 |
| paraphrase-multilingual-MiniLM-L12-v2 | FAISS Euclidean | 2, 5, 19, 20, 27, 34, 43, 51, 58, 81 | 1, 7, 9, 12, 20, 44, 61, 84, 86, 99 | 1, 11, 14, 26, 28, 31, 34, 47, 65, 73 | 1, 2, 12, 13, 19, 24, 27, 45, 54, 67 | 1, 2, 3, 5, 7, 11, 16, 22, 27, 82 | **30.66** | 0.059 | 0.012 |
| paraphrase-multilingual-MiniLM-L12-v2 | ChromaDB | 2, 5, 19, 20, 27, 33, 42, 50, 57, 80 | 1, 7, 9, 12, 20, 43, 60, 83, 85, 98 | 10, 13, 25, 27, 30, 33, 46, 64, 72 | 1, 2, 12, 13, 19, 24, 27, 45, 54, 66 | 1, 2, 3, 5, 7, 11, 16, 22, 27, 81 | **30.84** | 0.078 | 0.016 |
| neuralmind/bert-base-portuguese-cased | Cosine Similarity | 2, 3, 5, 6, 14, 36, 37, 44, 52, 71 | 2, 3, 4, 6, 13, 14, 16, 39, 40, 47 | 1, 2, 10, 12, 18, 23, 25, 39, 41, 45 | 1, 2, 3, 7, 8, 10, 21, 45, 55, 87 | 3, 5, 8, 17, 23, 34, 35, 67, 79, 88 | **25.36** | 0.174 | 0.035 |
| neuralmind/bert-base-portuguese-cased | FAISS Cosine | 2, 3, 5, 6, 14, 36, 37, 44, 52, 71 | 2, 3, 4, 6, 13, 14, 16, 39, 40, 47 | 1, 2, 10, 12, 18, 23, 25, 39, 41, 45 | 1, 2, 3, 7, 8, 10, 21, 45, 55, 87 | 3, 5, 8, 17, 23, 34, 35, 67, 79, 89 | **25.38** | 0.181 | 0.036 |
| neuralmind/bert-base-portuguese-cased | FAISS Euclidean | 2, 3, 5, 6, 14, 34, 48, 61, 66, 74 | 3, 4, 5, 7, 23, 28, 35, 44, 51, 60 | 1, 2, 8, 10, 13, 19, 27, 32, 39, 48 | 1, 2, 3, 8, 9, 14, 22, 53, 59, 81 | 11, 14, 15, 20, 32, 42, 44, 57, 67, 99 | **28.50** | 0.178 | 0.036 |
| neuralmind/bert-base-portuguese-cased | ChromaDB | 2, 3, 5, 6, 14, 34, 48, 61, 66, 74 | 3, 4, 5, 7, 23, 28, 35, 44, 51, 60 | 1, 2, 8, 10, 13, 19, 27, 32, 39, 48 | 1, 2, 3, 8, 9, 14, 22, 53, 59, 81 | 11, 14, 15, 20, 32, 42, 44, 57, 67, 99 | **28.50** | 0.194 | 0.039 |
| BAAI/bge-m3 | Cosine Similarity | 1, 2, 4, 10, 12, 14, 26, 32, 52, 58 | 1, 2, 4, 6, 9, 43, 54, 78, 90, 91 | 1, 3, 4, 5, 6, 7, 11, 15, 23, 43 | 1, 2, 3, 4, 5, 7, 8, 11, 16, 65 | 1, 2, 6, 9, 16, 25, 28, 41, 50, 67 | **21.48** | 0.564 | 0.113 |
| BAAI/bge-m3 | FAISS Cosine | 1, 2, 4, 10, 12, 14, 26, 32, 52, 58 | 1, 2, 4, 6, 9, 43, 54, 78, 90, 91 | 1, 3, 4, 5, 6, 7, 11, 15, 23, 43 | 1, 2, 3, 4, 5, 7, 8, 11, 16, 65 | 1, 2, 6, 9, 16, 25, 28, 41, 50, 67 | **21.48** | 0.666 | 0.133 |
| BAAI/bge-m3 | FAISS Euclidean | 1, 2, 4, 10, 12, 14, 26, 32, 52, 58 | 1, 2, 4, 6, 9, 43, 54, 78, 90, 91 | 1, 3, 4, 5, 6, 7, 11, 15, 23, 43 | 1, 2, 3, 4, 5, 7, 8, 11, 16, 65 | 1, 2, 6, 9, 16, 25, 28, 41, 50, 67 | **21.48** | 0.570 | 0.114 |
| BAAI/bge-m3 | ChromaDB | 1, 2, 4, 10, 12, 14, 26, 32, 52, 58 | 1, 2, 4, 6, 9, 43, 54, 78, 90, 91 | 1, 3, 4, 5, 6, 7, 11, 15, 23, 43 | 1, 2, 3, 4, 5, 7, 8, 11, 16, 65 | 1, 2, 6, 9, 16, 25, 28, 41, 50, 67 | **21.48** | 0.585 | 0.117 |

## Consolidado por Modelo


| Modelo | Média Geral |
|--------|-------------|
| N/A (lexical) | **37.42** |
| sentence-transformers/all-MiniLM-L6-v2 | **37.52** |
| paraphrase-multilingual-MiniLM-L12-v2 | **31.31** |
| neuralmind/bert-base-portuguese-cased | **26.93** |
| BAAI/bge-m3 | **21.48** |

## Conclusão


O melhor desempenho foi de **Cosine Similarity** com modelo **BAAI/bge-m3** (rank médio: **21.48**).


## Top 10 Respostas Selecionadas pelo Algoritmo Vencedor


*As respostas em **negrito** são as respostas úteis esperadas.*


### Query 1: Como começar a investir em renda fixa com segurança?


| # | Resposta |
|---|----------|
| 1 | **A renda fixa é uma modalidade de investimento onde você empresta dinheiro para uma instituição em troca de juros. Os principais títulos são Tesouro Direto, CDB, LCI e LCA. São opções mais seguras e previsíveis, ideais para quem busca preservar capital e ter renda constante.** |
| 2 | **Educação financeira é base do sucesso. Estude antes de investir. Livros, cursos e canais especializados ajudam. Comece com renda fixa e evolua gradualmente. Nunca invista no que não entende. Conhecimento protege contra golpes e escolhas ruins frequentes.** |
| 3 | Aporte regular é investir periodicamente todo mês. Cria disciplina e aproveita média de custos. Não tenta acertar timing do mercado. Foque em aumentar aportes mensais através de economia e aumento de renda. Constância é mais importante que valor inicial. |
| 4 | **O Tesouro Direto permite investir em títulos públicos federais. Existem três tipos: Pré-fixado (taxa fixa), IPCA+ (proteção contra inflação) e Selic (pós-fixado). É considerado o investimento mais seguro do país, pois tem garantia do governo federal.** |
| 5 | Aposentadoria por investimentos complementa INSS. Construa carteira geradora de renda. Diversifique fontes de proventos. Planeje-se décadas antes. Comece cedo para aproveitar juros compostos. Nunca é tarde para começar a investir. |
| 6 | Rebalanceamento ajusta carteira à alocação original. Se ações subiram muito, venda parte e compre renda fixa. Mantém risco controlado e disciplina. Faça semestralmente ou quando alocação desviar muito do planejado inicialmente definido. |
| 7 | Carteira recomendada varia conforme idade e objetivos. Jovens podem ter mais ações pela tolerância a riscos. Pessoas próximas da aposentadoria devem priorizar renda fixa. Rebalanceie periodicamente mantendo alocação definida no planejamento estratégico. |
| 8 | Imposto de Renda incide sobre ganhos de capital. Renda fixa tem tabela regressiva de 22,5% a 15%. Ações pagam 15% sobre lucro acima de 20 mil mensais. Fundos imobiliários são isentos para PF. Declare todos investimentos na declaração anual obrigatória. |
| 9 | Gestão de risco define quanto arriscar em cada operação. Nunca aloque tudo em um único ativo. Use stop loss para limitar prejuízos. Diversifique entre setores e classes. Preserve capital é regra número um do investidor inteligente e profissional. |
| 10 | **LCI e LCA são isentos de Imposto de Renda para pessoas físicas. Investem no setor imobiliário e agropecuário respectivamente. Possuem carência mínima de 90 dias e garantia do FGC. São excelentes para diversificação e otimização tributária.** |

### Query 2: O que é análise fundamentalista e como usar para escolher ações?


| # | Resposta |
|---|----------|
| 1 | **Análise fundamentalista avalia saúde financeira das empresas. Examina balanços, dívidas, lucros e perspectivas. Busca empresas sólidas e subvalorizadas. É essencial para escolher ações para longo prazo e construir carteira de qualidade com fundamentos fortes.** |
| 2 | **Análise técnica estuda gráficos e padrões de preços. Busca identificar tendências e momentos de compra e venda. Usa indicadores como médias móveis e RSI. Mais utilizada para operações de curto e médio prazo no mercado de ações e derivativos financeiros.** |
| 3 | Cursos especializados aprofundam temas específicos. Análise fundamentalista, técnica, opções. Escolha cursos de profissionais reconhecidos. Cuidado com gurus prometendo ganhos fáceis. Educação de qualidade requer tempo e dedicação. |
| 4 | **Relatório de analistas traz projeções sobre empresas. Corretoras publicam recomendações de compra ou venda. Use como referência mas não siga cegamente. Faça sua própria análise antes de decidir investir baseado em relatórios profissionais.** |
| 5 | Blue chips são ações de empresas grandes e consolidadas. Como Petrobras, Vale e bancos grandes. Menor potencial de valorização mas mais estáveis. Pagam dividendos regulares. Ideais para compor base sólida da carteira de ações defensiva. |
| 6 | **Valuation é método para calcular valor justo das ações. Compara preço atual com valor intrínseco da empresa. Se preço está abaixo do valuation, ação está descontada. Métodos comuns incluem fluxo de caixa descontado e múltiplos como P/L e EV/EBITDA.** |
| 7 | Tag along garante receber mesmo preço em venda da empresa. Protege acionistas minoritários. Se controlador vender ações, deve fazer oferta pelos minoritários também. Verifique se ação ordinária tem tag along de 100% antes de investir. |
| 8 | Mercado primário é emissão de novos títulos. Empresa recebe recursos diretamente. Como IPOs e follow-ons. Mercado secundário é negociação entre investidores. Bolsa é mercado secundário de ações. |
| 9 | **Governança corporativa são práticas de transparência da empresa. Níveis Novo Mercado têm regras mais rígidas. Protegem minoritários e melhoram gestão. Prefira empresas com boa governança para investir em ações na bolsa de valores.** |
| 10 | Direitos de acionista incluem voto e informações. Ações ordinárias dão direito a voto. Prefenciais têm prioridade em dividendos. Conheça diferenças entre classes de ações. Escolha conforme objetivos de investimento. |

### Query 3: Como montar uma carteira diversificada de investimentos?


| # | Resposta |
|---|----------|
| 1 | **Diversificação é a estratégia de distribuir recursos em diferentes ativos para reduzir riscos. Não coloque todos os ovos na mesma cesta. Uma carteira diversificada combina renda fixa, ações, fundos imobiliários e investimentos internacionais.** |
| 2 | Aposentadoria por investimentos complementa INSS. Construa carteira geradora de renda. Diversifique fontes de proventos. Planeje-se décadas antes. Comece cedo para aproveitar juros compostos. Nunca é tarde para começar a investir. |
| 3 | **Rebalanceamento ajusta carteira à alocação original. Se ações subiram muito, venda parte e compre renda fixa. Mantém risco controlado e disciplina. Faça semestralmente ou quando alocação desviar muito do planejado inicialmente definido.** |
| 4 | **Aporte regular é investir periodicamente todo mês. Cria disciplina e aproveita média de custos. Não tenta acertar timing do mercado. Foque em aumentar aportes mensais através de economia e aumento de renda. Constância é mais importante que valor inicial.** |
| 5 | **Carteira recomendada varia conforme idade e objetivos. Jovens podem ter mais ações pela tolerância a riscos. Pessoas próximas da aposentadoria devem priorizar renda fixa. Rebalanceie periodicamente mantendo alocação definida no planejamento estratégico.** |
| 6 | **Perfil de investidor define sua tolerância a riscos. Conservador prioriza segurança, moderado aceita algum risco e arrojado busca maiores retornos. Conheça seu perfil antes de investir para escolher ativos adequados à sua personalidade.** |
| 7 | **Gestão de risco define quanto arriscar em cada operação. Nunca aloque tudo em um único ativo. Use stop loss para limitar prejuízos. Diversifique entre setores e classes. Preserve capital é regra número um do investidor inteligente e profissional.** |
| 8 | Educação financeira é base do sucesso. Estude antes de investir. Livros, cursos e canais especializados ajudam. Comece com renda fixa e evolua gradualmente. Nunca invista no que não entende. Conhecimento protege contra golpes e escolhas ruins frequentes. |
| 9 | Comunidades de investidores trocam experiências. Fóruns, grupos e redes sociais. Aprenda com outros investidores. Mas filtre informações e faça sua análise. Não siga recomendações cegamente de grupos. |
| 10 | Fundos de investimento são condomínios onde vários investidores aplicam juntos. Um gestor profissional decide os ativos. Cobram taxa de administração e às vezes performance. Podem ser de renda fixa, ações, multimercado ou estrangeiros. |

### Query 4: Qual a diferença entre Tesouro IPCA+ e Tesouro Selic?


| # | Resposta |
|---|----------|
| 1 | **O Tesouro Direto permite investir em títulos públicos federais. Existem três tipos: Pré-fixado (taxa fixa), IPCA+ (proteção contra inflação) e Selic (pós-fixado). É considerado o investimento mais seguro do país, pois tem garantia do governo federal.** |
| 2 | **Tesouro IPCA+ protege contra inflação e paga juros real. Ideal para objetivos de longo prazo como aposentadoria. Possui marcação a mercado, podendo ter oscilações negativas se vendido antes do vencimento. Segure até o vencimento para garantir retorno.** |
| 3 | **Liquidez é facilidade de resgatar o investimento. Tesouro Selic tem liquidez diária. Alguns CDBs travam dinheiro até vencimento. Imóveis têm liquidez baixa. Considere liquidez conforme necessidade de uso do dinheiro em cada objetivo financeiro planejado.** |
| 4 | **Reserva de emergência deve cobrir de 6 a 12 meses de gastos mensais. Deve estar em aplicações seguras e com liquidez diária como Tesouro Selic ou CDB com liquidez. O objetivo é ter acesso rápido ao dinheiro em situações imprevistas.** |
| 5 | **Inflação corrói o poder de compra do dinheiro ao longo do tempo. Investimentos atrelados ao IPCA protegem seu patrimônio. É fundamental que seus rendimentos superem a inflação para garantir ganho real e manutenção do padrão de vida.** |
| 6 | A renda fixa é uma modalidade de investimento onde você empresta dinheiro para uma instituição em troca de juros. Os principais títulos são Tesouro Direto, CDB, LCI e LCA. São opções mais seguras e previsíveis, ideais para quem busca preservar capital e ter renda constante. |
| 7 | **O CDI é a taxa média dos empréstimos entre bancos e serve como referência para muitos investimentos. Atualmente está próximo da taxa Selic. Quando um investimento rende 100% do CDI, acompanha basicamente a taxa básica de juros da economia.** |
| 8 | **LCI e LCA são isentos de Imposto de Renda para pessoas físicas. Investem no setor imobiliário e agropecuário respectivamente. Possuem carência mínima de 90 dias e garantia do FGC. São excelentes para diversificação e otimização tributária.** |
| 9 | Setores cíclicos variam com economia. Como commodities e construção. Crescem na expansão e caem na recessão. Timing é importante nestes setores. Defensivos como utilities são estáveis em qualquer ciclo econômico. |
| 10 | Juros sobre capital próprio são proventos tributados em 15%. Diferente de dividendos isentos. Empresas pagam JSCP como forma de remunerar acionistas. Receba ambos mas saiba que JSCP tem imposto retido na fonte obrigatoriamente. |

### Query 5: Como proteger meu patrimônio da inflação?


| # | Resposta |
|---|----------|
| 1 | **Inflação corrói o poder de compra do dinheiro ao longo do tempo. Investimentos atrelados ao IPCA protegem seu patrimônio. É fundamental que seus rendimentos superem a inflação para garantir ganho real e manutenção do padrão de vida.** |
| 2 | **Tesouro IPCA+ protege contra inflação e paga juros real. Ideal para objetivos de longo prazo como aposentadoria. Possui marcação a mercado, podendo ter oscilações negativas se vendido antes do vencimento. Segure até o vencimento para garantir retorno.** |
| 3 | Rebalanceamento ajusta carteira à alocação original. Se ações subiram muito, venda parte e compre renda fixa. Mantém risco controlado e disciplina. Faça semestralmente ou quando alocação desviar muito do planejado inicialmente definido. |
| 4 | O Tesouro Direto permite investir em títulos públicos federais. Existem três tipos: Pré-fixado (taxa fixa), IPCA+ (proteção contra inflação) e Selic (pós-fixado). É considerado o investimento mais seguro do país, pois tem garantia do governo federal. |
| 5 | Custódia é guarda dos ativos investidos. Corretora ou banco custodia seus investimentos. Taxa de custódia pode ser cobrada. Muitas corretoras não cobram mais. Verifique onde seus ativos estão guardados. |
| 6 | **Mercado de câmbio permite investir em moedas estrangeiras. Dolarizar parte do patrimônio protege contra riscos do Brasil. Pode ser feito através de contas no exterior, ETFs de dólar ou fundos cambiais. Recomendado ter exposição internacional.** |
| 7 | Marcação a mercado causa oscilações em títulos prefixados. Se juros sobem, preços caem temporariamente. Não venda com queda se precisar do dinheiro depois. Segure até vencimento para garantir retorno contratado sem perdas reais na renda fixa. |
| 8 | Crises são oportunidades para investidores pacientes. Mercados caem mas recuperam historicamente. Mantenha caixa para aproveitar quedas. Não venda em pânico. Compre ativos de qualidade com desconto durante crises de mercado. |
| 9 | **Aposentadoria por investimentos complementa INSS. Construa carteira geradora de renda. Diversifique fontes de proventos. Planeje-se décadas antes. Comece cedo para aproveitar juros compostos. Nunca é tarde para começar a investir.** |
| 10 | Perfil de investidor define sua tolerância a riscos. Conservador prioriza segurança, moderado aceita algum risco e arrojado busca maiores retornos. Conheça seu perfil antes de investir para escolher ativos adequados à sua personalidade. |
