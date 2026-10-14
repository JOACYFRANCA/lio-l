# Registro de desenvolvimento · LIO-L

Este arquivo registra como a LIO-L foi construída, no mesmo formato do registro da LIO-E. Uma linha por pedido relevante.

- **Pedido:** em uma frase, o que o autor pediu à IA.
- **Resultado:** o que a IA entregou, incluindo erros.
- **Decisão:** aceitou, pediu correção, desistiu ou mudou o plano.
- **Datas:** sempre no formato AAAA-MM-DD.

---

## Versão para Claude

**Plataforma:** claude.ai · **Modelo:** Claude Opus 5.5 · **Conta:** pessoal do autor ( plano Pro)· **Período:** 2026-10-14 · **Versão:** beta 1 (base: LIO-E v29)

| Data | Versão | Pedido do autor | Resultado da IA | Decisão | Tempo (min) | Evidência |
|---|---|---|---|---|---|---|
| 2026-10-14 | — | Em teste, a LIO não rendia em leis ("tudo é importante, não há parágrafos densos"); atuar como especialista em leis e bancas e propor uma metodologia que mantenha a leitura inteligente | Diagnóstico (texto denso pede selecionar; lei pede discriminar), três camadas de leitura, etapas da LIO transpostas para a lei, modo banca com técnicas de deturpação, confiança como estratégia de prova, indicadores e cuidados (vigência, verificação, incidência) | Aceitou e pediu a construção | — | Conversa no claude.ai |
| 2026-10-14 | LIO-E v28 | Na leitura ativa, botão para ver todo o texto da seção (p. 4–9) e navegação livre entre os "traços" (hoje só dá para pular) | Traços viram botões (ir a qualquer parágrafo; azul quando há etiqueta; círculo final leva ao resumo), botão "◀ Parágrafo anterior", "Ver a seção inteira" com páginas marcadas, parágrafo atual destacado e toque para estudar; testado em navegador sem interface | Aceitou | — | Conversa no claude.ai |
| 2026-10-14 | LIO-L beta 1 | Construir a LIO-L (nome dado pelo autor; LIO-E é o nome extraoficial da LIO original, pensando numa família de LIOs) | Gerador `gerar_lio_l.py` a partir da LIO-E; leitor estrutural (artigo como unidade, títulos, rubricas, penas, anotações do Planalto, artigos longos partidos); nove etapas, com Números e prazos e Banca novas; pedidos à IA de professor de cursinho, só com a lei; verificação de cada item contra o texto; dados separados da LIO-E; testado com trecho do art. 37 da CF e exercícios simulados | Aceitou para teste | — | Conversa no claude.ai |
| 2026-10-14 | LIO-E v29 | Erro relatado: todo pedido de exercícios ou de questões voltava à tela com "Preparar exercícios", sem exercícios | Teste com resposta simulada mostrou a geração funcionando; ponto fraco encontrado: quando o próprio Claude interrompia o pedido, a LIO tratava como "Parar" e voltava calada. Correção: toda falha mostra o motivo e o código do erro, nos exercícios, nas perguntas, no teste e no treino. Causa original ainda a confirmar no teste do autor | Aceitou | — | Conversa no claude.ai |
| 2026-10-14 | — | Mostrar o HTML para teste | Cópias de teste publicadas na conta do autor (LIO-E v29 e LIO-L beta 1), com as permissões do INSTALAR | Aceitou | — | Conversa no claude.ai |
| 2026-10-14 | LIO-L beta 1 | Gerar o repositório completo, com toda a documentação, autor Joacy Raimundo França; acrescentar o L no logo, conforme imagem enviada | Logo LIO-L aplicado no cabeçalho e no Início (fundo transparente); textos do Início adaptados; repositório com README, INSTALAR, METODOLOGIA, CONTRIBUTING, Declaração de IA, este registro, licenças, modelos de Issue, código-fonte reproduzível (`fonte/`), manual e documentação técnica em PDF | Em revisão pelo autor | — | Conversa no claude.ai |

---

## Versões para ChatGPT e Gemini

Planejadas. Seguem as versões da LIO-E para cada plataforma. O registro será preenchido no mesmo formato.

| Data | Versão | Pedido do autor | Resultado da IA | Decisão | Tempo (min) | Evidência |
|---|---|---|---|---|---|---|
| | | | | | | |
