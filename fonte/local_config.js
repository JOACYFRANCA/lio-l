/* ---------------- Configurações (versão independente) ---------------- */
function renderConfig(){
  const tem=!!chave();
  main.innerHTML=`<div class="stack"><span class="eyebrow">Versão independente</span><h1>Configurações</h1>
  <p class="lead">${ehAluno()?"Neste modo a LIO não usa IA: as atividades chegam prontas do mediador, e tudo o que você faz fica guardado neste navegador.":cfg.via==="manual"?"Esta versão roda inteira no seu navegador. Os textos e as anotações ficam neste computador. Quando uma etapa precisa de IA, a LIO prepara o pedido e você o leva à IA que já usa.":"Esta versão roda inteira no seu navegador. Os textos e as anotações ficam neste computador; a IA só é chamada, pela sua chave da API, quando você prepara exercícios ou lê páginas escaneadas."}</p></div>

  <div class="stack"><h2>Modo do site</h2>
  <div class="subtabs"><button class="chip" data-modo="aluno" aria-pressed="${ehAluno()}">Participante (sem IA)</button><button class="chip" data-modo="prof" aria-pressed="${!ehAluno()}">Com IA</button></div>
  <p class="note">No modo Participante, as perguntas abertas são comparadas com a referência pelo próprio participante, e as funções que dependem de IA ficam escondidas. No modo Com IA aparecem a escolha de mediar um grupo e a configuração da IA. Para abrir o site direto num modo, use o endereço terminado em #aluno ou #mediador.</p></div>

  <div class="stack" id="secUso"><h2>Como você usa a LIO</h2>
  <div class="subtabs"><button class="chip" data-uso="autonomo" aria-pressed="${modoUso()!=="mediador"}">Estudo por conta própria</button><button class="chip" data-uso="mediador" aria-pressed="${modoUso()==="mediador"}">Mediar um grupo</button></div>
  <p class="note">Mediar um grupo mostra a aba Mediador, para preparar atividades e distribuí-las por arquivo. Pode ser professor, tutor ou um colega que organiza o estudo.</p></div>

  <div class="stack" id="secVia"><h2>Como a LIO usa a IA</h2>
  <div class="choices"><button class="choice" data-via="manual" aria-pressed="${cfg.via==="manual"}"><b>Copiar e colar</b><span>Com a IA que você já usa: ChatGPT, Gemini, Claude ou outra, inclusive gratuitas. Sem chave e sem custo extra. Você copia o pedido, cola na IA e traz a resposta de volta.</span></button>
  <button class="choice" data-via="api" aria-pressed="${cfg.via==="api"}"><b>Automático</b><span>A LIO chama a IA sozinha, com uma chave da API da Anthropic. Mais rápido, mas a API é paga à parte e precisa de configuração.</span></button></div>
  <p class="note">No modo copiar e colar, a leitura de páginas escaneadas por imagem não está disponível.</p></div>

  <div class="stack" id="secChave"><h2>Chave da API da Anthropic</h2>
  <p>Crie a chave em <b>console.anthropic.com</b>, na área API Keys. A conta da API é separada da assinatura do Claude e precisa ter créditos; o custo é cobrado por uso.</p>
  <div class="field"><label for="ck">Chave${tem?" (já configurada)":""}</label><input id="ck" type="password" autocomplete="off" placeholder="${tem?"•••••••• (deixe em branco para manter)":"sk-ant-..."}"></div>
  <label class="row" style="gap:8px"><input type="checkbox" id="cl" ${cfg.lembrar?"checked":""}> Lembrar a chave neste navegador</label>
  <p class="note">Desmarcado, a chave vale só até fechar a página. Não deixe a chave salva em computador compartilhado: quem usar o navegador pode usá-la.</p>
  <div class="row"><button class="btn primary" id="cs">Salvar chave</button><button class="btn" id="ct" ${tem?"":"disabled"}>Testar</button><button class="btn" id="cx" ${tem?"":"disabled"}>Apagar chave</button></div>
  <p class="note" id="cst"></p></div>

  <div class="stack" id="secModelos"><h2>Modelos</h2>
  <div class="grid2"><div class="field"><label for="md1">Para exercícios e páginas escaneadas</label><input id="md1" value="${esc(cfg.mDefault)}"></div>
  <div class="field"><label for="md2">Para tarefas rápidas (glossário, teste)</label><input id="md2" value="${esc(cfg.mQuick)}"></div></div>
  <p class="note">Se a Anthropic lançar modelos novos ou aposentar estes, troque o nome aqui. A lista atual está em docs.claude.com.</p>
  <div class="row"><button class="btn" id="ms">Salvar modelos</button><button class="btn" id="mr">Voltar ao padrão</button></div></div>

  <div class="stack"><h2>Backup</h2>
  <p>Tudo fica guardado no navegador. Se os dados de navegação forem apagados, os estudos se perdem. Exporte um backup toda semana e guarde o arquivo junto com os PDFs do curso.</p>
  <div class="row"><button class="btn primary" id="bx">Exportar backup</button><label class="btn" for="bi" style="display:inline-block">Importar backup<input type="file" id="bi" accept=".json,application/json" hidden></label></div>
  <p class="note" id="bst"></p></div>

  <div class="stack"><h2>Apagar tudo</h2>
  <p>Remove todos os estudos, anotações e o progresso do treino deste navegador. A chave e os modelos continuam.</p>
  <div class="row" id="zz"><button class="btn" id="za">Apagar todos os dados</button></div></div>`;

  if(ehAluno()){$("#secChave").hidden=true;$("#secModelos").hidden=true;$("#secVia").hidden=true;$("#secUso").hidden=true}
  else if(cfg.via==="manual"){$("#secChave").hidden=true;$("#secModelos").hidden=true}
  main.querySelectorAll("[data-uso]").forEach(b=>b.onclick=()=>{save("modoUso",b.dataset.uso);renderTabs();toast(b.dataset.uso==="mediador"?"Aba Mediador ligada.":"Estudo por conta própria.");renderConfig()});
  main.querySelectorAll("[data-via]").forEach(b=>b.onclick=()=>{cfg.via=b.dataset.via;salvarCfg();atualizarSample();toast(cfg.via==="manual"?"Modo copiar e colar: use a sua IA.":chave()?"Modo automático.":"Modo automático: configure a chave abaixo.");renderConfig()});
  main.querySelectorAll("[data-modo]").forEach(b=>b.onclick=()=>{modo=b.dataset.modo;save("modo",modo);atualizarSample();CAP.prof=!ehAluno();renderTabs();toast(ehAluno()?"Modo Participante: sem IA.":"Modo com IA.");renderConfig()});
  $("#cs").onclick=()=>{const v=$("#ck").value.trim();cfg.lembrar=$("#cl").checked;
    if(v){if(cfg.lembrar)cfg.key=v;else{cfg.key="";chaveSessao=v}}
    else if(!cfg.lembrar&&cfg.key){chaveSessao=cfg.key;cfg.key=""}
    else if(cfg.lembrar&&!cfg.key&&chaveSessao){cfg.key=chaveSessao}
    salvarCfg();atualizarSample();toast(chave()?"Chave salva.":"Nenhuma chave informada.");renderConfig()};
  $("#cx").onclick=()=>{cfg.key="";chaveSessao="";salvarCfg();atualizarSample();toast("Chave apagada.");renderConfig()};
  $("#ct").onclick=async()=>{$("#ct").disabled=true;$("#cst").innerHTML='<span class="spin"></span>Testando…';
    try{await CAP.sample("Responda apenas: ok",{modelTier:"quick",maxTokens:10});
      try{await CAP.sample("Responda apenas: ok",{maxTokens:10});$("#cst").textContent="A chave e os dois modelos funcionam."}
      catch(e){$("#cst").textContent="A chave funciona, mas o modelo de exercícios falhou: "+sampleMsg(e)}}
    catch(e){$("#cst").textContent=sampleMsg(e)}
    $("#ct").disabled=false};
  $("#ms").onclick=()=>{cfg.mDefault=$("#md1").value.trim()||CFG_PADRAO.mDefault;cfg.mQuick=$("#md2").value.trim()||CFG_PADRAO.mQuick;salvarCfg();toast("Modelos salvos.")};
  $("#mr").onclick=()=>{cfg.mDefault=CFG_PADRAO.mDefault;cfg.mQuick=CFG_PADRAO.mQuick;salvarCfg();renderConfig();toast("Modelos padrão restaurados.")};
  $("#bx").onclick=async()=>{try{const rows=await LDB.all();
      const data={app:"oficina-leitura",versao:1,exportado:agora(),docs:Object.fromEntries(rows),treino:load("prog",{})};
      await baixarLocal.save({filename:`lio-backup-${new Date().toISOString().slice(0,10)}.json`,data:JSON.stringify(data)});
      $("#bst").textContent=`Backup exportado: ${rows.filter(([k])=>/\/est_[^/]+$/.test(k)).length} estudo(s).`}
    catch(e){$("#bst").textContent="Não foi possível exportar o backup."}};
  $("#bi").onchange=async e=>{const f=e.target.files[0];if(!f)return;
    let d;try{d=JSON.parse(await f.text())}catch(x){$("#bst").textContent="Este arquivo não é um backup válido.";return}
    if(!d||d.app!=="oficina-leitura"||typeof d.docs!=="object"){$("#bst").textContent="Este arquivo não é um backup da LIO.";return}
    const n=Object.keys(d.docs).filter(k=>/\/est_[^/]+$/.test(k)).length;
    $("#bst").innerHTML=`O backup tem ${n} estudo(s). Estudos com o mesmo identificador serão substituídos. <button class="btn small" id="bok">Importar agora</button>`;
    $("#bok").onclick=async()=>{try{for(const [k,v] of Object.entries(d.docs))if(typeof k==="string"&&k.startsWith("data/users/local/"))await LDB.putRaw(k,v);
        if(d.treino&&typeof d.treino==="object"){const p=load("prog",{});for(const k in d.treino)if(Array.isArray(d.treino[k]))p[k]=d.treino[k];save("prog",p)}
        $("#bst").textContent=`Backup importado: ${n} estudo(s).`;est.view="lib"}
      catch(x){$("#bst").textContent=x&&x.code==="quota_exceeded"?"O navegador ficou sem espaço para importar.":"Não foi possível importar o backup."}}};
  $("#za").onclick=()=>{$("#zz").innerHTML='<span class="note">Apagar todos os estudos e o progresso? Não dá para desfazer.</span><button class="btn small" id="zy">Apagar</button><button class="btn small" id="zn">Cancelar</button>';
    $("#zn").onclick=renderConfig;
    $("#zy").onclick=async()=>{try{await LDB.limpar();save("prog",{});est={view:"lib",list:null,id:null,meta:null,secoes:null,si:0,step:"mapa",nv:null,job:null};tp={id:null,meta:null,secoes:null,lista:null,carregando:false,erro:null};tpDados=null;rv={dados:null,carregando:false,ses:null,erro:null};pf={view:"home",lista:null,estudos:null,A:null,si:0,turma:null,carregando:false,job:null};fonte={tipo:"ex",id:null,n:0};save("fonte",fonte);resetRuns();toast("Dados apagados.")}catch(x){toast("Não foi possível apagar.")}renderConfig()}};
}

