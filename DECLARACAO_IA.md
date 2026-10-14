# Declaração de autoria e de uso de IA

**Projeto:** LIO-L · Leitura Inteligente Orientada de Leis (família LIO)
**Autor:** Joacy Raimundo França
**Modelo de desenvolvimento:** co-desenvolvimento humano–IA

## Resumo

A LIO-L foi concebida, especificada e validada por **Joacy Raimundo França**. O código é gerado por um agente de IA, no ambiente da própria plataforma, sob a direção do autor.

A LIO-L é a segunda ferramenta da **família LIO**. A primeira, a LIO-E (Educacional, para textos densos), está em [github.com/JOACYFRANCA/lio](https://github.com/JOACYFRANCA/lio). A LIO-L não é escrita do zero: o script `fonte/gerar_lio_l.py` gera a LIO-L a partir do código da LIO-E, trocando o leitor de texto pelo leitor estrutural de leis, as etapas de estudo, os pedidos à IA e os textos da interface. Assim, cada melhoria da LIO-E chega à LIO-L na geração seguinte, e o registro do co-desenvolvimento das duas fica ligado.

O projeto não reivindica programação manual do autor. A autoria está na concepção, no desenho pedagógico, na especificação, nas decisões de cada versão, nos testes e na curadoria do resultado. O autor responde pelo projeto como um todo, inclusive pela segurança e pela exatidão do conteúdo.

## Objetivos do projeto

1. **Ferramenta de estudo:** um método de estudo ativo de lei seca, com a IA que o usuário já tem, para concurseiros, estudantes de Direito e quem precisa conhecer uma norma a fundo.
2. **Demonstração:** mostrar que é possível construir uma família de ferramentas educacionais em co-desenvolvimento humano–IA, derivando uma da outra de forma registrada e reproduzível.

## Papéis

| Atividade | Autor | Agente de IA |
|---|---|---|
| Ideia da LIO-L e diagnóstico do problema (a LIO não rendia em leis) | Identificou em teste e definiu | — |
| Metodologia de leitura de lei (METODOLOGIA.md) | Pediu, com o papel de especialista em leis e bancas, e aprovou | Propôs o método, as técnicas de deturpação e os indicadores |
| Nome (LIO-L; LIO-E como nome extraoficial da LIO original) e logo | Escolheu e forneceu a imagem do logo | Aplicou no código e na documentação |
| Melhorias da LIO-E usadas pela LIO-L (texto inteiro da seção, navegação pelos traços) | Pediu e aprovou | Implementou |
| Código da LIO-L (gerador, leitor estrutural, etapas, pedidos à IA) | Não escreveu | Escreveu, testou e corrigiu |
| Testes automáticos (navegador sem interface, respostas simuladas da IA) | Definiu o que precisava funcionar | Escreveu e executou |
| Testes de uso e aceitação na conta do Claude | Executa e decide | Apoia com relatórios |
| Documentação | Revisa e aprova | Redigiu |
| Decisões de publicação, licença e privacidade | Decide | Informou opções e riscos |

## Situação das versões

| Versão | Situação | Base |
|---|---|---|
| Claude | Beta 1 (14/10/2026) | LIO-E versão 29 |
| ChatGPT | Planejada: segue a versão da LIO-E para ChatGPT | — |
| Gemini | Planejada: segue a versão da LIO-E para Gemini | — |

## Versão para Claude

- **Plataforma:** claude.ai (artefatos e sessão com ferramentas de código), da Anthropic
- **Modelo:** Claude Opus 5.5 (família Claude 5)
- **Conta usada:** conta pessoal do autor no claude.ai(plano Pro)
- **Período:** 14 de outubro de 2026
- **Versão:** beta 1, gerada da LIO-E versão 29
- **Registro do processo:** `REGISTRO_DESENVOLVIMENTO.md` e Documentação Técnica, seção "Histórico"

## Como a LIO-L é gerada e conferida

- O código da LIO-E usado como base está em `fonte/base/lio-e.html`. Rodar `python3 gerar_lio_l.py` na pasta `fonte` produz exatamente o `lio-l.html` publicado; rodar `python3 build.py ../lio-l.html` produz a versão independente (`index.html`). Qualquer pessoa pode conferir que os arquivos publicados saem do código-fonte.
- O gerador troca trechos exatos e para com erro se um trecho esperado não existir na base, para que uma mudança na LIO-E nunca passe despercebida.
- O cabeçalho do `lio-l.html` informa a versão da LIO-E de que ele foi gerado.

## Uso de IA dentro da LIO-L

Além de ter sido feita com IA, a LIO-L usa IA durante o estudo:

- prepara exercícios, itens de banca e perguntas;
- dá retorno sobre as respostas abertas;
- explica trechos difíceis;
- sugere a regra do artigo e os gatilhos.

A IA é sempre chamada por um botão do usuário. Cada pedido envia só o trecho de lei necessário e proíbe jurisprudência, doutrina e outras leis. Todo item gerado é conferido contra o texto antes de ser usado: o trecho de base precisa estar na lei, a palavra trocada precisa estar no item, e o número citado precisa aparecer no texto. Itens que não passam são descartados, e a LIO-L informa quantos.

## Uso acadêmico

A LIO-L é um projeto independente. Se vier a ser objeto ou ferramenta de um trabalho acadêmico, esta declaração serve como registro público e datado do uso de IA no desenvolvimento.

## Observação sobre direitos

A autoria aqui declarada é a do projeto: concepção, especificação, desenho pedagógico e curadoria. A situação jurídica de código gerado por IA ainda não está pacificada. Por isso, a origem do código é informada de forma explícita, e o uso do projeto segue as licenças indicadas nos arquivos LICENSE (código: GNU AGPL 3.0 ou posterior) e LICENSE-TEXTOS (textos e documentação: CC BY 4.0).

## Histórico desta declaração

| Data | Mudança |
|---|---|
| 2026-10-14 | Primeira versão, com a publicação da LIO-L beta 1 (versão para Claude, gerada da LIO-E v29) |
