import os,sys
# uso: python3 build.py                 → lio-local.html (LIO-E, a partir do lio.html)
#      python3 build.py ../lio-l.html   → lio-l-local.html (LIO-L)
_arg=sys.argv[1] if len(sys.argv)>1 else 'lio.html'
_src=_arg if os.path.exists(_arg) else os.path.join('..',_arg)
LEIS=os.path.basename(_src).startswith('lio-l')
_saida='lio-l-local.html' if LEIS else 'lio-local.html'
s=open(_src).read()
# o código-fonte já é um documento completo: retira o esqueleto para montar o da versão independente
if s.lstrip().lower().startswith('<!doctype'):
    s=s.split('<meta name="viewport" content="width=device-width,initial-scale=1">\n',1)[1]
    s=s.replace('\nbody{margin:0}\n[hidden]{display:none!important}\nimg{max-width:100%}','',1)
    s=s.replace('\n</head>\n<body>\n','\n',1)
    s=s.rstrip()
    assert s.endswith('</body>\n</html>')
    s=s[:-len('</body>\n</html>')].rstrip()+'\n'
parts=open('local_parts.js').read(); conf=open('local_config.js').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(n,a[:60]); s=s.replace(a,b)
def rep_region(a,b,new):
    global s
    i=s.index(a); j=s.index(b,i); s=s[:i]+new+s[j:]
rep_region('/* --- Capacidades --- */','let toastT=null;',parts)
rep_region('function sampleMsg(e){','const uCol=','''function sampleMsg(e){return ({sem_chave:"Configure a chave da API em Configurações.",chave_invalida:"A chave da API foi recusada. Confira em Configurações.",
  saldo:"A conta da API está sem créditos. Adicione créditos em console.anthropic.com.",modelo:"O modelo configurado não existe ou não está disponível para esta chave. Confira em Configurações.",
  rede:"Sem conexão com a API da Anthropic. Verifique a internet.",rate_limited:"Limite de uso da API atingido por agora. Tente de novo em alguns minutos.",
  invalid_json:"A resposta veio incompleta. Tente de novo; se repetir, use um trecho menor.",prompt_too_large:"O trecho é grande demais para uma vez só.",
  empty_completion:"A resposta veio vazia. Tente de novo.",cancelled:"Pedido cancelado. Tente de novo quando quiser.",upstream_error:"A API da Anthropic está instável agora. Tente de novo em instantes.",
  invalid_request:"A API recusou o pedido."+(e&&e.message?" ("+e.message+")":"")})[e&&e.code]||"Algo falhou ao falar com a API. Tente de novo."}

''')
rep('["prog","","Progresso"],["prof","","Mediador"]];','["prog","","Progresso"],["prof","","Mediador"],["config","","Ajustes"]];')
rep('revisar:renderRev,prof:renderProf})','revisar:renderRev,prof:renderProf,config:renderConfig})')
rep('<button class="mtoast" id="mtoast" type="button" hidden></button>','')
rep('Conectando ao Claude…','Abrindo o armazenamento local…')
rep('versão para Claude (artefato do claude.ai)','versão independente (navegador), derivada da versão para Claude')
rep('O modo Estudo guarda seus textos e anotações numa área privada da sua conta. Ele funciona com a página aberta no claude.ai, com você conectado e com permissão para salvar.',
    'O navegador não permitiu o armazenamento local. Abra este arquivo no Chrome, Edge ou Firefox, fora de uma janela anônima.')
rep('''${CAP.sample?"":'<span class="note">Sem acesso ao Claude nesta visualização: dá para ler e anotar, mas não preparar exercícios.</span>'}''',
    '''${CAP.sample?"":'<span class="note">Sem chave da API: dá para ler e anotar, mas não preparar exercícios. <button class="linkbtn" id="tocfg">Configurar a chave</button></span>'}''')
