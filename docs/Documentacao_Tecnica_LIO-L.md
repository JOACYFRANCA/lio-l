# LIO-L · Documentação técnica

**Leitura Inteligente Orientada de Leis** · beta 1 · 14/10/2026 · Autor: Joacy Raimundo França

Este documento explica como a LIO-L funciona por dentro: de onde vem o código, como a lei é separada em artigos, como os exercícios são pedidos à IA e conferidos, onde os dados ficam e como reproduzir os arquivos publicados.

## 1. Visão geral

A LIO-L é uma página única (HTML, CSS e JavaScript num só arquivo), sem servidor próprio, com duas formas de execução:

| Forma | Arquivo | IA | Dados |
|---|---|---|---|
| Versão para Claude (referência) | `lio-l.html` | `sample` do Claude, na conta de quem usa | `db` do artefato (privado por pessoa; atividades e grupo compartilhados por regras de acesso) |
| Versão independente | `index.html` | Chave da API da Anthropic ou modo copiar e colar | IndexedDB do navegador |

As duas usam o mesmo código de estudo. A versão independente é montada a partir da versão para Claude pelo `fonte/build.py`, que troca a camada de capacidades (`fonte/local_parts.js`) e acrescenta a aba Ajustes (`fonte/local_config.js`).

## 2. De onde vem o código: geração a partir da LIO-E

A LIO-L não é mantida à mão. O script `fonte/gerar_lio_l.py` lê o código da LIO-E (`fonte/base/lio-e.html`) e aplica trocas de trechos exatos, em grupos:

| Grupo | O que muda |
|---|---|
| Identidade | Título, logo (cabeçalho e Início), etiqueta "LIO-L · beta 1 (base vNN)", cabeçalho de copyright do arquivo, textos do Início |
| Isolamento de dados | Prefixo do armazenamento do navegador `olh_` → `lil_`; identificador `"oficina-leitura"` → `"lio-leis"` em atividades, pacotes, relatórios, backups e no banco IndexedDB |
| Leitor estrutural | Funções `estruturarLei`, `partesLei`, `rotuloArt`, `rotuloUnid`, chamadas no início de `seccionar`; texto colado passa a ser lido linha a linha; a revisão do texto extraído preserva as quebras de linha |
| Etapas | `passos`, `PRECISA_GEN`, `SEM_MATERIAL`, `ETAPAS`, despacho de `estSecao`, `passoFeito`; funções novas `pNumeros`, `tabelaNumeros`, `pBanca`, `fecharItem`, `resumoBanca`, `bancaFim` |
| Pedidos à IA | `promptSecao`, `promptEtq`, `lerEtqIA`, `promptPerg`, `promptFeedback`, `promptTeste`, glossário |
| Verificação | `validar` próprio da LIO-L |
| Estrutura da norma | `PAPEIS` vira Regra, Condição, Exceção, Consequência (o treino continua com `PAPEIS_T`, os papéis do texto acadêmico); `mapaArg` e `mapaVozes` redesenhados |
| Revisão do mediador | Rótulos e grupos novos para Números e prazos e Banca, com leitura e conferência ao salvar |
| Revisão espaçada e fichamento | Cartões de regra, quem faz o quê, números e itens de banca errados ou em branco; fichamento com competências, números, banca e estrutura da norma |
| Índices | `COMP_ROT` e `indicesDe` com a Banca; "Localização da ideia" → "Detecção de gatilhos" |

Cada troca confere que o trecho original existe o número de vezes esperado; se não existir, o script para e mostra o início do trecho. Assim, uma mudança na LIO-E nunca passa despercebida na LIO-L.

```
cd fonte
python3 gerar_lio_l.py          # → ../lio-l.html
python3 build.py ../lio-l.html  # → lio-l-local.html (renomear para ../index.html)
```

Os arquivos gerados são idênticos, byte a byte, aos publicados.

## 3. Leitor estrutural de leis

### 3.1 Entrada

O texto chega por três caminhos: PDF (extração por página com pdf.js e análise de blocos da LIO-E), Word (.docx, via mammoth) ou texto colado. Antes de dividir em seções, `seccionar()` chama `estruturarLei(pars)`, que recebe a lista de blocos `{t, pg, h?}` (texto, página, título?).

Se nenhum bloco contém "Art. N" no começo de um dispositivo, o texto não é tratado como lei e passa sem mudança.

### 3.2 Marcadores

A expressão `RX_MARCA` reconhece o início de um dispositivo:

