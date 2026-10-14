# Gera a LIO-L (LIO para leitura de leis) a partir do código-fonte da LIO-E.
# Copyright (C) 2026 Joacy Raimundo França · AGPL-3.0-or-later (ver LICENSE)
#
# Uso, dentro da pasta fonte:  python3 gerar_lio_l.py   →  ../lio-l.html
# Fonte da LIO-E: base/lio-e.html (no repositório da LIO-L) ou ../lio.html (no repositório da LIO).
# Como o build.py, troca trechos exatos. Se o código da LIO-E mudar num ponto trocado aqui,
# o script para e mostra o início do trecho que não encontrou.
import os, re, base64
_aqui = os.path.dirname(os.path.abspath(__file__))
_cands = [os.path.join(_aqui, 'base', 'lio-e.html'), os.path.join(_aqui, '..', 'lio.html')]
_src = next(c for c in _cands if os.path.exists(c))
_out = os.path.join(_aqui, '..', 'lio-l.html')
_logo = 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(_aqui, 'lio_l_logo.webp'), 'rb').read()).decode()
s = open(_src, encoding='utf-8').read()

def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:80])
    s = s.replace(a, b)

def rep_all(a, b):
    global s
    assert a in s, ('nenhum', a[:80])
    s = s.replace(a, b)

def region(a, b):
    i = s.index(a); j = s.index(b, i)
    return i, j

def rep_region(a, b, new):
    global s
    i, j = region(a, b)
    s = s[:i] + new + s[j:]

def sub_in_region(a, b, pairs):
    """Trocas feitas só entre os marcadores a e b."""
    global s
    i, j = region(a, b)
    r = s[i:j]
    for x, y in pairs:
        assert x in r, ('regiao', a[:30], x[:60])
        r = r.replace(x, y)
    s = s[:i] + r + s[j:]

# ------------------------------------------------------------------ identidade
rep('<title>LIO · Leitura Inteligente Orientada</title>', '<title>LIO-L · Leitura Inteligente Orientada de Leis</title>')
rep('<span class="brand-t">Leitura Inteligente Orientada</span>', '<span class="brand-t">Leitura Inteligente Orientada <span class="lio-l">· Leis</span></span>')
s = re.sub(r'>beta · v(\d+)<', lambda m: '>LIO-L · beta 1 (base v%s)<' % m.group(1), s, count=1)
rep('<p class="lead">Leia textos densos por partes, guarde o que importa e acompanhe a sua evolução a cada rodada.</p>',
    '<p class="lead">Leia leis artigo por artigo, ache as palavras que a banca troca e treine com itens no estilo da prova.</p>')
rep_all('"olh_"', '"lil_"')                    # armazenamento local separado da LIO-E
rep_all('"oficina-leitura"', '"lio-leis"')     # atividades e pacotes da LIO-L não se misturam com os da LIO-E
rep_all('Localização da ideia', 'Detecção de gatilhos')


# logo da LIO-L (as duas imagens: cabeçalho e Início)
s = re.sub(r'(<img class="lio-logo" src=")data:image/webp;base64,[A-Za-z0-9+/=]+(" alt=")LIO(" width=")68(" height="40">)',
           lambda m: m.group(1) + _logo + m.group(2) + 'LIO-L' + m.group(3) + '100' + m.group(4), s, count=1)
assert 'alt="LIO-L"' in s, 'logo do cabeçalho não trocado'
s, _n = re.subn(r'LIO_LOGO="[A-Za-z0-9+/=]+"', 'LIO_LOGO="' + _logo.split(',', 1)[1] + '"', s, count=1)
assert _n == 1, 'constante LIO_LOGO não encontrada'
rep('alt="LIO · Leitura Inteligente Orientada" width="440" height="316"', 'alt="LIO-L · Leitura Inteligente Orientada de Leis" width="370" height="148"')
# cabeçalho do código
_m = re.search(r'<!--\n  LIO · Leitura Inteligente Orientada — versão para Claude \(artefato do claude.ai\)\n  Versão (\d+) \(beta\)[^\n]*\n', s)
assert _m, 'cabeçalho do código não encontrado'
s = s.replace(_m.group(0), '<!--\n  LIO-L · Leitura Inteligente Orientada de Leis — versão para Claude (artefato do claude.ai)\n'
              '  Beta 1 · 14/10/2026 · gerada a partir da LIO-E versão %s por fonte/gerar_lio_l.py\n' % _m.group(1), 1)

# ------------------------------------------------------------------ CSS
s = s.replace('</style>\n', '''
/* ---- LIO-L ---- */
.lio-l{font-weight:700;color:var(--accent)}
.passage p{white-space:pre-line}
.secinteira .sp{white-space:pre-line}
.rubrica{font-family:var(--f-ui);font-size:.85rem;font-weight:600;color:var(--muted);margin:0 0 4px}
.ann{font-family:var(--f-ui);font-size:.75rem;color:var(--muted)}
.ce{display:flex;gap:8px;flex-wrap:wrap}
.ce .btn{min-width:7rem}
.confs{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.item-ce{text-align:left;word-spacing:normal;font-family:var(--f-read);font-size:var(--read-size);line-height:var(--read-lh)}
.item-ce .tk{border-radius:3px;cursor:pointer;padding:0 1px}
.item-ce .tk:hover{background:var(--accent-soft)}
.item-ce .tk.sel{background:var(--mk-u);outline:1px solid var(--line)}
.item-ce .tk.troca{background:var(--mk-a);box-shadow:inset 0 -2px 0 var(--mk-a-l)}
.item-ce.apontar .tk{text-decoration:underline dotted var(--line)}
.tecn{display:inline-block;font:600 .72rem var(--f-ui);letter-spacing:.04em;text-transform:uppercase;color:var(--accent);background:var(--accent-soft);border-radius:999px;padding:2px 8px}
.placar{display:grid;grid-template-columns:repeat(auto-fit,minmax(8rem,1fr));gap:8px}
.placar .stat b{font-size:1.4rem}
.comp-map{display:grid;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr));gap:10px}
.comp-map .cm{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--surface)}
.comp-map .cm b{display:block;font-family:var(--f-ui);margin-bottom:4px;color:var(--accent)}
.comp-map .cm p{margin:.3em 0;font-size:.92rem}
.tabnum{width:100%;border-collapse:collapse;font-size:.92rem}
.tabnum td,.tabnum th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
.tabnum td.v{font-weight:700;white-space:nowrap}
</style>
''', 1)