rep('''  $("#novo").onclick=()=>estGo("novo",{nv:{}});''','''  $("#novo").onclick=()=>estGo("novo",{nv:{}});
  if($("#tocfg"))$("#tocfg").onclick=()=>{tab="config";save("tab",tab);go()};''')
rep('O PDF não é guardado. Só o texto do trecho escolhido e as suas anotações ficam salvos, numa área que só você vê.',
    'O PDF não é guardado. O texto do trecho e as suas anotações ficam salvos neste navegador, neste computador. Faça backups em Configurações.')
rep('Leva de 30 segundos a 2 minutos e usa a sua conta Claude.','Leva de 30 segundos a 2 minutos e é cobrado na sua chave da API.')
rep('''</div>`:""}
  <div class="stack" id="st"></div>`;''','''</div>`:""}
  ${!S.gen&&!CAP.sample?'<div class="panel"><b>Exercícios desta seção</b><p>Para preparar as perguntas, configure a chave da API em Configurações. Mapa, leitura com etiquetas e glossário funcionam sem ela.</p></div>':""}
  <div class="stack" id="st"></div>`;''')
rep(' Nesta visualização não dá para lê-las por imagem; o estudo seguirá sem elas.',' Configure a chave da API em Configurações para lê-las por imagem; sem isso, o estudo seguirá sem elas.')
rep('{images:blobs,signal:ctl.signal,cache:false}','{images:blobs,signal:ctl.signal,cache:false,maxTokens:16000}')
rep('/* ---------------- Relógio da sessão e tamanho da letra ---------------- */',conf+'/* ---------------- Relógio da sessão e tamanho da letra ---------------- */')
# documento completo
i=s.index('</style>')+len('</style>')
head='<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
s=head+s[:i].replace('*{box-sizing:border-box}','*{box-sizing:border-box}\nbody{margin:0}\n[hidden]{display:none!important}\nimg{max-width:100%}')+'\n</head>\n<body>\n'+s[i:].lstrip()+'\n</body>\n</html>\n'
rep('const SEM_GEN="A preparação precisa do Claude, que não está disponível nesta visualização.";','const SEM_GEN="Para prepará-los, configure a chave da API em Configurações.";')
rep('function semGen(){return SEM_GEN}','function semGen(){return ehAluno()?"Esta parte usa IA, que não está ligada neste site. Use as atividades com exercícios prontos que o mediador enviar.":SEM_GEN}')
rep("'<span class=\"note\">Sem chave da API: dá para ler e anotar, mas não preparar exercícios. <button class=\"linkbtn\" id=\"tocfg\">Configurar a chave</button></span>'",
    "(ehAluno()?'<span class=\"note\">Sem IA neste site: use as atividades que o mediador enviar, ou estude um texto seu com mapa, leitura ativa, glossário, mapas e revisão.</span>':'<span class=\"note\">Sem chave da API: dá para ler e anotar, mas não preparar exercícios. <button class=\"linkbtn\" id=\"tocfg\">Configurar a chave</button></span>')")
rep('<p>Para preparar as perguntas, configure a chave da API em Configurações. Mapa, leitura com etiquetas e glossário funcionam sem ela.</p>',
    "<p>'+(ehAluno()?'Esta seção não tem exercícios prontos. Mapa, leitura com etiquetas, glossário e revisão funcionam normalmente.':'Para preparar as perguntas, configure a chave da API em Configurações. Mapa, leitura com etiquetas e glossário funcionam sem ela.')+'</p>")
rep('" Configure a chave da API em Configurações para lê-las por imagem; sem isso, o estudo seguirá sem elas."','(ehAluno()?" Neste site elas não podem ser lidas; o estudo seguirá sem elas.":" Configure a chave da API em Configurações para lê-las por imagem; sem isso, o estudo seguirá sem elas.")')
if LEIS:s=s.replace('"oficina-leitura"','"lio-leis"')   # banco local e backups separados da LIO-E
open(_saida,'w').write(s)
print('ok',len(s))
