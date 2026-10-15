<p align="center"><img src="docs/lio_l_logo.png" alt="LIO-L" width="300"></p>

# LIO-L · Leitura Inteligente Orientada de Leis

> **Versão beta 1:** em teste. Sua opinião ajuda a definir a versão 1.0 — veja [Contribua](#contribua).

Ferramenta de estudo de **lei seca** para concurseiros, estudantes de Direito e quem precisa conhecer uma norma a fundo. A LIO-L lê a lei **artigo por artigo**, treina a percepção das palavras que as bancas trocam e faz você responder itens **Certo/Errado no estilo da prova**, com confiança declarada e nota líquida.

A LIO-L faz parte da família **LIO**. A [LIO-E](https://github.com/JOACYFRANCA/lio) (Educacional) é a ferramenta de leitura de textos densos, e a [LIO-C](https://github.com/JOACYFRANCA/lio-c) é a de ciências (Matemática, Física e Química). A LIO-L é derivada da LIO-E e adaptada a textos normativos. Na lei não há parágrafo denso nem ideia escondida: **tudo é importante**, e o trabalho do leitor deixa de ser *selecionar* para ser *discriminar*: perceber a diferença entre "pode" e "deve", entre "até dois anos" e "dois anos", entre a regra e a ressalva no fim do inciso. A metodologia completa está em [METODOLOGIA.md](METODOLOGIA.md).

## O que a LIO-L faz

- **Separa a lei em artigos.** Cola-se o texto do site do Planalto (ou anexa-se o PDF) e a LIO-L reconhece artigos, parágrafos, incisos, alíneas, penas, rubricas e a divisão em Títulos, Capítulos e Seções. Anotações do texto compilado ("Redação dada pela…") ficam guardadas à parte. Artigos muito longos são partidos entre incisos.
- **Nove etapas por seção:**

| | Etapa | O que você faz |
|---|---|---|
| 1 | Mapa topográfico | Lê só os caputs e prevê o que vem em cada artigo |
| 2 | Leitura do artigo | Escreve **a regra em uma frase** e marca os **gatilhos** (as palavras que a banca trocaria); depois, com o artigo escondido, escolhe a alternativa que reproduz a regra sem deturpação |
| 3 | Núcleo | Acha quem, deve/pode, o quê, em dispositivos longos |
| 4 | Quem faz o quê | Liga cada atribuição ao órgão ou autoridade certa |
| 5 | Regra e exceção | Classifica partes da norma em regra, condição, exceção ou consequência |
| 6 | Números e prazos | Responde, de memória, prazos, quóruns, percentuais e limites |
| 7 | **Banca** | Itens Certo/Errado com confiança obrigatória; ao marcar Errado, aponta a palavra da troca; resultado com nota líquida e técnica de deturpação em que mais cai |
| 8 | Compreensão | Perguntas abertas: literal, aplicação (caso concreto) e sistemática |
| 9 | Glossário e notas | Termos técnicos, tabela de números da seção e observações |

- **Confere tudo o que a IA gera contra o texto da lei** antes de mostrar: o trecho de base de cada item, o número citado e a palavra trocada precisam estar lá.
- Mantém os recursos da LIO: revisão espaçada, fichamento e mapas, teste antes e depois, rodadas com índices, leitura em voz alta e ajustes de leitura, mediação de grupos, aula ao vivo e mensagens.

## Duas formas de usar

| Forma | Arquivo | Como |
|---|---|---|
| **No Claude** (versão de referência) | `lio-l.html` | Instale na sua conta do Claude: veja [INSTALAR.md](INSTALAR.md). A IA é a da sua conta; grupo, mensagens e aula ao vivo funcionam pelo próprio Claude. |
| **No navegador** (versão independente) | `index.html` | Abra o site do repositório no GitHub Pages ([https://joacyfranca.github.io/lio-l/](https://joacyfranca.github.io/lio-l/), depois de ativado). Os estudos ficam no navegador de cada pessoa; a IA usa uma chave da API da Anthropic ou o modo **copiar e colar** (a LIO-L mostra o pedido, você cola na IA que já usa — Claude, ChatGPT, Gemini — e traz a resposta de volta), escolhidos na aba Ajustes. |

A LIO-L guarda seus dados **separados** dos da LIO-E, mesmo quando as duas são usadas no mesmo navegador: estudos, atividades, pacotes e backups de uma não se misturam com os da outra.

## Formas de uso

Na primeira abertura, a LIO-L pergunta como você vai usá-la. A escolha pode ser mudada depois, no Início.

| Forma | Para quem | O que aparece |
|---|---|---|
| Estudar por conta própria | Uso principal. Cada pessoa estuda a lei do seu edital. | As abas de estudo. |
| Mediar um grupo | Quem prepara atividades para outras pessoas: professor de cursinho, tutor ou um colega. | As abas de estudo e a aba **Mediador**. |
| Participar de um grupo | Quem recebe uma atividade pronta. | As abas de estudo, sem precisar de IA. |

## Cuidados com o texto da lei

- Estude sempre o texto **compilado e atualizado**. No site do Planalto, trechos revogados aparecem tachados; ao copiar ou extrair, o tachado se perde. Confira dispositivos revogados antes de memorizá-los.
- Textos de lei são de domínio público (Lei 9.610/1998, art. 8º, IV). Material de terceiros (leis comentadas, apostilas, questões de provas) continua protegido: não o coloque neste repositório.
- Nunca coloque uma chave de API em nenhum arquivo do repositório.

## Como foi feito

Co-desenvolvimento humano–IA: concebido, especificado e validado pelo autor; código gerado pelo Claude (Anthropic) sob a direção do autor. A LIO-L é gerada a partir do código da LIO-E por um script (`fonte/gerar_lio_l.py`), para que as melhorias da LIO-E cheguem também à LIO-L. Ver [DECLARACAO_IA.md](DECLARACAO_IA.md).

## Documentação

| Documento | Conteúdo |
|---|---|
| [INSTALAR.md](INSTALAR.md) | Instalar, atualizar e usar uma LIO-L compartilhada no Claude |
| [METODOLOGIA.md](METODOLOGIA.md) | O método de leitura de lei seca e como cada etapa o aplica |
| [Manual de utilização](docs/Manual_de_Utilizacao_LIO-L.pdf) | Como estudar, participar e mediar, tela a tela |
| [Documentação técnica](docs/Documentacao_Tecnica_LIO-L.pdf) | Como a LIO-L funciona por dentro: leitor estrutural, geração e verificação, dados, versões |
| [fonte/LEIA-ME.md](fonte/LEIA-ME.md) | Como gerar a LIO-L e a versão independente a partir do código-fonte |
| [DECLARACAO_IA.md](DECLARACAO_IA.md) e [REGISTRO_DESENVOLVIMENTO.md](REGISTRO_DESENVOLVIMENTO.md) | Como a LIO-L foi feita |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Como relatar erros e sugerir melhorias |

## Estrutura do repositório

```
lio-l/
├── lio-l.html                 versão para Claude (instalar como artefato)
├── index.html                 versão independente (GitHub Pages)
├── README.md · INSTALAR.md · METODOLOGIA.md · CONTRIBUTING.md
├── DECLARACAO_IA.md · REGISTRO_DESENVOLVIMENTO.md
├── LICENSE (código, AGPL-3.0) · LICENSE-TEXTOS (textos, CC BY 4.0)
├── docs/                      logo, manual e documentação técnica (PDF)
├── fonte/                     gerador da LIO-L, montagem da versão independente
│   └── base/lio-e.html        código da LIO-E usado como base
└── .github/ISSUE_TEMPLATE/    modelos de Erro e Sugestão
```

## Licença

| O quê | Licença | Arquivo |
|---|---|---|
| Código: `lio-l.html`, `index.html` e tudo em `fonte/` | **GNU AGPL 3.0 ou posterior** (AGPL-3.0-or-later) | `LICENSE` |
| Textos e documentação: README, INSTALAR, METODOLOGIA, CONTRIBUTING, Declaração de IA, Registro de desenvolvimento, Manual e Documentação Técnica | **Creative Commons Atribuição 4.0** (CC BY 4.0) | `LICENSE-TEXTOS` |
| Logo da LIO-L (`docs/lio_l_logo.png`) | Identidade visual do projeto; uso para indicar a LIO-L oficial | — |

Copyright © 2026 Joacy Raimundo França. Código gerado por IA sob a direção do autor (ver `DECLARACAO_IA.md`).

Em resumo: você pode usar, estudar, copiar e modificar a LIO-L. Se distribuir uma versão modificada do código, inclusive como serviço on-line, precisa manter os créditos e oferecer o código-fonte dessa versão sob a mesma licença. Ao reutilizar os textos, cite a autoria e indique se fez alterações. Pedimos ainda que versões modificadas deixem claro que não são a LIO-L oficial.

## Contribua

- **Dê sua opinião:** [formulário de 5 minutos](https://docs.google.com/forms/d/e/1FAIpQLSfgBYt45TQsZMBL3DV7KHX-LgpnLY-RDb17_6ggDfYdwDai4Q/viewform), sem login (o mesmo da família LIO; diga que usou a LIO-L).
- **Encontrou um erro ou tem uma ideia?** Abra uma [Issue](https://github.com/JOACYFRANCA/lio-l/issues/new/choose) com o modelo **Erro** ou **Sugestão**.
- Veja como as contribuições são tratadas em [CONTRIBUTING.md](CONTRIBUTING.md).

---

**Autor:** Joacy Raimundo França · LIO-L beta 1 · 14/10/2026
