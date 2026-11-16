# Indicadores de negócio e limites de decisão

| Pergunta | Indicador observável | Comparação necessária |
|---|---|---|
| O agente entrega certo de primeira? | Entregas com TODOS os critérios obrigatórios aprovados / entregas planejadas | Mesmo conjunto e contexto por braço |
| O processo deixa erro escapar? | Entregas incorretas aceitas / incorretas aferidas independentemente | Controles conhecidos; depois auditoria real autorizada |
| Ele bloqueia entregas boas? | Entregas corretas rejeitadas / corretas aferidas | Controles positivos e piloto |
| Menos trabalho humano? | Minutos de revisão e retrabalho por entrega aprovada | Tempo observado de pessoas, não token ou opinião do agente |
| Menor custo? | Custo atribuível total / entregas aprovadas | Incluir checagem, rejeições e correções, não só geração |
| É transferível? | Critérios de promoção cumpridos em atividade/agente novos | Novo contrato e ensaio sem ajustar ao resultado observado |

**No ensaio presente:** aferimos aceite contra contrato e o comportamento do gate
em controles conhecidos. Não medimos horas humanas, custo total, cliente satisfeito
ou receita. Não há ROI publicado. Estoque representa transferência de atividade;
não representa homologação em outro cliente ou outro modelo.

O ideal de cada caso está registrado independentemente em `tests/oracles.json` e
recomputado a partir das fontes pelo verificador. `reports/index.html` põe esse
ideal ao lado da primeira entrega efetivamente recebida, inclusive reprovações.
Não se usa a declaração do agente como verdade de referência.

Ausência/saída inválida permanece no denominador. Réplicas reutilizam os mesmos
casos e não justificam tratar a amostra como mais clientes ou atividades novas.
Um validador que conhece apenas certas regras não garante que detectará erro
fora delas. Atividades subjetivas exigem aceite humano autorizado; sem ele,
marcar não aferido, nunca sucesso presumido.

O template é propositalmente `ready_to_run=false`: precisa ser preenchido e
homologado pelo dono do processo. Automatizar uma regra errada só cria confiança
indevida. Também existe custo de criar/manter os verificadores por atividade;
a SOP é reutilizável, o gabarito não é universal.