# ------------------------------------------------------------------ leitor estrutural de leis
LEITOR = r'''
/* ======================= LEITOR ESTRUTURAL DE LEIS (LIO-L) =======================
   Reagrupa o texto extraído em artigos: cada unidade de leitura é um artigo com o caput,
   os parágrafos, incisos e alíneas, um por linha. Títulos, capítulos e seções viram
   títulos da seção. Artigos muito longos são partidos entre incisos. */
const RX_EST=/^(LIVRO|T[ÍI]TULO|CAP[ÍI]TULO|SE[ÇC][ÃA]O|Se[çc][ãa]o|SUBSE[ÇC][ÃA]O|Subse[çc][ãa]o|PARTE)\s+([IVXLCDM]+|[ÚU]NIC[OA]|\d+|GERAL|ESPECIAL)\b/;
const RX_MARCA=/(Pena\s*[-–—]\s|Art\.\s*\d+(?:\.\d{3})*\s*(?:[º°ºo](?![a-zà-ÿ]))?(?:\s*-\s*[A-Z](?![a-zà-ÿ]))?\.?|§\s*\d+\s*(?:[º°o](?![a-zà-ÿ]))?(?:\s*-\s*[A-Z](?![a-zà-ÿ]))?\.?|Par[áa]grafo [úu]nico\.?|[IVXLCDM]+(?:\s*-\s*[A-Z])?\s*[-–—]\s|[a-z]\)\s)/g;
const RX_ANOT=/\s*\((?:Reda[çc][ãa]o dada|Inclu[íi]d[oa]|Vide|Vig[êe]ncia|Regulamento|Regulamenta[çc][ãa]o|Promulga[çc][ãa]o|Renumerad[oa]|Acrescid[oa]|Produ[çc][ãa]o de efeitos?|Convers[ãa]o|Express[ãa]o|Texto)[^()]*(?:\([^()]*\)[^()]*)*\)/gi;
function tipoMarca(m){return /^Pena/.test(m)?"pena":/^Art/.test(m)?"art":/^(§|Par)/.test(m)?"par":/^[IVXLCDM]/.test(m)?"inc":/^[a-z]\)/.test(m)?"ali":"txt"}
function partesLei(t){const out=[];let ult=0;RX_MARCA.lastIndex=0;let m;
  while((m=RX_MARCA.exec(t))){const i=m.index;if(i===0)continue;
    const antes=t.slice(0,i).replace(/\s+$/,"");const c=antes.slice(-1);
    if(!/[.;:)]/.test(c))continue;
    if(tipoMarca(m[0])==="inc"&&/\b(inciso|incisos|item|itens|al[íi]nea)\s*$/i.test(antes))continue;
    out.push(t.slice(ult,i).trim());ult=i}
  out.push(t.slice(ult).trim());
  return out.filter(Boolean).map(x=>{RX_MARCA.lastIndex=0;const mm=x.match(new RegExp("^"+RX_MARCA.source));return {t:x,k:mm?tipoMarca(mm[0]):"txt"}})}
function rotuloArt(t){const m=t.match(/^Art\.\s*(\d+(?:\.\d{3})*)\s*(?:[º°o](?![a-zà-ÿ]))?(?:\s*-\s*([A-Z])(?![a-zà-ÿ]))?/);if(!m)return "";
  const n=+String(m[1]).replace(/\./g,"");return "Art. "+m[1]+(n<10?"º":"")+(m[2]?"-"+m[2]:"")}
const eCaixaAlta=t=>{const l=t.replace(/[^A-Za-zÀ-ÿ]/g,"");return l.length>=3&&l===l.toUpperCase()};
function estruturarLei(pars){
  if(!pars||!pars.length)return pars;
  const temArt=pars.some(p=>/(^|[.;:)\n]\s*)Art\.\s*\d/.test(p.t));
  if(!temArt)return pars;                       // não parece lei: deixa como está
  const out=[];let cur=null,ultEst=null,rubPend=null;
  const fechaRub=()=>{if(rubPend&&cur){cur.t+="\n"+rubPend.t}else if(rubPend)out.push({t:rubPend.t,pg:rubPend.pg});rubPend=null};
  for(const p0 of pars){
    const pg=p0.pg;let txt=String(p0.t||"").replace(/\r/g,"");
    const anot=[];txt=txt.replace(RX_ANOT,m=>{anot.push(m.trim());return ""});
    txt=txt.replace(/[ \t]+/g," ").replace(/ *\n */g,"\n").trim();
    if(!txt){if(anot.length&&cur)cur.ann=(cur.ann||[]).concat(anot);continue}
    const um=txt.replace(/\s+/g," ");
    RX_MARCA.lastIndex=0;const comecaMarca=new RegExp("^"+RX_MARCA.source).test(um);
    // títulos estruturais (Capítulo, Seção...) e o nome que vem logo abaixo deles
    if(!comecaMarca&&RX_EST.test(um)&&um.length<160){fechaRub();ultEst={t:um,pg,h:true};out.push(ultEst);cur=null;continue}
    if(ultEst&&!comecaMarca&&um.length<140&&(eCaixaAlta(um)||p0.h)){ultEst.t+=" · "+um;continue}
    ultEst=null;
    if(!comecaMarca&&!cur&&!rubPend&&um.length<80&&!/[.;:,]$/.test(um)&&/^[A-ZÀ-Ý]/.test(um)&&!eCaixaAlta(um)&&!p0.h&&!out.some(x=>!x.h)){rubPend={t:um,pg};continue}
    if(!comecaMarca&&!cur){fechaRub();out.push(p0.h?{t:um,pg,h:true}:{t:um,pg});continue}   // epígrafe, ementa, preâmbulo
    // rubrica (ex.: "Homicídio simples") antes de um artigo
    if(!comecaMarca&&cur&&um.length<80&&!/[.;:,]$/.test(um)&&/^[A-ZÀ-Ý]/.test(um)&&/[.;:)]$/.test(cur.t.trim())){fechaRub();rubPend={t:um,pg};continue}
    const pecas=partesLei(um);
    pecas.forEach((pc,j)=>{
      if(pc.k==="art"){const r=rubPend;rubPend=null;cur={t:pc.t,pg,art:rotuloArt(pc.t)};if(r)cur.rub=r.t;else if(p0.art&&p0.rub&&j===0)cur.rub=p0.rub;out.push(cur);return}
      if(rubPend)fechaRub();
      if(!cur){out.push({t:pc.t,pg});cur=out[out.length-1];return}
      if(pc.k==="txt"&&j===0)cur.t=joinL(cur.t,pc.t);   // continuação de linha ou de página
      else cur.t+="\n"+pc.t});
    if(anot.length&&cur)cur.ann=(cur.ann||[]).concat(anot);
  }
  fechaRub();
  // artigos longos: partir entre incisos ou parágrafos
  const fin=[];
  for(const p of out){if(p.h||!p.art||p.t.length<=2400){fin.push(p);continue}
    const L=p.t.split("\n"),blocos=[];let b=[],tam=0;
    for(const l of L){const quebra=/^([IVXLCDM]+(\s*-\s*[A-Z])?\s*[-–—]|§|Par[áa]grafo)/.test(l);
      if(b.length&&quebra&&tam>=1500){blocos.push(b);b=[];tam=0}b.push(l);tam+=l.length}
    if(b.length)blocos.push(b);
    if(blocos.length<2){fin.push(p);continue}
    blocos.forEach((bl,k)=>{const prim=bl[0].match(/^([IVXLCDM]+(?:\s*-\s*[A-Z])?|§\s*\d+\s*[º°o]?|Par[áa]grafo [úu]nico)/),ult=bl[bl.length-1].match(/^([IVXLCDM]+(?:\s*-\s*[A-Z])?|§\s*\d+\s*[º°o]?|Par[áa]grafo [úu]nico)/);
      const parte=k===0?"caput"+(ult&&ult[1]!==prim?.[1]?" até "+ult[1]:""):(prim?prim[1].replace(/\s+/g," "):"continuação")+(ult&&prim&&ult[1]!==prim[1]?" a "+ult[1].replace(/\s+/g," "):"");
      const o={t:bl.join("\n"),pg:p.pg,art:p.art,parte:parte+` · parte ${k+1} de ${blocos.length}`};if(k===0&&p.rub)o.rub=p.rub;if(k===0&&p.ann)o.ann=p.ann;fin.push(o)})}
  return fin}
function rotuloUnid(P){return P.art?P.art+(P.parte?" ("+P.parte+")":""):(P.h?"Título":"Trecho")}
'''
rep('function seccionar(pars,notas){\n  const S=[];', LEITOR + 'function seccionar(pars,notas){pars=estruturarLei(pars);\n  const S=[];')

# texto colado: cada linha é um bloco (o leitor junta as linhas quebradas)
rep(r'''function parsDeTexto(txt){const blocos=txt.replace(/\r/g,"").split(/\n\s*\n|\n(?=\s{2,}|\t)/)''',
    r'''function parsDeTexto(txt){const blocos=txt.replace(/\r/g,"").split(/\n/)''')
# a revisão do texto extraído não pode achatar as quebras de linha dos artigos
rep(r'''    const o={t:b.replace(/^‹p\.\d+›>?\s*/,"").replace(/\s+/g," "),pg};if(m&&m[2])o.q=true;if(o.t)out.push(o)}''',
    r'''    const o={t:b.replace(/^‹p\.\d+›>?\s*/,"").replace(/[ \t]+/g," ").replace(/ *\n */g,"\n").trim(),pg};if(m&&m[2])o.q=true;if(o.t)out.push(o)}''')

# ------------------------------------------------------------------ etapas
rep('''function passos(S){return [["mapa","Mapa"],["leitura","Leitura ativa"],["frases","Frases difíceis"],["vozes","Vozes"],["argumento","Argumento"],["crono","Cronologia"],["compreensao","Compreensão"],["fecho","Glossário e notas"]]}
const PRECISA_GEN={frases:g=>arr(g.lab).length>0,vozes:g=>!!g.vozes,argumento:g=>!!g.arg,crono:g=>arr(g.crono).length>=3};''',
'''function passos(S){return [["mapa","Mapa"],["leitura","Leitura do artigo"],["frases","Núcleo"],["vozes","Quem faz o quê"],["argumento","Regra e exceção"],["crono","Números e prazos"],["banca","Banca"],["compreensao","Compreensão"],["fecho","Glossário e notas"]]}
const PRECISA_GEN={frases:g=>arr(g.lab).length>0,vozes:g=>!!g.vozes,argumento:g=>!!g.arg,crono:g=>arr(g.num).length>0,banca:g=>arr(g.banca).length>0};''')
rep_region('const SEM_MATERIAL={', 'const corpo=', '''const SEM_MATERIAL={frases:"O Claude não encontrou nesta seção dispositivos longos que conferissem palavra por palavra com o texto.",
  vozes:"Esta seção não atribui competências ou deveres a sujeitos diferentes o bastante para o exercício.",
  argumento:"Esta seção não tem regra com condição ou exceção suficientes para o exercício.",
  crono:"Esta seção não tem prazos, números ou quóruns que conferissem com o texto.",
  banca:"O Claude não conseguiu montar itens de prova que conferissem com o texto desta seção."};
''')
rep('const ETAPAS={mapa:"Mapa",leitura:"Leitura ativa",frases:"Frases difíceis",vozes:"Vozes",argumento:"Argumento",crono:"Cronologia",compreensao:"Compreensão",fecho:"Glossário e notas",teste:"Teste"};',
    'const ETAPAS={mapa:"Mapa",leitura:"Leitura do artigo",frases:"Núcleo",vozes:"Quem faz o quê",argumento:"Regra e exceção",crono:"Números e prazos",banca:"Banca",compreensao:"Compreensão",fecho:"Glossário e notas",teste:"Teste"};')
rep('''  if(s==="frases"){est.fi=0;est.fr={c:0,t:0}}''', '''  if(s==="frases"){est.fi=0;est.fr={c:0,t:0}}
  if(s==="crono"){est.ni=0;est.nr={c:0,t:0,res:{}}}
  if(s==="banca"){est.bi=0;est.bst=null}''')
rep('''({mapa:pMapa,leitura:pLeitura,frases:pFrases,vozes:pVozes,argumento:pArg,crono:pCrono,compreensao:pComp,fecho:pFecho})[cur](S,$("#st"));''',
    '''({mapa:pMapa,leitura:pLeitura,frases:pFrases,vozes:pVozes,argumento:pArg,crono:pNumeros,banca:pBanca,compreensao:pComp,fecho:pFecho})[cur](S,$("#st"));''')
rep('''id==="crono"?!!R.crono:''', '''id==="crono"?!!R.crono:id==="banca"?!!(R.banca&&R.banca.fim):''')

# papéis: na LIO-L o exercício "Argumento" vira "Regra e exceção"; o treino continua com os papéis do texto acadêmico
rep('const PAPEIS={tese:"Tese",premissa:"Premissa",evidencia:"Evidência",conclusao:"Conclusão"};',
    'const PAPEIS_T={tese:"Tese",premissa:"Premissa",evidencia:"Evidência",conclusao:"Conclusão"};\nconst PAPEIS={tese:"Regra",premissa:"Condição",evidencia:"Exceção",conclusao:"Consequência"};')
