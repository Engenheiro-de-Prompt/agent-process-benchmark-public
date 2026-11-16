# Transferência do método para atividades de negócio

## O que é transferível

A estrutura geral é: **pedido → contrato de entrega → evidências → artefato → verificação independente → decisão limitada ao que foi demonstrado**. Não exige um setor específico. A verificação, porém, não é universal: contratos, gabaritos e verificadores precisam ser construídos, adaptados e validados em cada domínio. Sem critério observável e justificável, não é possível avaliar correção; uma aparência convincente ou declaração de conclusão não preenche essa lacuna.

O procedimento candidato pede explicitação dos critérios já acordados, mapeamento de evidências sem inferências indevidas e checagem pré-entrega independente do raciocínio gerador. Não é uma garantia técnica de que um agente obedecerá, nem um substituto para validação externa.

`PROTOCOL.md` fixa o desenho e os thresholds desta campanha. Este guia não os altera e não apresenta resultados. A campanha usa agentes nativos reais com modelos hospedados atuais e somente fixtures públicas sintéticas; não é uma avaliação de modelo local.

## Receita de adaptação

### Definir a decisão antes de automatizar

Identificar ator, ação, informação confiável necessária e decisão viabilizada. Distinguir produzir um arquivo, obter um cálculo correto e habilitar uma decisão de negócio. Escolher uma entrega delimitada cuja correção possa ser observada, sem reduzir silenciosamente a meta para aquilo que o verificador consegue testar.

### Escrever o contrato do ideal

Descrever entradas autorizadas, saída esperada, campos obrigatórios, evidências exigidas, ausência de informação, proibições e condições de abstenção. Definir unidades, arredondamento, datas e equivalências quando necessários. Explicar o que constitui erro relevante para a decisão, não apenas para o parser.

Um critério não pode ser inventado após ver a resposta. Se o pedido for ambíguo, esclarecer o contrato antes da avaliação. Se não houver padrão defensável de correção, registrar a atividade ou dimensão como não avaliável por esse desenho. Não disfarçar preferência subjetiva como regra determinística.

### Construir uma referência independente

Escrever o gabarito a partir das fontes, fora do contexto do executor e antes de receber suas respostas. Outra pessoa ou agente segregado deve conferir sua consistência com o contrato. Não usar a resposta candidata, o baseline ou a autoconfiança do modelo como referência de verdade.

O gabarito pode conter valores exatos, conjuntos de obrigações ou invariantes verificáveis conforme a atividade. Tarefas abertas podem exigir critérios adicionais de avaliação humana sob outro protocolo; o presente benchmark não utiliza LLM juiz e não comprova qualidades que seu verificador não mede.

### Implementar e desafiar o verificador

Construir regras determinísticas para as exigências que puderem ser operacionalizadas. Validar tanto entregas válidas quanto violações conhecidas, incluindo erros semânticos e omissões. Examinar falsos aceites e falsas rejeições: um gate que rejeita tudo não é útil; um gate que aceita todo JSON não verifica negócio.

Preservar separação entre avaliar um resultado e repará-lo. Caso seja desejado um ciclo de reparo em outro produto, avaliá-lo em experimento distinto, com custo, tentativas e entregas originais preservados. Não atribuir sua melhoria à primeira geração desta campanha.

### Congelar e comparar em condições equivalentes

Fixar casos, contratos, gabaritos, verificadores, controles, prompts, modelo, ferramentas, limites e ordem antes dos runs. Comparar primeiras entregas pareadas nos mesmos casos. Manter o baseline capaz de usar as mesmas ferramentas e conferir por conta própria. Isolar contextos e impedir acesso ao esperado reservado.

Registrar interrupções, ausência de artefato e falhas sem excluí-las para aumentar a taxa de sucesso. Um incidente que comprometa a comparabilidade torna a conclusão inconclusiva, não prova superioridade do outro braço.

### Decidir com limites explícitos

Separar três afirmações:

- **Melhoria de geração:** o agente com procedimento entregou melhor sob comparação pareada válida.
- **Proteção do gate:** o verificador aceitou controles válidos e recusou falhas conhecidas na bateria exercitada.
- **Valor em produção:** usuários reais conseguiram decidir melhor, com risco e custo aceitáveis em seu contexto.

Uma afirmação não substitui a seguinte. Para esta campanha, promoção exige mais de zero melhoras, zero regressões nos 24 pares reais de agentes sobre 12 casos sintéticos e duas réplicas e gate com todos os válidos aceitos e nenhum inválido aceito nos três domínios, além da integridade do desenho. Empate com 24/24 em ambos os braços não demonstra superioridade de geração. Pequena amostra permite no máximo conclusão restrita; não valida universalidade nem ROI de cliente.

## Comparar realizado e ideal sem inflar evidência

