# Código-fonte da LIO-L

A LIO-L é **gerada** a partir do código da LIO-E (a LIO original, para textos densos), para que toda melhoria feita na LIO-E chegue também à LIO-L. Os dois arquivos publicados na raiz do repositório saem desta pasta.

| Arquivo | O que é |
|---|---|
| `base/lio-e.html` | Código da LIO-E usado como base (versão 29). Vem do repositório [JOACYFRANCA/lio](https://github.com/JOACYFRANCA/lio) |
| `gerar_lio_l.py` | Gera `../lio-l.html` (versão para Claude) a partir de `base/lio-e.html` |
| `lio_l_logo.webp` | Logo da LIO-L embutido na página pelo gerador |
| `build.py` | Monta a versão independente (navegador) a partir da versão para Claude |
| `local_parts.js` | Camada de capacidades da versão independente: banco local (IndexedDB), chave e chamadas à API da Anthropic, modo copiar e colar, downloads, formas de uso |
| `local_config.js` | Aba Ajustes da versão independente |

## Gerar os arquivos publicados

Precisa só do Python 3, sem bibliotecas extras.

```
cd fonte
python3 gerar_lio_l.py          # gera ../lio-l.html
python3 build.py ../lio-l.html  # gera lio-l-local.html
```

Renomeie `lio-l-local.html` para `index.html` e substitua o da raiz do repositório. Os arquivos gerados devem ser idênticos aos publicados: é assim que se confere que eles saem deste código.

## O que o gerador muda na LIO-E

| Parte | Mudança |
|---|---|
| Identidade | Título, logo LIO-L, etiqueta de versão "LIO-L · beta 1 (base vNN)", textos do Início |
| Dados | Prefixo do armazenamento do navegador (`lil_`), identificador de atividades, pacotes e backups (`lio-leis`) e nome do banco local: a LIO-L nunca lê nem grava os dados da LIO-E |
| Leitor estrutural | `estruturarLei()`: junta linhas quebradas, reconhece Art., §, Parágrafo único, incisos, alíneas e penas, títulos (Livro, Título, Capítulo, Seção, Subseção), rubricas e anotações do texto compilado; agrupa por artigo; parte artigos com mais de 2.400 caracteres entre incisos ou parágrafos |
| Etapas | Mapa topográfico, Leitura do artigo (regra em uma frase e marca-gatilhos), Núcleo, Quem faz o quê, Regra e exceção, Números e prazos, Banca, Compreensão (literal, aplicação, sistemática), Glossário e notas |
| Pedidos à IA | Exercícios, regra e gatilhos, perguntas, retorno e teste escritos para lei seca, proibindo jurisprudência, doutrina e outras leis |
| Verificação | `validar()` da LIO-L descarta itens cujo trecho de base, número ou palavra trocada não confere com o texto |
| Índices | Banca entra no índice de compreensão; Detecção de gatilhos substitui a Localização da ideia |

## Quando a LIO-E mudar

1. Copie o `lio.html` novo da LIO-E para `base/lio-e.html`.
2. Rode `python3 gerar_lio_l.py`.
3. Se o script parar com um erro que mostra o início de um trecho, aquele ponto mudou na LIO-E: ajuste a troca correspondente no `gerar_lio_l.py` para o texto novo.
4. Rode `python3 build.py ../lio-l.html` e teste as duas versões.

## Publicar a versão do Claude

Veja `INSTALAR.md`, na raiz do repositório.

## Licença

Código sob GNU AGPL 3.0 ou posterior (arquivo `LICENSE`); textos sob CC BY 4.0 (arquivo `LICENSE-TEXTOS`). Copyright © 2026 Joacy Raimundo França.
