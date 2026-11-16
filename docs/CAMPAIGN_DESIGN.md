# Desenho final da campanha 001 (antes das execuções)

Este documento especifica os detalhes operacionais do protocolo e prevalece sobre
as formulações de isolamento e unidade de execução do esboço PROTOCOL.md. Ambos
são congelados antes das primeiras entregas. Não altera o limiar de promoção.

- **12 casos únicos, dois braços, duas réplicas:** 48 entregas, 24 pares. Réplicas
  não são 24 casos independentes. Nenhum cliente real é uma unidade experimental.
- **Unidade de execução:** um agente por domínio/braço/réplica, com os quatro
  casos daquele domínio. Total de 12 agentes independentes. Existe contexto
  compartilhado entre os quatro casos da mesma coorte; isso limita inferência.
  Não existe feedback do avaliador, visão do outro braço ou reparo pelo pai.
- **Modelo exposto:** gpt-6.1-sol / openai-codex, conforme metadados disponíveis
  do runtime de agentes. Não controlamos seed, temperatura, versão de pesos,
  limite efetivo de contexto ou scheduler da plataforma. Os dois braços herdam
  os mesmos defaults e capacidades; parâmetros não expostos ficam desconhecidos.
- **Baseline operacional:** herda instruções gerais do runtime, inclusive hábitos
  de verificação. Não é um agente artificialmente incapacitado. O ensaio mede o
  benefício INCREMENTAL de fornecer a SOP no pedido, não SOP versus ausência
  universal de toda verificação.
- **Intervenção:** texto integral de methods/DELIVERY_SOP.md anexado somente ao
  braço SOP. Ferramentas e escopo idênticos. O baseline pode conferir livremente.
- **Segregação:** cada executor recebe apenas task.json próprio com casos públicos,
  sem oráculos, código do avaliador, resultados de outros executores ou textos do
  histórico. Recebe instrução de não ler fora do diretório do worker. Isso NÃO é
  uma sandbox OS e não torna outros caminhos tecnicamente inacessíveis. A
  fronteira é de contexto e escopo instruído; não homologamos segurança adversarial.
- **Término:** primeira versão final de deliveries.json é recolhida após a conclusão
  do agente, sem correções do pai. Regravações internas antes da entrega são
  permitidas para ambos. Erros, ausências e formato inválido ficam no denominador.
- **Resultado de negócio primário:** entrega inteiramente aceita contra contrato,
  não número de testes, confiança textual ou alegação de conclusão do agente.
- **Custos:** tempo desde preparação pode incluir fila; não é latência pura de
  execução nem economia do cliente. Tokens e custo monetário por worker não são
  prometidos. Sem dados atribuíveis, não publicaremos ROI.

A qualificação de proteção é separada: o gate deve aceitar todos os controles
válidos e recusar todos os inválidos conhecidos em cada domínio. Isso valida a
conferência nessas regras, não demonstra redução de erros gerados pelo agente.
Uma alegação de geração melhor exige mais de zero pares melhorados, zero
regressões e todos os pares completos. Sem isso, o resultado será empate ou
inconclusivo, mesmo se o gate estiver qualificado.