i, j = region('function ex3Arg(){', '\nfunction ')
s = s[:i] + s[i:j].replace('PAPEIS', 'PAPEIS_T') + s[j:]
rep('''<div class="mrow">${g("tese").map(box).join("")}</div>${nivel("premissa","▲ sustentada por")}${nivel("evidencia","▲ apoiada em")}${nivel("conclusao","▼ leva a")}</figure>`}''',
    '''<div class="mrow">${g("tese").map(box).join("")}</div>${nivel("premissa","▲ aplica-se quando")}${nivel("evidencia","✕ salvo")}${nivel("conclusao","▼ resulta em")}</figure>`}''')
rep('''aria-label="Mapa do argumento"><figcaption>${titulo||"Mapa do argumento"}</figcaption>''',
    '''aria-label="Estrutura da norma"><figcaption>${titulo||"Estrutura da norma"}</figcaption>''')
# mapa das vozes vira mapa de competências
rep_region('function mapaVozes(V,titulo){', 'function mapaTempo(', '''function mapaVozes(V,titulo){const por=V.lista.map(v=>({v,af:V.af.filter(a=>a.v===v.id)})).filter(x=>x.af.length);if(!por.length)return "";
  return `<figure class="mapa" role="group" aria-label="Quem faz o quê"><figcaption>${titulo||"Quem faz o quê"}</figcaption><div class="comp-map">${por.map(x=>`<div class="cm"><b>${esc(x.v.nome)}</b>${x.af.map(a=>`<p>${esc(a.t)}</p>`).join("")}</div>`).join("")}</div></figure>`}
''')

# ------------------------------------------------------------------ geração e verificação
rep_region('function promptSecao(S){', 'function redesenharSecao(){', r'''function promptSecao(S){
  const ps=S.pars.map((p,i)=>p.h?`## ${p.t}`:`[P${i+1}] (p. ${p.pg})${p.rub?" ["+p.rub+"]":""} ${p.t}`).join("\n\n");
  return `Você é professor de cursinho para concursos públicos e conhece o estilo das bancas (Cebraspe, FGV, FCC, Vunesp). Prepare exercícios de leitura ativa de LEI SECA para um estudante, a partir do trecho de lei abaixo. Use SOMENTE o trecho: não traga jurisprudência, doutrina nem outras leis. Cada unidade [Pn] é um artigo (ou parte de um artigo) com caput, parágrafos, incisos e alíneas. Escreva em português do Brasil, com frases curtas e diretas.

Responda apenas com um objeto JSON neste formato:
{"ideias":[{"p":1,"certa":"...","erradas":["...","..."]}],
 "labirinto":[{"frase":"...","nucleo":"...","erradas":["...","..."]}],
 "competencias":{"sujeitos":[{"id":"s1","nome":"..."}],"atribuicoes":[{"texto":"...","sujeito":"s1","p":2}]},
 "estrutura":[{"texto":"...","papel":"regra","p":1}],
 "numeros":[{"campo":"...","certo":"...","erradas":["...","..."],"p":3}],
 "banca":[{"item":"...","gabarito":"E","tecnica":"troca_numero","troca":"...","correto":"...","base":"...","p":3}],
 "termos":[{"termo":"...","sentido":"...","p":2}]}

Regras:
- ideias: uma entrada para cada [Pn] que seja artigo. "certa" reproduz a regra do artigo em até 25 palavras, com sujeito, verbo (deve, pode, é vedado...), objeto e a exceção, se houver. As duas "erradas" têm tamanho e tom parecidos e são deturpações típicas de banca (troca de pode/deve, de prazo, de sujeito, supressão da exceção), falsas para quem leu com atenção.
- labirinto: até 3 dispositivos com 25 palavras ou mais, copiados EXATAMENTE (um caput, parágrafo ou inciso). "nucleo" é a norma reduzida a sujeito + verbo + complemento, com palavras do próprio dispositivo. As duas "erradas" são condições ou detalhes secundários do mesmo dispositivo.
- competencias: sujeitos (órgãos, autoridades, agentes, partes) que aparecem escritos no trecho, com o nome como está no texto; de 3 a 8 atribuições curtas parafraseadas (o que cada sujeito deve, pode ou não pode fazer). Se o trecho não distribui atribuições entre ao menos dois sujeitos, use listas vazias.
- estrutura: de 4 a 8 itens parafraseados que decompõem as normas do trecho. "papel" é "regra", "condicao" (quando ou desde que a regra se aplica), "excecao" (salvo, exceto, ressalvado) ou "consequencia" (sanção ou efeito). Ao menos uma regra. Se não houver condição nem exceção, use lista vazia.
- numeros: todo prazo, número, percentual, valor, quórum ou limite escrito no trecho (até 8). "campo" diz a que se refere, sem revelar o número; "certo" é a expressão exatamente como está no texto (ex.: "até dois anos", "dois terços"); as duas "erradas" são trocas plausíveis (outro número, "até" no lugar de "no mínimo", outra unidade).
- banca: de 8 a 12 itens Certo/Errado no estilo Cebraspe, cobrindo artigos diferentes. Cerca de 40% certos. Cada item errado usa UMA técnica de deturpação, indicada em "tecnica": "troca_verbo" (deve/pode/é vedado), "troca_sujeito" (outro órgão ou autoridade), "troca_numero" (prazo, número, quórum, "até"/"no mínimo"), "supressao_excecao" (regra apresentada como absoluta), "inversao" (regra vira exceção ou o contrário), "generalizacao" (sempre, em qualquer caso, exclusivamente), "rol" (exemplificativo como taxativo ou inciso que não existe no rol), "mistura" (requisito de um instituto atribuído a outro). Itens certos usam "tecnica":"parafrase_fiel" e dizem a regra com outras palavras, sem mudar o sentido. Em itens errados, "troca" é a palavra ou expressão EXATA do item que o torna errado e "correto" é o que o texto diz no lugar dela; em itens certos, "troca" e "correto" ficam vazios. "base" é o trecho do texto que decide o item, copiado EXATAMENTE, com 5 a 40 palavras.
- termos: de 3 a 6 termos técnicos do trecho; "sentido" explica, em até 25 palavras, como ESTA lei usa o termo (se a lei define o termo, use a definição dela).
- "p" é sempre o número do [Pn] de onde vem a informação.

TRECHO:
${ps}`}
const TECN={troca_verbo:"Troca do verbo",troca_sujeito:"Troca de sujeito",troca_numero:"Troca de número",supressao_excecao:"Supressão da exceção",inversao:"Inversão regra/exceção",generalizacao:"Generalização",rol:"Rol trocado",mistura:"Mistura de institutos",parafrase_fiel:"Paráfrase fiel"};
const PAPEL_L={regra:"tese",condicao:"premissa",excecao:"evidencia",consequencia:"conclusao"};
function validar(g,S){
  g=g&&typeof g==="object"?g:{};
  const full=norm(S.pars.map(p=>p.t).join(" ")+" "+S.notas.map(n=>n.t).join(" "));
  const nP=S.pars.length,okP=p=>Number.isInteger(+p)&&+p>=1&&+p<=nP&&!S.pars[+p-1].h;
  let desc=0;const conta=(a,b)=>{desc+=a.length-b.length;return b};
  const id0=arr(g.ideias);
  const ideias=conta(id0,id0.filter(x=>x&&okP(x.p)&&str(x.certa)&&arr(x.erradas).filter(str).length>=2)).map(x=>({i:+x.p-1,ok:x.certa.trim(),no:x.erradas.filter(str).slice(0,2).map(s=>s.trim())}));
  const lab0=arr(g.labirinto);
  const lab=conta(lab0,lab0.filter(x=>{if(!x||!str(x.frase)||!str(x.nucleo)||arr(x.erradas).filter(str).length<2)return false;
    if(!full.includes(norm(x.frase)))return false;
    const fw=new Set(x.frase.split(/\s+/).map(norm)),nw=x.nucleo.split(/\s+/).map(norm).filter(w=>w.length>=4);
    return nw.length>0&&nw.filter(w=>fw.has(w)).length/nw.length>=0.7})).slice(0,3).map(x=>({frase:x.frase.trim(),ok:x.nucleo.trim(),no:x.erradas.filter(str).slice(0,2)}));
  let vozes=null;const c=g.competencias||{};
  const vl=arr(c.sujeitos).filter(x=>x&&str(x.id)&&str(x.nome)&&(()=>{const ws=x.nome.split(/\s+/).map(norm).filter(w=>w.length>=3);return ws.length&&ws.some(w=>full.includes(w))})());
  desc+=arr(c.sujeitos).length-vl.length;
  const ids=new Set(vl.map(x=>x.id));
  const af=arr(c.atribuicoes).filter(x=>x&&str(x.texto)&&ids.has(x.sujeito));
  if(vl.length>=2&&af.length>=2&&new Set(af.map(x=>x.sujeito)).size>=2)vozes={lista:vl.map(x=>({id:x.id,nome:x.nome.trim()})).filter(v=>af.some(a=>a.sujeito===v.id)),af:af.map(x=>({t:x.texto.trim(),v:x.sujeito,p:okP(x.p)?+x.p-1:null})),rel:[]};
  const a0=arr(g.estrutura).filter(x=>x&&str(x.texto)&&PAPEL_L[x.papel]);
  const arg=a0.length>=3&&a0.some(x=>x.papel==="regra")&&a0.some(x=>x.papel!=="regra")?a0.map(x=>({t:x.texto.trim(),r:PAPEL_L[x.papel],p:okP(x.p)?+x.p-1:null})):null;
  const n0=arr(g.numeros);
  const num=conta(n0,n0.filter(x=>x&&str(x.campo)&&str(x.certo)&&arr(x.erradas).filter(str).length>=2&&full.includes(norm(x.certo))&&!x.erradas.some(e=>norm(e)===norm(x.certo)))).slice(0,8)
    .map(x=>({campo:x.campo.trim(),ok:x.certo.trim(),no:x.erradas.filter(str).slice(0,2).map(s=>s.trim()),p:okP(x.p)?+x.p-1:null}));
  const b0=arr(g.banca);
  const banca=conta(b0,b0.filter(x=>{if(!x||!str(x.item)||!/^[CE]$/.test(String(x.gabarito||"").trim().toUpperCase())||!TECN[x.tecnica]||!str(x.base))return false;
    if(!full.includes(norm(x.base)))return false;
    const gab=String(x.gabarito).trim().toUpperCase();
    if(gab==="E"){if(!str(x.troca)||!str(x.correto)||x.tecnica==="parafrase_fiel")return false;if(!norm(x.item).includes(norm(x.troca)))return false}
    return true})).slice(0,12).map(x=>{const gab=String(x.gabarito).trim().toUpperCase();
      return {item:x.item.trim(),gab,tec:gab==="C"?"parafrase_fiel":x.tecnica,troca:gab==="E"?x.troca.trim():"",certo:gab==="E"?x.correto.trim():"",base:x.base.trim(),p:okP(x.p)?+x.p-1:null}});
  const t0=arr(g.termos);
  const termos=conta(t0,t0.filter(x=>x&&str(x.termo)&&str(x.sentido)&&full.includes(norm(x.termo)))).map(x=>({termo:x.termo.trim(),sentido:x.sentido.trim(),p:okP(x.p)?+x.p-1:null}));
  return {ideias,lab,vozes,arg,crono:[],num,banca,termos,desc,quando:agora()};
}
''')
# a geração da LIO-L devolve um JSON maior
rep_all('CAP.sample.json(promptSecao(S),{signal:ctl.signal,cache:false})', 'CAP.sample.json(promptSecao(S),{signal:ctl.signal,cache:false,maxTokens:12000})')
rep('CAP.sample.json(promptSecao(S),{cache:false})', 'CAP.sample.json(promptSecao(S),{cache:false,maxTokens:12000})')