| Marcador | Exemplos |
|---|---|
| Artigo | `Art. 1º`, `Art. 10.`, `Art. 1.048`, `Art. 5º-A` |
| Parágrafo | `§ 1º`, `§ 12.`, `Parágrafo único.` |
| Inciso | `I -`, `XIV –`, `IV-A -` |
| Alínea | `a)`, `b)` |
| Pena | `Pena -` |

Um marcador só abre um dispositivo novo quando está no começo do bloco ou vem depois de `.`, `;`, `:` ou `)`. Assim, referências no meio da frase ("nos termos do art. 6º", "o inciso I do § 2º") não partem o texto. Incisos precedidos de "inciso", "item" ou "alínea" também não partem.

### 3.3 Títulos, rubricas e anotações

- **Títulos estruturais** (`RX_EST`): Livro, Título, Capítulo, Seção, Subseção, Parte, seguidos de numeral romano, número, "Único", "Geral" ou "Especial". A linha seguinte em caixa alta (o nome do capítulo) é juntada: "CAPÍTULO VII · DA ADMINISTRAÇÃO PÚBLICA".
- **Rubricas**: linha curta, começando com maiúscula, sem pontuação final e sem caixa alta, depois de um dispositivo encerrado. Se o próximo bloco é um artigo, vira `rub` dele; se não, entra como linha do artigo atual.
- **Anotações do texto compilado** (`RX_ANOT`): "(Redação dada…)", "(Incluído…)", "(Vide…)", "(Vigência)", "(Regulamento)" e semelhantes saem do texto e vão para `ann`. "(Revogado)" e "(VETADO)" ficam no texto, porque informam o conteúdo.

### 3.4 Agrupamento e artigos longos

Cada artigo vira uma unidade `{t, pg, art, rub?, ann?, parte?}`, com os dispositivos separados por quebra de linha. Um bloco que não começa com marcador é continuação da linha anterior (linha quebrada ou mudança de página) e é juntado com espaço.

Artigos com mais de 2.400 caracteres são partidos antes de um inciso ou parágrafo, depois de pelo menos 1.500 caracteres. Cada parte recebe `parte` ("caput até XIV · parte 1 de 3", "XV a XXVIII · parte 2 de 3").

A função é idempotente: aplicada a um texto já estruturado, produz o mesmo resultado, o que permite corrigir o texto em "Revisar o texto extraído" e aplicar de novo.

## 4. Pedidos à IA e verificação

### 4.1 Exercícios da seção

`promptSecao` pede um único JSON, com o papel de professor de cursinho que conhece as bancas, usando SOMENTE o trecho de lei e proibindo jurisprudência, doutrina e outras leis. Cada unidade vai numerada (`[P3] (p. 1) [rubrica] texto`).

| Campo | Conteúdo | Verificação em `validar()` |
|---|---|---|
| `ideias` | Por artigo: a regra (até 25 palavras) e duas deturpações | Parágrafo válido; duas erradas |
| `labirinto` | Dispositivos longos copiados exatamente, núcleo e duas distrações | Dispositivo presente no texto; 70% das palavras do núcleo no dispositivo |
| `competencias` | Sujeitos e atribuições | Nome do sujeito presente no texto; pelo menos dois sujeitos com atribuição |
| `estrutura` | Regra, condição, exceção, consequência | Ao menos uma regra e um item de outro papel |
| `numeros` | Campo, expressão exata e duas trocas | Expressão presente no texto; nenhuma errada igual à certa |
| `banca` | 8 a 12 itens C/E, técnica, troca, correto, base | Base presente no texto; num item errado, troca presente no item e técnica diferente de paráfrase fiel |
| `termos` | Termos e o sentido nesta lei | Termo presente no texto |

Itens descartados são contados; a página informa quantos ("2 itens descartados por não conferir com o texto"). O pedido usa `cache: false` (cada clique pede de novo).

### 4.2 Regra e gatilhos

`promptEtq` pede duas linhas: `ETIQUETA` (a regra, até 20 palavras) e `GATILHOS` (3 a 8 expressões exatas, separadas por "|"). `gatIdx()` procura cada expressão no artigo, palavra por palavra, e marca todas as ocorrências. A **Detecção de gatilhos** é `coincidências ÷ (marcadas pelo estudante ∪ marcadas pela IA)`, calculada sobre a marcação feita antes da primeira comparação.

### 4.3 Banca

`pBanca` guarda em `resp.banca.it[k]` a resposta (`C`, `E`, `B`), a confiança (3, 2, 1), as palavras apontadas, se acertou e se apontou a troca (`trocaIdx`, a sequência de palavras da troca dentro do item). `resumoBanca` calcula certos, errados, brancos e a nota líquida; `bancaFim` agrega por confiança e por técnica. Para o índice de compreensão, entra `{c: certos, t: itens}`.

