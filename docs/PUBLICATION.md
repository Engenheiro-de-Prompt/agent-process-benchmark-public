# Sanitização da edição pública

## Conteúdo incluído

- Código do benchmark e testes de biblioteca padrão.
- Fontes, contratos, gabaritos e controles de três atividades fictícias.
- Primeiras entregas da campanha sintética concluída, plano congelado e avaliação.
- Procedimento genérico, métricas e guia de transferência.

## Conteúdo excluído

- Agregados derivados de históricos pessoais, contagens de sessões/mensagens e
  relatório de oportunidades baseado em uso privado.
- Inventários/auditorias de execução ligados ao ambiente original.
- Respostas brutas e metadados do ensaio de runtime local inconclusivo.
- Coletor de históricos e ferramentas que dependiam desses dados/ensaios.
- Relatórios e notas de revisão que combinavam conteúdo sintético e privado.
- Histórico Git, refs, configurações, anexos e metadados de autores do repositório
  de origem. Esta edição começa com histórico próprio.

Resultados científicos da campanha sintética mantida não foram alterados para
sanitizar: fontes/gabaritos/entregas continuam verificáveis com seus hashes
congelados. Datas e identificação do perfil de executor dessa campanha são
metadados experimentais, não credenciais ou caminhos de instalação. O ensaio
local excluído permaneceu inconclusivo; não fundamenta eficácia ou superioridade.

## Verificações

O repositório de origem foi inspecionado por mirror completo das refs disponíveis,
com varredura de todos os blobs alcançáveis e metadados de commits. O Gitleaks
usado na inspeção teve seu arquivo verificado contra o checksum oficial. Não
foram identificadas credenciais reais nessa varredura. Matches de uma URL de
credencial fictícia em teste e de nomes de campos proibidos no scanner foram
classificados como controles de segurança, não credenciais reais.

A edição pública usa snapshot sem herdar o histórico original, seleção explícita
de arquivos, scanner do índice e revisão independente. A varredura não é prova
universal: regras podem não reconhecer um segredo ou uma pessoa pode ser
identificável por contexto fora do pacote. Este documento não certifica
configurações de contas, serviços externos ou segurança de produção.

A CI verifica o conteúdo versionado. Não publique arquivos ignorados à parte.
Se uma credencial real for exposta depois, removê-la do código não basta: revogue
ou rotacione no provedor e examine histórico, cópias e superfícies de distribuição.