Usar uma ficha por caso com os seguintes campos, preenchidos somente após a execução:

| Campo | Conteúdo verificável |
|---|---|
| Caso e snapshot | ID do caso e vínculo com versões congeladas |
| Decisão de negócio | O que o ator precisa poder fundamentar |
| Ideal | Exigências do contrato e referência independente |
| Evidências disponíveis | Identificadores das fontes sintéticas autorizadas |
| Realizado baseline | Primeira entrega preservada e seu diagnóstico |
| Realizado SOP | Primeira entrega preservada e seu diagnóstico |
| Lacuna | Exigência violada, omissão, invenção ou desconhecimento |
| Resultado pareado | Melhora, regressão ou empate conforme o protocolo |
| Cobertura e limites | O que o verificador demonstra e o que permanece fora |
| Custo observado | Recursos efetivamente medidos ou indisponibilidade explícita |

Não preencher fichas com números ilustrativos que possam ser confundidos com resultados. Não comparar controles fabricados a entregas reais como se fossem braços experimentais. Uma regra estrutural verde não certifica fidelidade semântica fora de sua cobertura.

## Aplicações nos três domínios desta campanha

| Domínio | Ideal a especificar no caso | Risco a cobrir por evidência e regras |
|---|---|---|
| Finanças | Resultado calculado segundo fontes e convenções contratadas | Sinal, unidade ou arredondamento incorreto; total sem suporte; entrada omitida |
| Obrigações de reunião | Conjunto de compromissos explícitos, com responsáveis/prazos somente quando suportados | Transformar sugestão em obrigação; inventar responsável ou data; perder obrigação |
| Estoque | Estado ou decisão derivada dos movimentos e política informada | Ignorar movimento; misturar unidades; aplicar regra de reposição não contratada |

Esses exemplos descrevem categorias de risco, não resultados ou valores esperados dos casos. A adaptação para outra atividade deve recriar essa ligação entre decisão, evidência e erro significativo, não simplesmente renomear colunas.

## Custos e manutenção

A implantação exige esforço de definir contratos, preparar fontes sintéticas representativas, escrever e revisar gabaritos, implementar verificadores, criar controles, segregar acessos e manter rastreabilidade. Há ainda custo de contexto da SOP, checagem do executor, execução do gate, revisão de exceções e atualização quando regras de negócio mudam.

Medir custo de configuração e custo por execução separadamente. Qualquer amortização depende de volume e horizonte explicitamente declarados, não de economia presumida. Tempo de execução do agente não equivale a horas humanas poupadas; bloqueios podem evitar erro ou apenas criar retrabalho. Só chamar de ganho financeiro quando houver custo observado, comparador defensável e validação de negócio apropriada. Este benchmark sintético, por si só, não prova economia real.

Versionar contrato, referência e verificador em conjunto. Mudança de regra requer nova validação dos controles e nova campanha quando afetar comparabilidade. Falso aceite, falsa rejeição ou falha de infraestrutura não devem ser ocultados por reparos silenciosos. O gate é tão limitado quanto seus critérios e sua cobertura.

## Dados, ética e uso fora do laboratório

Somente dados sintéticos e registros sanitizados pertencem ao repositório. Fixtures públicas podem ser enviadas aos modelos hospedados; gabaritos e verificadores reservados não são disponibilizados aos executores. Fontes reais, caso autorizadas separadamente, devem permanecer em processamento local, sem envio aos agentes hospedados. Não acessar históricos, configurações, credenciais ou outros projetos para completar exemplos.

Heurísticas agregadas de histórico eventualmente produzidas em trabalho local separado são pistas para formular hipóteses, não prova de falha nesta amostra, benefício alcançado ou resultado de cliente. Não copiar conteúdo histórico ou derivados identificáveis para o repositório. Não alegar anonimização apenas porque nomes foram removidos.

Antes de uma adoção real, definir autorização e governança de dados, responsáveis pelo contrato, consequências de falso aceite/rejeição e tratamento das exceções. Validar utilidade com o ator de negócio e critérios adequados ao risco, sob escopo separado. Nenhuma dessas etapas pode ser marcada como concluída pelos resultados sintéticos desta campanha.

## Handoff para a campanha

O responsável pelos casos deve entregar dados públicos sintéticos, contratos, referências reservadas, verificadores e controles consistentes entre si. O responsável pela execução deve demonstrar segregação, congelamento e equivalência dos braços antes de executar. O avaliador deve preservar primeiras entregas e publicar análise pareada e qualificação do gate separadamente.

Até existirem essas evidências, o estado correto é **protocolo documentado; resultados não demonstrados**. Esta documentação não executa runs, não certifica verificadores ainda não exercitados e não autoriza rede, instalações, commits ou acesso a fontes privadas.