# ------------------------------------------------------------------ Mapa topográfico
rep_region('function pMapa(S,el){', '\n/* Etiqueta com IA', r'''function pMapa(S,el){const b=corpo(S),w=b.reduce((s,i)=>s+S.pars[i].t.split(/\s+/).length,0),na=b.filter(i=>S.pars[i].art).length;
  const cap=p=>{const l=p.t.split("\n")[0];return l.length>260?l.slice(0,260)+"…":l};
  const resto=p=>{const L=p.t.split("\n").slice(1),n=k=>L.filter(l=>k.test(l)).length,inc=n(/^[IVXLCDM]+(\s*-\s*[A-Z])?\s*[-–—]/),par=n(/^(§|Par[áa]grafo)/),ali=n(/^[a-z]\)/);
    const x=[par?par+(par>1?" parágrafos":" parágrafo"):"",inc?inc+(inc>1?" incisos":" inciso"):"",ali?ali+(ali>1?" alíneas":" alínea"):""].filter(Boolean);return x.length?`<span class="note"> + ${x.join(", ")}</span>`:""};
  el.innerHTML=`<p class="lead">Antes de ler, veja a topografia da seção: onde cada coisa está. Leia só os caputs e tente prever o que vem nos parágrafos e incisos de cada artigo.</p>
  <p class="note">${na} ${na===1?"artigo":"artigos"} · ${S.notas.length} notas · cerca de ${Math.max(1,Math.round(w/110))} min de leitura atenta</p>
  <ul class="skel">${S.pars.map(p=>p.h?`<li class="sk-h">${esc(p.t)}</li>`:`<li><span class="pgref">p. ${p.pg}</span>${p.rub?`<b>${esc(p.rub)}.</b> `:""}${esc(p.art&&p.parte&&!/^caput/.test(p.parte)?rotuloUnid(p)+" (continuação)":cap(p))}${resto(p)}</li>`).join("")}</ul>
  <p class="note">Confira se o texto é o compilado e atualizado (no site do Planalto, a versão compilada). Trechos tachados no site, que são revogados, perdem o tachado quando o texto é copiado ou extraído.</p>
  <div class="row"><button class="btn primary" id="nx">Começar a leitura</button></div>`;
  $("#nx").onclick=()=>abrirPasso("leitura");
}
''')

# ------------------------------------------------------------------ Etiqueta (regra) e gatilhos com IA
rep_region('function promptEtq(S,i){', 'function lerEtqIA(t){', '''function promptEtq(S,i){return `Você é professor de cursinho para concursos. Leia o dispositivo de lei abaixo e responda em duas linhas, em português do Brasil:
ETIQUETA: a regra em uma frase de até 20 palavras, com as próprias palavras: quem, deve/pode/é vedado o quê, em que condição e com que exceção, se houver; sem ponto final
GATILHOS: de 3 a 8 palavras ou expressões curtas que uma banca trocaria para tornar uma afirmação errada (verbos como deve, pode, é vedado; prazos; números; quóruns; sujeitos; condições; exceções; palavras como exclusivamente, salvo, no mínimo), copiadas EXATAMENTE como estão no texto e separadas por " | "

Responda somente com essas duas linhas, sem aspas e sem explicação.

DISPOSITIVO:
${S.pars[i].t}`}
''')
rep_region('function lerEtqIA(t){', '/* Marcador:', r'''function lerEtqIA(t){const L=String(t||"").split(/\n/).map(l=>l.trim()).filter(Boolean);
  const e=L.find(l=>/^\**\s*etiqueta\s*\**\s*:/i.test(l))||L.find(l=>!/^\**\s*(trecho|gatilhos)\s*\**\s*:/i.test(l))||"";
  const r=L.find(l=>/^\**\s*gatilhos\s*\**\s*:/i.test(l))||"";
  const gat=r.replace(/^\**\s*gatilhos\s*\**\s*:\s*/i,"").split("|").map(x=>x.trim().replace(/^["“'«]+|["”'»]+$/g,"")).filter(Boolean).slice(0,10);
  return {tag:limparEtq(e.replace(/^\**\s*etiqueta\s*\**\s*:\s*/i,"")),trecho:"",gat}}
/* Gatilhos: cada expressão é procurada no dispositivo, palavra por palavra; todas as ocorrências são marcadas */
function gatIdx(par,lista){const C=compactPar(par),out=new Set();
  for(const g of arr(lista)){const T=String(g||"").split(/\s+/).map(norm).filter(Boolean);if(!T.length||T.length>8)continue;
    for(let s0=0;s0+T.length<=C.length;s0++){let ok=true;for(let j=0;j<T.length;j++)if(C[s0+j].w!==T[j]){ok=false;break}if(ok)for(let j=0;j<T.length;j++)out.add(C[s0+j].k)}}
  return [...out].sort((a,b)=>a-b)}
''')
rep('''const w=x.split(/\\s+/);return w.length>10?w.slice(0,10).join(" "):x}''', '''const w=x.split(/\\s+/);return w.length>25?w.slice(0,25).join(" "):x}''')
rep('''const ia=trechoIdx(S.pars[i].t,lr.trecho);''', '''const ia=gatIdx(S.pars[i].t,lr.gat);''')
rep('''function locTexto(L){return `<b>Detecção de gatilhos: ${L.pct}%</b> · você marcou ${L.u} ${L.u===1?"palavra":"palavras"}, a IA ${L.a}, coincidiram ${L.c}.`}''',
    '''function locTexto(L){return `<b>Detecção de gatilhos: ${L.pct}%</b> · você marcou ${L.u} ${L.u===1?"palavra":"palavras"}, a IA ${L.a}, coincidiram ${L.c}.`}''')
sub_in_region('function ligarEtqIA(S,i,mk){', '/* 2 · Leitura ativa */', [
    ('Este parágrafo começou com uma sugestão da IA: não há Detecção de gatilhos aqui.', 'Este artigo começou com uma sugestão da IA: não há Detecção de gatilhos aqui.'),
    ('A IA não indicou um trecho reconhecível no parágrafo; sem Detecção de gatilhos desta vez.', 'A IA não indicou gatilhos reconhecíveis no texto; sem Detecção de gatilhos desta vez.'),
    ('Para ver a Detecção de gatilhos, marque no parágrafo, antes de comparar, as palavras de onde tirou a sua etiqueta.', 'Para ver a Detecção de gatilhos, marque no artigo, antes de comparar, as palavras que a banca trocaria.'),
    ('Em verde, o trecho que a IA usou; em azul, onde vocês coincidiram. A marcação da IA é uma referência, não um gabarito.', 'Em verde, os gatilhos que a IA apontou; em azul, onde vocês coincidiram. A marcação da IA é uma referência, não um gabarito.'),
    ('A ideia é a mesma? Se a sua deixou algo importante de fora, ajuste. Se as duas dizem o mesmo, fique com a sua.', 'A regra é a mesma? Confira se a sua manteve quem faz, o verbo (deve, pode, é vedado), o prazo e a exceção. Se as duas dizem o mesmo, fique com a sua.'),
    ('Lendo o parágrafo…', 'Lendo o artigo…'),
])