### 4.4 Falhas

Toda chamada à IA trata a rejeição do `sample`. A partir da LIO-E v29, só um "cancelled" provocado pelo botão **Parar** é silencioso; uma interrupção vinda da plataforma aparece como erro. Cada código tem uma mensagem própria, e códigos desconhecidos aparecem entre parênteses. O código também vai para o console do navegador (`avisoIA`).

## 5. Dados

### 5.1 Versão para Claude

| Coleção | Conteúdo | Quem lê e grava |
|---|---|---|
| `data/users/<id>/` | Estudos, seções (`pars`, `gen`, `perg`, `resp`), revisão, perfil, registro de uso | Só a própria pessoa |
| `atividades` | Atividades publicadas pelo mediador | Todos leem; só o dono grava |
| `entregas`, `entregas/{self}` | Progresso compartilhado com o mediador | O participante grava o seu; o dono lê |
| `aula` | Estado da aula ao vivo | Todos leem; só o dono grava |
| `msg/...` | Mensagens do grupo | Conforme as regras do INSTALAR |

As permissões declaradas na publicação estão em `INSTALAR.md`. Uma seção guarda o texto (`pars`, com `art`, `rub`, `ann`, `parte`), os exercícios (`gen`, com `ideias`, `lab`, `vozes`, `arg`, `num`, `banca`, `termos`), as perguntas (`perg`) e as respostas (`resp`, com `etq`, `marc`, `ide`, `frases`, `vozes`, `arg`, `crono` para números, `banca`, `perg`, `gloss`, `obs`).

### 5.2 Versão independente

Banco IndexedDB `lio-leis`, com a mesma estrutura de documentos. Preferências no `localStorage` com o prefixo `lil_`. Backups exportados e importados na aba Ajustes, com o identificador `lio-leis`, que não aceita backups da LIO-E.

## 6. Acessibilidade

Herdada da LIO-E: ajustes de letra, entrelinhas, espaçamento, largura de linha, fontes para leitura (Atkinson Hyperlegible, Lexend), paletas de alto contraste, leitura em voz alta com destaque da frase, modo foco. Na LIO-L, os traços de navegação são botões com rótulo (o artigo, a página e a regra escrita, quando houver), e cada dispositivo fica numa linha.

## 7. Testes feitos nesta versão

| Teste | Como | Resultado |
|---|---|---|
| Leitor estrutural | Trecho do art. 37, 38 e 41 da CF colado com linhas quebradas e anotações; artigo com rubrica, pena e parágrafo com rubrica; artigo com 40 incisos; referências cruzadas | Artigos, títulos, rubricas, penas e anotações reconhecidos; artigo longo em 3 partes; referências não partiram o texto |
| Etapas | Navegador sem interface (Chromium), com exercícios simulados no formato da IA | Leitura, navegação pelos traços, seção inteira, núcleo, quem faz o quê, regra e exceção, números, banca (com apontamento e resultado) sem erros de JavaScript |
| Verificação | Item com trecho de base inventado | Descartado |
| Revisão do mediador | Edição de um item de banca que tirou a troca do texto | Item retirado ao salvar; os demais mantidos |
| Cartões e fichamento | Seção com exercícios e banca respondida | Cartões de quem faz o quê, números e banca; fichamento com as seções novas |
| Reprodutibilidade | `gerar_lio_l.py` e `build.py` no repositório | Arquivos idênticos aos publicados |
| Isolamento | Busca do identificador da LIO-E na versão independente da LIO-L | Nenhuma ocorrência |

A preparação real de exercícios na conta do Claude é o teste de aceitação do autor.

## 8. Histórico

| Data | Versão | Mudança |
|---|---|---|
| 2026-10-14 | LIO-E v28 | Navegação livre pelos traços da leitura ativa; texto inteiro da seção |
| 2026-10-14 | LIO-L beta 1 | Primeira versão: gerador, leitor estrutural, nove etapas, Banca, Números e prazos, pedidos e verificação para lei seca, dados separados |
| 2026-10-14 | LIO-E v29 | Falhas ao falar com o Claude deixam de ser silenciosas e mostram o código; plural correto dos papéis |
| 2026-10-14 | LIO-L beta 1 | Logo LIO-L; Início; revisão do mediador com Números e Banca; cartões e fichamento para lei; repositório e documentação |

---

LIO-L · © 2026 Joacy Raimundo França · Texto sob CC BY 4.0 · Código sob AGPL-3.0-or-later
