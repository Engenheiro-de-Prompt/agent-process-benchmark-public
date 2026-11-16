# Resultado do benchmark sintético

A campanha concluída preserva 48 primeiras entregas de agentes reais: 12 casos,
três atividades, dois braços e duas réplicas. Baseline e SOP tiveram 24/24 aceites.
A instrução adicional não demonstrou superioridade. O efeito de teto restringe
as conclusões; não prova ineficácia da SOP em todos os contextos.

Separadamente, o gate aceitou 12 controles corretos e rejeitou 97 defeituosos.
Esses controles foram criados deliberadamente; não são falhas reais dos agentes.
A proteção está qualificada somente para a bateria conhecida, não para todo
erro possível ou uso em produção.

O ideal e as entregas podem ser conferidos em `reports/index.html`; os resultados
estruturados estão em `reports/results.json`. O replay offline verifica o mesmo
resultado sem consultar modelos ou históricos privados.

A metodologia é reutilizável: contrato, referência, controles positivos/negativos,
primeira entrega e conferência independente. Regras e referências precisam ser
adaptadas à nova atividade e validadas antes de aprovar seu uso. Sem critérios
confiáveis, mantenha aceitação humana autorizada.

Não houve medição de economia financeira, retrabalho real ou ganho em clientes.
Um teste adicional de runtime, excluído desta edição para minimizar metadados
operacionais, foi inconclusivo e não sustenta alegação de ganho.