# ------------------------------------------------------------------ Leitura do artigo
rep('aria-label="Ir para um parágrafo"', 'aria-label="Ir para um artigo"')
sub_in_region('/* 2 · Leitura ativa */', '/* 3 · Frases difíceis */', [
    ('k=>`Parágrafo ${k+1} · p. ${S.pars[b[k]].pg}', 'k=>`${rotuloUnid(S.pars[b[k]])} · p. ${S.pars[b[k]].pg}'),
    ('<span class="pn">${k+1}</span>${esc(p.t)}', '<span class="pn">${esc(p.art||k+1)}</span>${p.rub?`<span class="rubrica">${esc(p.rub)}</span>`:""}${esc(p.art?p.t.replace(/^Art\\.\\s*\\S+\\s*/,""):p.t)}'),
    ('<span class="label">Parágrafo ${est.li+1} de ${b.length} · p. ${P.pg}${P.q?" · citação":""}</span>', '<span class="label">${esc(rotuloUnid(P))} · ${est.li+1} de ${b.length} · p. ${P.pg}</span>${P.rub?`<p class="rubrica">${esc(P.rub)}</p>`:""}'),
    ('<p id="parTx">${parMarcavel(P.t,new Set(MK.u||[]),new Set(MK.a||[]))}</p></div>', '<p id="parTx">${parMarcavel(P.t,new Set(MK.u||[]),new Set(MK.a||[]))}</p>${arr(P.ann).length?`<details class="ann"><summary>Anotações do texto compilado (${P.ann.length})</summary>${P.ann.map(a=>`<p>${esc(a)}</p>`).join("")}</details>`:""}</div>'),
    ('Marcador: toque nas palavras de onde você tirou a sua etiqueta, ou selecione um trecho. É opcional, e é o que permite medir a Detecção de gatilhos.',
     'Marca-gatilhos: toque nas palavras que a banca trocaria para fazer um item errado (pode/deve, prazos, números, quem faz, condições, exceções) ou selecione um trecho. É opcional, e é o que permite medir a Detecção de gatilhos.'),
    ('Etiqueta: a ideia deste parágrafo em 3 a 8 palavras suas', 'A regra em uma frase, com as suas palavras: quem, deve/pode o quê, quando, salvo o quê'),
    ('Não consigo resumir: pedir uma sugestão', 'Não consigo resumir a regra: pedir uma sugestão'),
    ('placeholder="Termo difícil neste parágrafo" aria-label="Termo difícil"', 'placeholder="Termo técnico neste artigo" aria-label="Termo técnico"'),
    ('title="Escreva a etiqueta para continuar"', 'title="Escreva a regra para continuar"'),
    ('Resumo da seção nas suas palavras', 'As regras da seção nas suas palavras'),
    ('Nenhuma etiqueta escrita.', 'Nenhuma regra escrita.'),
    (' <span class="pill loc">localização ${R.marc[i].loc.pct}%</span>', ' <span class="pill loc">gatilhos ${R.marc[i].loc.pct}%</span>'),
    ('<span class="note">Média de ${LV.length} ${LV.length===1?"parágrafo":"parágrafos"} em que você marcou o texto e comparou a sua etiqueta com a da IA. Mede o quanto a região que você marcou coincide com a da IA (coincidências ÷ palavras marcadas por um ou pelos dois). Parágrafos que começaram com uma sugestão da IA não entram.</span>',
     '<span class="note">Média de ${LV.length} ${LV.length===1?"artigo":"artigos"} em que você marcou os gatilhos e comparou a sua regra com a da IA. Mede o quanto as palavras que você marcou coincidem com os gatilhos da IA (coincidências ÷ palavras marcadas por um ou pelos dois). Artigos que começaram com uma sugestão da IA não entram.</span>'),
    ('Estas etiquetas entram no fichamento. Dá para reescrever qualquer uma voltando à leitura.', 'Estas regras entram no fichamento e viram cartões de revisão. Dá para reescrever qualquer uma voltando à leitura.'),
    ('O parágrafo está escondido.</div><p class="q">Qual é a ideia central do parágrafo que você acabou de ler?</p>', 'O artigo está escondido.</div><p class="q">Qual alternativa reproduz fielmente a regra do artigo que você acabou de ler?</p>'),
    ('<b class="${right?"ok":"bad"}">${right?"Isso.":"Não era essa."}</b> Sua etiqueta: <i>${esc(R.etq[i])}</i>. Se ela ficou longe da ideia central, ajuste ao rever.',
     '<b class="${right?"ok":"bad"}">${right?"Isso.":"Essa foi deturpada."}</b> Sua regra: <i>${esc(R.etq[i])}</i>. Se ela perdeu o prazo, quem faz ou a exceção, ajuste ao rever.'),
    ('O parágrafo está escondido. Sem olhar, diga para você mesmo a ideia central e compare com a sua etiqueta: <i>${esc(R.etq[i])}</i>.',
     'O artigo está escondido. Sem olhar, reconstrua a regra para você mesmo: quem, deve ou pode o quê, quando, salvo o quê. Depois compare com a sua: <i>${esc(R.etq[i])}</i>.'),
    ('Rever e ajustar a etiqueta', 'Rever e ajustar a regra'),
])
sub_in_region('/* 2 · Leitura ativa */', '/* 3 · Frases difíceis */', [
    ('Parágrafo anterior', 'Artigo anterior'), ('Pular este parágrafo', 'Pular este artigo'),
    ('"ao parágrafo "+(est.li+1)', '"ao "+rotuloUnid(S.pars[b[est.li]])'), ('Seção inteira · ${b.length} parágrafos', 'Seção inteira · ${b.length} ${b.length===1?"unidade":"unidades"}'),
    ('Toque num parágrafo para estudá-lo.', 'Toque num artigo para estudá-lo.'), ('title="Estudar este parágrafo"', 'title="Estudar este artigo"'),
    ('>Próximo parágrafo<', '>Próximo artigo<'),
])

# ------------------------------------------------------------------ Núcleo, quem faz o quê, regra e exceção
sub_in_region('/* 3 · Frases difíceis */', '/* 4 · Vozes */', [
    ('Ao ler, procure primeiro o verbo principal e trate o que está entre vírgulas como desvio.', 'Na lei, ache primeiro quem e o verbo (deve, pode, é vedado, compete); o que vem entre vírgulas são condições e detalhes, que a banca também cobra.'),
    ('Frases longas tiradas desta seção. Encontre o núcleo: quem faz o quê.', 'Dispositivos longos desta seção. Encontre o núcleo da norma: quem, deve ou pode, o quê.'),
    ('Qual é o núcleo desta frase?', 'Qual é o núcleo deste dispositivo?'),
    ('As palavras do núcleo estão marcadas na frase.', 'As palavras do núcleo estão marcadas no dispositivo.'),
    ('`Você achou o núcleo de ${est.fr.c} de ${est.fr.t} frases.`:"Nenhuma frase restante."', '`Você achou o núcleo de ${est.fr.c} de ${est.fr.t} dispositivos.`:"Nenhum dispositivo restante."'),
])
sub_in_region('/* 4 · Vozes */', '/* 5 · Argumento */', [
    ('De memória: de quem é cada ideia? Se precisar, abra o trecho, mas tente antes sem ele.', 'De memória: quem faz o quê? Ligue cada atribuição ao sujeito certo. A troca de sujeito é uma das pegadinhas mais comuns. Se precisar, abra o texto, mas tente antes sem ele.'),
    ('`<b style="color:var(--bad)">É de ${esc(nome[x.v])}.</b>`', '`<b style="color:var(--bad)">Cabe a ${esc(nome[x.v])}.</b>`'),
    ('<summary>Mostrar o trecho</summary>', '<summary>Mostrar o texto da seção</summary>'),
])
sub_in_region('/* 5 · Argumento */', '/* 6 · Cronologia */', [
    ('As frases que reconstroem o raciocínio desta seção estão embaralhadas. Diga o papel de cada uma.', 'As partes das normas desta seção estão embaralhadas. Diga o papel de cada uma: regra, condição (quando se aplica), exceção (salvo, exceto, ressalvado) ou consequência.'),
])

