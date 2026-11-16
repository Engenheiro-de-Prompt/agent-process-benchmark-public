# Protocolo prévio — benchmark de entregas de negócio

## Estado e finalidade

Este documento registra decisões **antes das execuções**, não resultados. A campanha só poderá começar depois do congelamento descrito abaixo. Não há neste documento alegação de melhoria alcançada, retorno financeiro ou homologação de cliente.

Objetivo: comparar a primeira entrega de agentes reais com e sem um procedimento genérico de evidência e checagem pré-entrega, contra um ideal explícito de negócio. Separadamente, qualificar um gate determinístico contra entregas válidas e falhas conhecidas. A pergunta é se o procedimento melhora entregas neste conjunto sem regressões; não se um filtro consegue recusar erros fabricados.

Cadeia de valor: responsável de negócio → solicita artefato → recebe informação verificável contra contrato → pode fundamentar uma decisão. Correção sintética é condição técnica observável, não demonstração de utilidade reconhecida por cliente ou de economia realizada.

## Desenho e braços

- **Baseline:** pedido + contrato de entrega.
- **SOP:** o mesmo pedido + o mesmo contrato + o procedimento genérico abaixo.
- Ambos são agentes reais, executados pelo mecanismo nativo de agentes com modelos hospedados atuais; **não são modelos locais**, saídas roteirizadas, mocks ou respostas escritas pelo avaliador.
- Fixar o mesmo identificador de modelo, provedor, versão quando exposta, parâmetros disponíveis, ferramentas, permissões, limites de saída, prazo e orçamento de escopo para os dois braços. Registrar valores efetivos no manifesto anterior aos runs, sem credenciais. Não inventar identificador ou capacidade que a plataforma não exponha. Mudança de modelo ou configuração invalida a comparabilidade da campanha e requer novo congelamento.
- O único diferencial deliberado de contexto é a SOP. Seu custo adicional de contexto e de checagem integra o custo do tratamento, não autoriza ferramentas ou orçamento maior.
- Cada caso recebe uma primeira entrega por braço em sessão isolada, sem memória de outros casos, braço concorrente ou feedback de avaliação. Alternar a ordem baseline/SOP entre os casos em uma ordem fixada no manifesto antes da execução. Não escolher ordem após observar resultados.

### Texto da intervenção SOP

> Antes de executar, explicite os critérios de entrega já presentes no pedido e no contrato, sem criar exigências ou flexibilizá-las. Mapeie cada conclusão ou campo às evidências disponíveis; diferencie fatos, cálculos, ausência de informação e inferências, sem inventar dados. Produza o artefato pedido e faça uma checagem independente do raciocínio gerador, recalculando ou conferindo diretamente as fontes e o contrato com as ferramentas permitidas. Corrija problemas encontrados por você antes da entrega final dentro do orçamento original. Só declare concluído o que foi efetivamente conferido; sinalize limites e informação insuficiente conforme o contrato. Não consulte gabaritos, verificadores reservados ou outros executores.

A checagem do executor não substitui o verificador independente. O baseline não é proibido de conferir espontaneamente: a comparação mede o efeito de adicionar a instrução, não de incapacitar o controle. Nenhum braço recebe o gate reservado ou suas respostas.

## Corpus e ideal de negócio

São **12 casos sintéticos: 4 de finanças, 4 de obrigações de reunião e 4 de estoque**. Um subagente distinto prepara os dados, os contratos e os verificadores. Gabaritos escritos independentemente das respostas dos executores permanecem fora de seu contexto e do diretório atribuído. A fronteira nativa é de instrução/contexto, não de inacessibilidade técnica; os detalhes finais de coortes, duas réplicas e limites estão em CAMPAIGN_DESIGN.md. Não derivar o esperado da saída candidata nem usar um braço como gabarito do outro.

Cada caso precisa ter, antes de qualquer run:

1. ID estável, domínio, pedido, fontes públicas sintéticas e contrato de saída explícito.
2. Ideal escrito: valores, itens ou estados esperados e evidências nas fontes; campos ausentes e abstenções obrigatórias também definidos.
3. Regras semânticas executáveis: campos obrigatórios, completude, proibição de itens extras indevidos, rastreabilidade e critérios de negócio. Schema válido sozinho não basta.
4. Regras antecipadas de datas, unidades, sinais, precisão, arredondamento, ordenação e equivalências admissíveis quando aplicáveis. Qualquer tolerância deve ser justificada e congelada antes dos runs; não adicionada para aceitar uma resposta observada.
5. Verificador determinístico e controles positivos/negativos para suas regras. Sem LLM juiz, julgamento subjetivo pós-hoc ou critério secreto incompatível com o contrato público.

As dimensões de negócio dependem dos casos efetivamente criados. Em finanças, verificar cálculos e convenções documentadas; em reunião, distinguir compromisso explícito de sugestão e não inventar responsáveis/prazos; em estoque, respeitar movimentos, unidades e regras de reposição do contrato. Esses exemplos não inventam valores nem substituem os gabaritos independentes.

## Congelamento e segregação

Antes do primeiro run, selar em manifesto as versões/hashes dos 12 casos, pedidos, contratos, gabaritos reservados, verificadores, controles, prompts dos braços, protocolo, limites efetivos e ordem de execução. Registrar também a seleção completa de casos; não reconstruir denominadores a partir das entregas existentes. Esses registros ficam a cargo da campanha, não são resultados deste documento.

A área dos executores contém somente as fixtures públicas da respectiva coorte e o contrato; no braço SOP, também seu procedimento. Não fornecer gabaritos, código reservado ou respostas de outros braços no contexto ou diretório atribuído. As ferramentas gerais não impõem isolamento OS: essa limitação é explícita e não há homologação de sandbox. Uso observado de material reservado invalida a comparação. CAMPAIGN_DESIGN.md especifica a configuração final anterior às execuções.

Revisar contratos, gabaritos e controles antes do congelamento. Depois dele, não alterar casos, selecionar os mais favoráveis, afrouxar verificadores ou retocar prompts. Erro descoberto no avaliador deve ser documentado; preservar campanha e resultados originais, bloquear a decisão afetada e abrir nova versão/campanha. Não corrigir silenciosamente o passado.

## Execução e preservação

- Guardar a primeira entrega final original, metadados disponíveis de execução, limites, consumo observado quando exposto e diagnóstico determinístico. Vincular cada artefato ao caso, braço e snapshot congelado.
- O executor pode revisar seu próprio rascunho antes da entrega final dentro do orçamento. Após a primeira entrega final, o avaliador **não repara**, completa, normaliza conteúdo sem autorização do contrato nem devolve feedback para uma segunda tentativa.
- Timeout, saída ausente, incompleta ou inválida permanece no denominador e não conta como sucesso. Separar falha de entrega de incidente de infraestrutura; incidente deixa a conclusão causal inconclusiva, sem apagar o slot planejado nem substituir seletivamente o run. Qualquer repetição deve ser campanha separada e identificada, não sobrescrita.
- Executar o verificador reservado sobre os bytes preservados de ambos os braços. Parsing e normalização só conforme regras congeladas; registrar resultado por critério e diagnóstico sem inventar evidência.
- Não executar negócio real, pagamentos, alterações operacionais ou ações sobre clientes. Não confundir obtenção do artefato com aprovação semântica.

## Análise pareada: realizado versus ideal

Para cada caso, publicar o ideal contratado, o realizado em cada braço, critérios satisfeitos/violados e evidência do diagnóstico. Resultado primário binário: **aceito somente se todas as exigências obrigatórias do caso forem satisfeitas**. Ausência de critério executável não vira passe; a capacidade não foi avaliada.

Classificar cada par:

| Baseline | SOP | Interpretação |
|---|---|---|
| Reprova | Aprova | Melhora |
| Aprova | Reprova | Regressão |
| Aprova | Aprova | Empate com aceite |
| Reprova | Reprova | Empate sem aceite |

Informar as contagens pareadas no conjunto completo e por domínio, mantendo os casos planejados. A diferença de aceitações deriva das melhoras menos regressões; não usar médias de campos fáceis para ocultar falha obrigatória. Tempos, uso de ferramentas, tokens e custo monetário são descritivos apenas quando observados e atribuíveis; indisponibilidade permanece desconhecida, não zero. Não extrapolar custo, ROI ou significância estatística sem base. Não alterar thresholds ao conhecer resultados.

## Qualificação separada do gate

A bateria reservada inclui entregas válidas escritas independentemente e falhas conhecidas nos **três domínios**. Congelar inventário, rótulo esperado e razão contratual de cada controle antes dos runs. Incluir violações semânticas e de completude/rastreabilidade pertinentes ao contrato, além de problemas de formato: aceitar qualquer saída parseável é insuficiente. Controles positivos impedem que rejeitar tudo pareça proteção.

Relatar por domínio e no total: válidos aceitos/rejeitados, inválidos aceitos/rejeitados, e erros de execução. O limiar de qualificação é **100% dos controles válidos aceitos e 0 controles inválidos aceitos em cada um dos três domínios**, sem erros que impeçam avaliação e com controles de ambos os tipos em cada domínio. Bateria ausente ou sem controles positivos/negativos não qualifica o gate.

Controles são testes do avaliador: **não são execuções reais dos agentes**, não entram nos 12 pares e não provam melhoria da geração. Recusar erros conhecidos permite somente proteção limitada às regras e à bateria exercitadas; não prova detectar todo erro futuro. Mesmo gate qualificado não garante que o contrato represente corretamente o negócio.

## Regra de decisão pré-registrada

Promover o procedimento como melhoria **nesta campanha sintética** somente quando todas as condições forem satisfeitas:

- Há **mais de zero melhoras e zero regressões** nos pares de primeiras entregas dos agentes reais sobre os casos sintéticos.
- O gate satisfaz **100% de válidos aceitos e zero inválidos aceitos nos três domínios** na bateria separada.
- Os 12 pares estão avaliáveis e íntegros, o congelamento e a segregação foram cumpridos e não há incidente que invalide a comparação.

Qualquer condição não satisfeita impede promoção; distinguir resultado negativo de campanha inconclusiva. Não enfraquecer o critério para obter vitória. Se ambos os braços obtiverem **12/12**, há empate no aceite e **nenhuma superioridade de geração demonstrada**. O gate ainda pode qualificar proteção limitada em avaliação separada. Resultado nulo é admissível e deve ser preservado.

Pequena amostra sintética não valida generalização universal, confiabilidade em toda atividade, benefício causal em produção ou economia real. Mesmo uma promoção não elimina a necessidade de adaptação, validação por domínio e homologação com usuários autorizados.

## Ética, privacidade e fronteira de execução

Somente conteúdo sintético e metadados sanitizados podem integrar o repositório. Não acessar históricos, configurações, credenciais ou outros projetos para preencher o benchmark. Heurísticas agregadas eventualmente obtidas em investigação local separada apenas motivam hipóteses; **não provam resultado alcançado**, frequência nesta amostra ou ganho do procedimento.

Os modelos dos executores são hospedados e recebem somente fixtures públicas sintéticas. Fontes reais, se futuramente autorizadas em outro trabalho, são de processamento **exclusivamente local**: não enviá-las aos agentes hospedados, nem publicar trechos, identificadores ou derivados identificáveis. A presente campanha não autoriza tal acesso. Não registrar segredos em manifestos ou logs.

O registro deste protocolo não executa a campanha e não autoriza rede, instalação ou commit. A evidência futura deverá distinguir preparação, execução real dos agentes, qualificação do gate e aceite de negócio.
