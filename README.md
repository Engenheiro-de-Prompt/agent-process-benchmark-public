# Process Benchmark — public edition

Procedimento portável para comparar entregas de agentes contra um resultado ideal
verificável: **contrato → evidência → execução → conferência → aceite ou bloqueio**.

Esta distribuição contém código, contratos e exemplos inteiramente sintéticos.
Não contém históricos de conversas, métricas de uso pessoal, credenciais, dados
de clientes, configurações da máquina de origem ou o histórico Git privado.

## Resultado observado, sem promessa de melhoria universal

| Ensaio | Resultado | Limite |
|---|---|---|
| Primeiras entregas reais de agentes | Baseline 24/24; SOP 24/24 | Empate: nenhuma superioridade da instrução adicional |
| Controles corretos | 12/12 aceitos | Qualificação somente nesses controles |
| Controles defeituosos | 97/97 bloqueados | Defeitos deliberados, não erros observados nos agentes |

São 12 casos únicos, quatro em cada atividade: reconciliação financeira,
obrigações de reunião já estruturadas e estoque. Duas réplicas e dois braços
produziram 48 entregas. Réplicas não equivalem a novos casos independentes.
Não há demonstração de ROI, melhoria em produção ou generalização para qualquer
modelo/cliente. Um ensaio adicional de runtime ficou inconclusivo e não integra
a comparação publicada; não foi convertido em vitória.

## Verificar sem modelos, rede ou fontes privadas

Requisito: Python 3.11 ou superior, biblioteca padrão; Git para o scanner do índice.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tools/verify_release.py
python3 tools/check_publication.py
```

O replay confere os arquivos congelados, reconstrói os controles e recalcula a
avaliação em temporário, comparando com `reports/results.json`. Não chama modelos
nem reescreve os artefatos originais. Abra `reports/index.html` para inspecionar
casos, entregas e diagnósticos. A CI executa testes, replay e scanner do índice.

## Adaptar a outro agente ou atividade

- [Procedimento de entrega](methods/DELIVERY_SOP.md).
- [Template de contrato](methods/PROCESS_CONTRACT_TEMPLATE.json).
- [Métricas e limites](methods/METRICS.md).
- [Transferência entre domínios](docs/TRANSFER.md).
- [Protocolo inicial](docs/PROTOCOL.md) e [desenho final congelado](docs/CAMPAIGN_DESIGN.md).
- [Resultado e limites](docs/RESULTADO.md).
- [Política de sanitização](docs/PUBLICATION.md).

O desenho final prevalece sobre a granularidade do esboço inicial. Os executores
receberam somente os insumos públicos de sua coorte; gabaritos não foram fornecidos.
A fronteira foi de contexto/instrução auditada, não sandbox de sistema operacional.
Publicar gabaritos agora serve à auditoria; uma nova avaliação cega exige não os
fornecer ao executor e controlar contaminação prévia.

O procedimento é transferível; contrato, referência e verificador precisam ser
adaptados e validados por domínio. Se não há regra automática confiável, o aceite
permanece com revisor humano autorizado. Custo de preparação não é economia
comprovada. Uma barreira que detecta erros não prova que o agente passou a gerá-los
com menor frequência.

## Novos experimentos

Não sobrescreva a campanha preservada. Trabalhe numa cópia para desenvolvimento,
versione novos casos e registre um novo desenho antes das execuções. `bench.py`
expõe `freeze`, `stage`, `ingest` e `evaluate`; consulte `python3 bench.py --help`.
Nunca execute `freeze` sobre a campanha existente para tentar renovar sua origem.
Para uma campanha nova, adapte a configuração numa cópia separada e mantenha
as evidências antigas intactas. Não reescreva hashes para fazer uma edição passar.

## Segurança e direitos

Scanner heurístico não garante ausência de todo segredo. Não adicione `.env`,
transcrições, bases reais, logs privados ou configurações de autenticação. Use
controles sintéticos e revisão independente antes de publicar novas versões.
A visibilidade pública não estabelece, por si só, uma licença de reutilização;
nenhuma licença adicional foi atribuída nesta sanitização.