# ------------------------------------------------------------------ Números e prazos, Banca
NOVAS = r'''
/* 6 · Números e prazos (LIO-L) */
function pNumeros(S,el){const N=S.gen.num.map((x,k)=>({...x,k})).filter(x=>!sinal(S,"n"+x.k));est.nr=est.nr||{c:0,t:0,res:{}};
  if(est.ni>=N.length){S.resp.crono={c:est.nr.c,t:est.nr.t};salvarResp(S);
    el.innerHTML=`<div class="fb">${est.nr.t?`Você acertou ${est.nr.c} de ${est.nr.t} números.`:"Nenhum número restante."} Números são o alvo mais fácil da banca: um "até" vira "no mínimo", dois anos viram quatro.</div>
    ${tabelaNumeros(S,N)}<div class="row"><button class="btn primary" id="nx">Próxima etapa</button></div>`;
    $("#nx").onclick=()=>proximoPasso(S);return}
  const X=N[est.ni],opts=shuffle([X.ok,...X.no]).map(esc);
  el.innerHTML=`<p class="lead">De memória: qual é o número exato? Prazos, quóruns, percentuais e limites desta seção.</p>${stepsBar(N.length,est.ni)}
  <p class="q">${esc(X.campo)}${X.p!=null&&S.pars[X.p]&&S.pars[X.p].art?` <span class="pgref">${esc(S.pars[X.p].art)}</span>`:""}</p>${optsHTML(opts)}<div id="fb" aria-live="polite"></div>`;
  bindOpts(opts,esc(X.ok),right=>{est.nr.t++;if(right)est.nr.c++;est.nr.res[X.k]=right;logEv("numero",{est:est.id,sec:S.n,certo:right});
    $("#fb").innerHTML=`<div class="stack"><div class="fb"><b class="${right?"ok":"bad"}">${right?"Isso.":"Não."}</b> O texto diz: <b>${esc(X.ok)}</b>${X.p!=null?pg(S,X.p):""}.</div><div class="row"><button class="btn primary" id="nx">Continuar</button></div>${botaoSinal("n"+X.k)}</div>`;
    const nx=()=>{est.ni++;pNumeros(S,el)};$("#nx").onclick=nx;ligarSinal(S,el,nx)});
}
function tabelaNumeros(S,N){N=N||arr(S.gen&&S.gen.num);if(!N.length)return "";
  return `<figure class="mapa" role="group" aria-label="Números desta seção"><figcaption>Números e prazos desta seção</figcaption><table class="tabnum"><tbody>${N.map(x=>`<tr><td>${esc(x.campo)}</td><td class="v">${esc(x.ok)}</td><td>${x.p!=null&&S.pars[x.p]?esc(S.pars[x.p].art||"")+pg(S,x.p):""}</td></tr>`).join("")}</tbody></table></figure>`}

/* 7 · Banca (LIO-L): itens Certo/Errado, com confiança e a palavra da troca */
const CONF_B=[[3,"Certeza"],[2,"Dúvida"],[1,"Chute"]];
function tokensItem(t){return String(t).split(/(\s+)/)}
function trocaIdx(item,troca){const C=[];let k=0;tokensItem(item).forEach(x=>{if(!x||/^\s+$/.test(x))return;C.push({k,w:norm(x)});k++});
  const T=String(troca||"").split(/\s+/).map(norm).filter(Boolean),out=new Set();if(!T.length)return out;
  for(let s0=0;s0+T.length<=C.length;s0++){let ok=true;for(let j=0;j<T.length;j++)if(C[s0+j].w!==T[j]){ok=false;break}if(ok){for(let j=0;j<T.length;j++)out.add(C[s0+j].k);break}}
  return out}
function itemHTML(item,sel,troca,apontar){let k=0;return `<p class="item-ce${apontar?" apontar":""}" id="itx">${tokensItem(item).map(x=>{if(!x||/^\s+$/.test(x))return esc(x);const c=troca&&troca.has(k)?" troca":sel&&sel.has(k)?" sel":"";return `<span class="tk${c}" data-t="${k++}">${esc(x)}</span>`}).join("")}</p>`}
function pBanca(S,el){const R=S.resp,B=S.gen.banca.map((x,k)=>({...x,k})).filter(x=>!sinal(S,"b"+x.k));
  R.banca=R.banca&&R.banca.it?R.banca:{it:{}};const it=R.banca.it;
  if(est.bi>=B.length)return bancaFim(S,el,B);
  const X=B[est.bi],a=it[X.k]||{},st=est.bst=est.bst&&est.bst.k===X.k?est.bst:{k:X.k,conf:a.conf||null,resp:a.r||null,fase:a.r?"fim":"responder",sel:new Set(a.pal||[])};
  const tr=trocaIdx(X.item,X.troca);
  const cab=`<p class="lead">Itens no estilo Cebraspe. Marque a confiança, responda Certo ou Errado, ou deixe em branco. Na prova, cada erro anula um acerto.</p>${stepsBar(B.length,est.bi)}`;
  if(st.fase==="responder"){
    el.innerHTML=`${cab}<div class="passage">${itemHTML(X.item)}</div>
    <div class="confs" role="group" aria-label="Confiança"><span class="note">Sua confiança:</span>${CONF_B.map(([v,l])=>`<button class="chip" data-cf="${v}" aria-pressed="${st.conf===v}">${l}</button>`).join("")}</div>
    <div class="ce"><button class="btn primary" data-ce="C" ${st.conf?"":"disabled"}>Certo</button><button class="btn primary" data-ce="E" ${st.conf?"":"disabled"}>Errado</button><button class="btn" data-ce="B">Deixar em branco</button></div>
    ${st.conf?"":'<p class="note">Escolha a confiança antes de responder: é ela que mostra quando vale a pena chutar.</p>'}`;
    el.querySelectorAll("[data-cf]").forEach(b=>b.onclick=()=>{st.conf=+b.dataset.cf;pBanca(S,el)});
    el.querySelectorAll("[data-ce]").forEach(b=>b.onclick=()=>{st.resp=b.dataset.ce;st.t0=st.t0||Date.now();
      if(st.resp==="E"){st.fase="apontar";pBanca(S,el)}else fecharItem(S,el,X,st)});
    return}
  if(st.fase==="apontar"){
    el.innerHTML=`${cab}<div class="passage">${itemHTML(X.item,st.sel,null,true)}</div>
    <p class="q">Toque a palavra ou expressão que torna o item errado.</p>
    <div class="row"><button class="btn primary" id="bok" ${st.sel.size?"":"disabled"}>Conferir</button><button class="btn small" id="bsem">Não sei apontar</button><button class="linkbtn" id="bvolta">Mudar a resposta</button></div>`;
    el.querySelectorAll("[data-t]").forEach(x=>x.onclick=()=>{const k=+x.dataset.t;st.sel.has(k)?st.sel.delete(k):st.sel.add(k);pBanca(S,el)});
    $("#bok").onclick=()=>fecharItem(S,el,X,st);$("#bsem").onclick=()=>{st.sel.clear();fecharItem(S,el,X,st)};$("#bvolta").onclick=()=>{st.fase="responder";st.resp=null;st.sel.clear();pBanca(S,el)};
    return}
  // resultado
  const ok=a.r===X.gab,branco=a.r==="B",palOk=a.pal&&a.pal.length&&tr.size?a.pal.some(k=>tr.has(k)):null;
  el.innerHTML=`${cab}<div class="passage">${itemHTML(X.item,new Set(a.pal||[]),X.gab==="E"?tr:null)}</div>
  <div class="fb stack" style="gap:6px"><span><b class="${branco?"":ok?"ok":"bad"}">${branco?"Em branco.":ok?"Acertou.":"Errou."}</b> Gabarito: <b>${X.gab==="C"?"Certo":"Errado"}</b> · <span class="tecn">${esc(TECN[X.tec]||"")}</span>${a.conf?` · você marcou <i>${esc((CONF_B.find(c=>c[0]===a.conf)||[,""])[1].toLowerCase())}</i>`:""}</span>
   ${X.gab==="E"?`<span>A troca: <b>${esc(X.troca)}</b> no lugar de <b>${esc(X.certo)}</b>.${a.r==="E"&&palOk!==null?(palOk?' <span class="ok">Você apontou a troca.</span>':' <span class="bad">A palavra que você apontou não é a da troca.</span>'):""}</span>`:'<span>O item diz a regra com outras palavras, sem mudar o sentido. Paráfrase fiel também cai em prova.</span>'}
   <span class="note">O texto: «${esc(X.base)}»${X.p!=null&&S.pars[X.p]?" · "+esc(S.pars[X.p].art||"")+pg(S,X.p):""}</span></div>
  <div class="row"><button class="btn primary" id="nx">${est.bi+1<B.length?"Próximo item":"Ver o resultado"}</button>${est.bi>0?'<button class="btn small" id="ant">◀ Item anterior</button>':""}</div>${botaoSinal("b"+X.k)}`;
  const nx=()=>{est.bi++;est.bst=null;pBanca(S,el);window.scrollTo(0,0)};$("#nx").onclick=nx;
  if($("#ant"))$("#ant").onclick=()=>{est.bi--;est.bst=null;pBanca(S,el)};ligarSinal(S,el,nx);
}
function fecharItem(S,el,X,st){const R=S.resp,tr=trocaIdx(X.item,X.troca);
  const pal=st.resp==="E"?[...st.sel]:[];R.banca.it[X.k]={r:st.resp,conf:st.resp==="B"?null:st.conf,pal,ok:st.resp===X.gab,palOk:st.resp==="E"&&X.gab==="E"&&pal.length?pal.some(k=>tr.has(k)):null,tec:X.tec};
  logEv("banca",{est:est.id,sec:S.n,k:X.k,r:st.resp,gab:X.gab,conf:st.conf,tec:X.tec,ms:Date.now()-(st.t0||Date.now())});
  resumoBanca(S);salvarResp(S);st.fase="fim";pBanca(S,el)}
function resumoBanca(S){const R=S.resp,B=arr(S.gen&&S.gen.banca),it=R.banca.it,ks=Object.keys(it).filter(k=>B[k]&&!sinal(S,"b"+k));
  let c=0,e=0,b=0;ks.forEach(k=>{const x=it[k];if(x.r==="B")b++;else if(x.ok)c++;else e++});
  R.banca.c=c;R.banca.t=ks.length;R.banca.e=e;R.banca.b=b;R.banca.liq=c-e}
function bancaFim(S,el,B){const R=S.resp;resumoBanca(S);R.banca.fim=true;salvarResp(S);const it=R.banca.it,x=R.banca;
  const porConf=CONF_B.map(([v,l])=>{const xs=Object.values(it).filter(a=>a.conf===v&&a.r!=="B");return {l,n:xs.length,ok:xs.filter(a=>a.ok).length}}).filter(z=>z.n);
  const erros={};Object.entries(it).forEach(([k,a])=>{if(a.r!=="B"&&!a.ok&&B.find(y=>y.k===+k)){const t=TECN[B.find(y=>y.k===+k).tec];erros[t]=(erros[t]||0)+1}});
  const ap=Object.values(it).filter(a=>a.palOk!==null&&a.palOk!==undefined),apOk=ap.filter(a=>a.palOk).length;
  const chute=porConf.find(z=>z.l==="Chute");
  el.innerHTML=`<h2>Resultado da banca</h2>
  <div class="placar"><div class="stat"><b>${x.c}</b><span class="note">certos</span></div><div class="stat"><b>${x.e}</b><span class="note">errados</span></div><div class="stat"><b>${x.b}</b><span class="note">em branco</span></div><div class="stat"><b>${x.liq}</b><span class="note">nota líquida (certos − errados)</span></div></div>
  ${porConf.length?`<div class="fb"><b>Confiança × acerto.</b> ${porConf.map(z=>`${z.l}: ${z.ok} de ${z.n} (${Math.round(100*z.ok/z.n)}%)`).join(" · ")}.${chute&&chute.n>=2?(chute.ok/chute.n<.5?" Seus chutes erram mais do que acertam: em prova que desconta, deixe em branco.":" Seus chutes estão acertando mais da metade, mas confira com mais itens antes de confiar neles."):""}</div>`:""}
  ${Object.keys(erros).length?`<div class="fb"><b>Onde você caiu:</b> ${Object.entries(erros).sort((a,b)=>b[1]-a[1]).map(([t,n])=>`${esc(t)} (${n})`).join(" · ")}.</div>`:""}
  ${ap.length?`<p class="note">Você apontou a palavra da troca em ${apOk} de ${ap.length} ${ap.length===1?"item errado que marcou como errado":"itens errados que marcou como errados"}.</p>`:""}
  <div class="row"><button class="btn primary" id="nx">Próxima etapa</button><button class="btn" id="re">Refazer os itens</button></div>`;
  $("#nx").onclick=()=>proximoPasso(S);$("#re").onclick=()=>{R.banca={it:{}};est.bi=0;est.bst=null;salvarResp(S);pBanca(S,el)};
}

/* 7 · Glossário e notas */'''
rep('\n/* 7 · Glossário e notas */', NOVAS)
# fechamento: tabela de números
rep('''  el.innerHTML=`<h2>Glossário desta seção</h2>''', '''  el.innerHTML=`${tabelaNumeros(S)}<h2>Glossário desta seção</h2>''')
rep('''<label for="obs">Minhas observações sobre esta seção (dúvidas, conexões com a pesquisa, o que discordo)</label>''',
    '''<label for="obs">Minhas observações sobre esta seção (dúvidas, pegadinhas em que caí, ligações com outros artigos)</label>''')
rep('''Explique, em até 25 palavras cada, como o TRECHO abaixo usa cada termo da lista.''', '''Explique, em até 25 palavras cada, como o TRECHO de lei abaixo usa cada termo da lista; se a lei define o termo, use a definição dela.''')

# ------------------------------------------------------------------ Compreensão: literal, aplicação, sistemática
rep('const NIVEL={literal:"Literal",inferencial:"Inferencial",critica:"Crítica"};', 'const NIVEL={literal:"Literal",inferencial:"Aplicação",critica:"Sistemática"};')
rep('const NIVEL_DESC={literal:"A resposta está escrita no texto.",inferencial:"Exige ligar informações ou deduzir o que o texto dá a entender.",critica:"Pede que você avalie o argumento e se posicione, com base no texto."};',
    'const NIVEL_DESC={literal:"A resposta está escrita na lei, palavra por palavra.",inferencial:"Um caso concreto: você aplica a regra e diz o que acontece.",critica:"Liga dispositivos diferentes da seção: regra e exceção, competência e prazo."};')
rep_region('function promptPerg(S){', 'function validarPerg(g,S){', r'''function promptPerg(S){return `Você é professor de cursinho para concursos e prepara perguntas sobre LEI SECA. Use SOMENTE o trecho de lei abaixo: não traga jurisprudência, doutrina nem outras leis. Escreva em português do Brasil, com frases curtas e claras.

Crie 6 perguntas abertas: 2 literais (a resposta está escrita no texto: prazo, quem faz, requisito), 2 de aplicação (um caso concreto curto, com nomes fictícios, em que o estudante aplica a regra e diz o que acontece) e 2 sistemáticas (ligam dois ou mais artigos ou dispositivos do trecho: a regra de um com a exceção de outro, a competência com o prazo).

Responda apenas com JSON neste formato:
{"perguntas":[{"nivel":"literal","pergunta":"...","p":2,"resposta":"..."}]}

- "nivel" é "literal", "inferencial" (para as de aplicação) ou "critica" (para as sistemáticas).
- "p" é o número do [Pn] que mais ajuda a responder.
- "resposta": a resposta esperada em até 40 palavras, citando o artigo.

TRECHO:
${trechoNum(S)}`}
''')
rep('''- "avaliacao": "completa", "parcial" ou "incompleta". Numa pergunta crítica, é "completa" quando a posição do estudante está fundamentada em elementos do texto, concorde ele ou não com o autor.''',
    '''- "avaliacao": "completa", "parcial" ou "incompleta". Em lei, precisão conta: troca de prazo, de sujeito, de pode por deve ou esquecimento da exceção tornam a resposta "parcial" ou "incompleta". Numa pergunta de aplicação, a conclusão precisa estar certa e apoiada no artigo.''')
rep('''Você é um tutor paciente que ajuda um estudante com dificuldade de compreensão de leitura. Avalie a resposta do estudante com base SOMENTE no trecho.''',
    '''Você é um professor de cursinho paciente que ajuda um estudante a ler lei seca. Avalie a resposta do estudante com base SOMENTE no trecho de lei.''')
rep('''PERGUNTA (${NIVEL[Q.n].toLowerCase()}): ${Q.q}''', '''PERGUNTA (${NIVEL[Q.n].toLowerCase()}): ${Q.q}''')

# teste antes e depois no formato de prova
rep('''Crie um teste de compreensão de leitura sobre o texto abaixo, dividido em seções [Sn]. Use SOMENTE o texto. Faça ${n} questões de múltipla escolha, cerca de metade literais (resposta escrita no texto) e metade inferenciais (exigem ligar informações ou deduzir), distribuídas entre as seções.''',
    '''Crie um teste sobre o texto de lei abaixo, dividido em seções [Sn], no estilo das questões de múltipla escolha de concurso. Use SOMENTE o texto, sem jurisprudência nem doutrina. Faça ${n} questões, cerca de metade de literalidade (a resposta é a letra da lei) e metade de aplicação (um caso curto em que se aplica a regra), distribuídas entre as seções. As alternativas erradas usam as deturpações típicas de banca: troca de prazo ou número, de sujeito, de pode por deve, supressão de exceção.''')

# ------------------------------------------------------------------ índices da rodada
rep('''const COMP_ROT={ide:"Ideia central",frases:"Frases difíceis",vozes:"Vozes",arg:"Argumento",crono:"Cronologia",perg:"Compreensão",teste:"Teste"};''',
    '''const COMP_ROT={ide:"Regra do artigo",frases:"Núcleo",vozes:"Quem faz o quê",arg:"Regra e exceção",crono:"Números e prazos",banca:"Banca",perg:"Compreensão",teste:"Teste"};''')
rep('''const soma={ide:[0,0],frases:[0,0],vozes:[0,0],arg:[0,0],crono:[0,0],perg:[0,0]};''', '''const soma={ide:[0,0],frases:[0,0],vozes:[0,0],arg:[0,0],crono:[0,0],banca:[0,0],perg:[0,0]};''')
rep('''    ["frases","vozes","arg","crono"].forEach(k=>{const x=R[k];if(x&&x.t){soma[k][0]+=x.c||0;soma[k][1]+=x.t}});''',
    '''    ["frases","vozes","arg","crono","banca"].forEach(k=>{const x=R[k];if(x&&x.t){soma[k][0]+=x.c||0;soma[k][1]+=x.t}});''')


# ------------------------------------------------------------------ ajustes de texto
rep("${nP} parágrafos, ${nv.notas.length} notas de rodapé, ${nv.secs.length}", "${nv.secs.reduce((n,x)=>n+x.pars.filter(p=>p.art).length,0)} unidades de leitura (artigos), ${nv.notas.length} notas de rodapé, ${nv.secs.length}")
rep("p. ${s.pgIni}–${s.pgFim} · ${ps.length} parágrafos · cerca de", 'p. ${s.pgIni}–${s.pgFim} · ${ps.length} ${ps.length===1?"unidade":"unidades"} · cerca de')
rep('p. ${S.pgIni}–${S.pgFim} · ${nP} parágrafos${S.gen?" · exercícios prontos":""}', 'p. ${S.pgIni}–${S.pgFim} · ${nP} ${nP===1?"unidade":"unidades"}${S.gen?" · exercícios prontos":""}')
rep('<label for="clx">Texto (separe os parágrafos com uma linha em branco)</label>', '<label for="clx">Texto da lei (cole do site do Planalto, versão compilada: a LIO-L separa os artigos sozinha)</label>')

# ------------------------------------------------------------------ Início
rep('"Bem-vindo(a) à LIO"', '"Bem-vindo(a) à LIO-L"')
rep('Escolha um texto do seu curso. A LIO divide em seções e guia a leitura.', 'Cole ou anexe a lei do seu edital. A LIO-L separa os artigos, divide em seções e guia a leitura.')
rep('<summary>Como a LIO funciona</summary>', '<summary>Como a LIO-L funciona</summary>')
rep('<p><b>Estudar</b> usa o seu material: o texto é dividido em seções de 15 a 20 minutos, e cada seção passa por mapa, leitura ativa, frases difíceis, vozes, argumento, cronologia e compreensão. No fim, o fichamento sai pronto e os índices mostram como foi a rodada.</p>',
    '<p><b>Estudar</b> usa a lei que você trouxer: o texto é separado em artigos e dividido em seções. Cada seção passa por mapa topográfico, leitura do artigo (a regra em uma frase e as palavras que a banca troca), núcleo, quem faz o quê, regra e exceção, números e prazos, banca (itens Certo/Errado) e compreensão. No fim, o fichamento sai pronto e os índices mostram como foi a rodada.</p>')
rep('A LIO está em <b>versão beta</b>.', 'A LIO-L está em <b>versão beta</b>.')

# ------------------------------------------------------------------ revisão do mediador: rótulos e os grupos novos
rep('${g?grupo("Ideias centrais",g.ideias.length,', '${g?grupo("Regra do artigo",g.ideias.length,')
rep('"Uma pergunta por parágrafo na leitura ativa."', '"Uma pergunta por artigo na leitura: a certa reproduz a regra; as erradas são deturpações."')
rep('${g?grupo("Frases difíceis",g.lab.length,', '${g?grupo("Núcleo",g.lab.length,')
rep('grupo("Vozes: afirmações",g.vozes.af.length,', 'grupo("Quem faz o quê",g.vozes.af.length,')
rep('${sel("v",x.v,vozOps,"De quem é")}', '${sel("v",x.v,vozOps,"Sujeito")}')
rep('${g&&g.arg?grupo("Argumento",g.arg.length,', '${g&&g.arg?grupo("Regra e exceção",g.arg.length,')
rep('"Precisa de uma tese."', '"Precisa de uma regra."')
rep("""  ${P.length?grupo("Perguntas de compreensão",P.length,""", """  ${g&&arr(g.num).length?grupo("Números e prazos",g.num.length,g.num.map((x,k)=>item("num",k,`${fld("campo",x.campo,"A que se refere")}${fld("ok",x.ok,"Certo (como está na lei)")}${fld("no0",x.no[0],"Errada 1")}${fld("no1",x.no[1],"Errada 2")}`)).join("")):""}
  ${g&&arr(g.banca).length?grupo("Banca (Certo/Errado)",g.banca.length,g.banca.map((x,k)=>item("banca",k,`${fld("item",x.item,"Item",true)}${sel("gab",x.gab,[["C","Certo"],["E","Errado"]],"Gabarito")}${sel("tec",x.tec,Object.entries(TECN),"Técnica")}${fld("troca",x.troca,"Palavra da troca (item errado)")}${fld("certo",x.certo,"O que a lei diz no lugar")}${fld("base",x.base,"Trecho da lei que decide",true)}`)).join(""),"Num item errado, a palavra da troca precisa estar escrita no item, senão ele é retirado ao salvar."):""}
  ${P.length?grupo("Perguntas de compreensão",P.length,""")
rep("""    g.termos=lerGrupo("termos").filter(x=>x.termo&&x.sentido).map(x=>({...g.termos[x.k],termo:x.termo,sentido:x.sentido}))}""",
"""    if(arr(g.num).length)g.num=lerGrupo("num").filter(x=>x.campo&&x.ok&&x.no0&&x.no1).map(x=>({...g.num[x.k],campo:x.campo,ok:x.ok,no:[x.no0,x.no1]}));
    if(arr(g.banca).length)g.banca=lerGrupo("banca").filter(x=>x.item&&x.base&&(x.gab==="C"||x.troca&&norm(x.item).includes(norm(x.troca)))).map(x=>({...g.banca[x.k],item:x.item,gab:x.gab,tec:x.gab==="C"?"parafrase_fiel":x.tec,troca:x.gab==="E"?x.troca:"",certo:x.gab==="E"?x.certo:"",base:x.base}));
    g.termos=lerGrupo("termos").filter(x=>x.termo&&x.sentido).map(x=>({...g.termos[x.k],termo:x.termo,sentido:x.sentido}))}""")

# ------------------------------------------------------------------ cartões de revisão e fichamento
rep('tipo:"Ideia do parágrafo"+(R.dif&&R.dif[i]?" · trecho difícil":"")', 'tipo:"Regra do artigo"+(R.dif&&R.dif[i]?" · trecho difícil":"")')
rep('frente:`<p>Do que trata o parágrafo que começa assim?</p><blockquote>${esc(primeira(S.pars[i].t))}</blockquote>`,',
    'frente:`<p>Qual é a regra ${S.pars[i].art?"do <b>"+esc(rotuloUnid(S.pars[i]))+"</b>":"deste trecho"}${S.pars[i].rub?" ("+esc(S.pars[i].rub)+")":""}? Quem, deve ou pode o quê, quando, salvo o quê.</p><blockquote>${esc(S.pars[i].t.split("\\n")[0].slice(0,240))}</blockquote>`,')
rep('verso:`<p><b>Sua etiqueta:</b> ${esc(etq[i])}</p>${ide?`<p><b>Ideia central:</b> ${esc(ide.ok)}</p>`:""}`,texto:S.pars[i].t})}',
    'verso:`<p><b>Sua regra:</b> ${esc(etq[i])}</p>${ide?`<p><b>Regra sem deturpação:</b> ${esc(ide.ok)}</p>`:""}`,texto:S.pars[i].t})}')
rep('frente:`<p>O que significa <b>${esc(gl.termo)}</b> neste texto?</p>`', 'frente:`<p>O que significa <b>${esc(gl.termo)}</b> nesta lei?</p>`')
rep('tipo:"Argumento",onde,pg:pgi(te.p),frente:`<p>Qual é a tese defendida em “${esc(S.titulo)}”? E com que evidências?</p>`,',
    'tipo:"Regra e exceção",onde,pg:pgi(te.p),frente:`<p>Qual é a regra em “${esc(S.titulo)}”? E quais são as exceções?</p>`,')
rep('verso:`<p><b>Tese:</b> ${esc(te.t)}</p>${it.filter(x=>x.r==="evidencia").map(x=>`<p><b>Evidência:</b> ${esc(x.t)}</p>`).join("")}`})}',
    'verso:`<p><b>Regra:</b> ${esc(te.t)}</p>${it.filter(x=>x.r==="evidencia").map(x=>`<p><b>Exceção:</b> ${esc(x.t)}</p>`).join("")}${it.filter(x=>x.r==="premissa").map(x=>`<p><b>Condição:</b> ${esc(x.t)}</p>`).join("")}`})}')
rep('    if(arr(g.crono).length>=3&&R.crono)for(const c of g.crono)',
    '''    if(g.vozes&&R.vozes){const nome=Object.fromEntries(g.vozes.lista.map(v=>[v.id,v.nome]));
      g.vozes.af.forEach((a,k)=>{if(sinal(S,"v"+k))return;out.push({id:`${base}:qf:${k}`,est:id,sec:S.n,tipo:"Quem faz o quê",onde,pg:pgi(a.p),frente:`<p>A quem cabe isto?</p><blockquote>${esc(a.t)}</blockquote>`,verso:`<p><b>${esc(nome[a.v]||"")}</b></p>`})})}
    if(arr(g.num).length&&R.crono)g.num.forEach((x,k)=>{if(sinal(S,"n"+k))return;out.push({id:`${base}:n:${k}`,est:id,sec:S.n,tipo:"Números e prazos",onde,pg:pgi(x.p),frente:`<p>Qual é o número exato?</p><blockquote>${esc(x.campo)}${x.p!=null&&S.pars[x.p]&&S.pars[x.p].art?" · "+esc(S.pars[x.p].art):""}</blockquote>`,verso:`<p><b>${esc(x.ok)}</b></p>`,texto:x.p!=null&&S.pars[x.p]?S.pars[x.p].t:""})});
    if(arr(g.banca).length&&R.banca&&R.banca.it)g.banca.forEach((x,k)=>{const a=R.banca.it[k];if(!a||a.ok||sinal(S,"b"+k))return;out.push({id:`${base}:b:${k}`,est:id,sec:S.n,tipo:a.r==="B"?"Banca · item deixado em branco":"Banca · item em que você errou",onde,pg:pgi(x.p),frente:`<p>Certo ou errado?</p><blockquote>${esc(x.item)}</blockquote>`,verso:`<p><b>${x.gab==="C"?"Certo":"Errado"}</b>${x.gab==="E"?`: <b>${esc(x.troca)}</b> no lugar de <b>${esc(x.certo)}</b>`:""} · ${esc(TECN[x.tec]||"")}</p><p class="note">${esc(x.base)}</p>`})});
    if(arr(g.crono).length>=3&&R.crono)for(const c of g.crono)''')
rep('    crono:arr(g.crono),gloss:arr(R.gloss).filter(x=>x.sentido),',
    '''    af:g.vozes?g.vozes.af.filter((x,k)=>!sinal(S,"v"+k)).map(x=>({n:nome[x.v],t:x.t})):[],num:arr(g.num).filter((x,k)=>!sinal(S,"n"+k)),banca:R.banca&&R.banca.fim?R.banca:null,
    crono:arr(g.crono),gloss:arr(R.gloss).filter(x=>x.sentido),''')
rep('if(d.resumo.length)o+=`### Resumo nas minhas palavras\\n\\n', 'if(d.resumo.length)o+=`### Regras nas minhas palavras\\n\\n')
rep('if(d.arg){o+=`### Argumento\\n\\n`;', 'if(d.af.length)o+=`### Quem faz o quê\\n\\n${d.af.map(x=>`- **${x.n}**: ${x.t}`).join("\\n")}\\n\\n`;\n    if(d.num.length)o+=`### Números e prazos\\n\\n${d.num.map(x=>`- ${x.campo}: **${x.ok}**${pgOf(S,x.p)}`).join("\\n")}\\n\\n`;\n    if(d.banca)o+=`### Banca\\n\\n${d.banca.c} certos, ${d.banca.e} errados, ${d.banca.b} em branco · nota líquida ${d.banca.liq}\\n\\n`;\n    if(d.arg){o+=`### Regra e exceção\\n\\n`;')
rep('return o+"---\\nArgumento, interlocutores e glossário foram preparados com ajuda do Claude a partir do texto. Confira no original antes de citar.\\n"}',
    'return o+"---\\nEstrutura das normas, competências, números e glossário foram preparados com ajuda do Claude a partir do texto da lei. Confira no texto oficial e atualizado antes de usar.\\n"}')

open(_out, 'w', encoding='utf-8').write(s)
print('ok', _out, len(s))
