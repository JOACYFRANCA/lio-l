/* --- Configuração, armazenamento local e API (versão independente) --- */
const CFG_PADRAO={key:"",lembrar:true,mDefault:"claude-sonnet-5-5",mQuick:"claude-haiku-5-5"};
let cfg=Object.assign({},CFG_PADRAO,load("cfg",{}));
if(cfg.via!=="api"&&cfg.via!=="manual")cfg.via=cfg.key?"api":"manual";
let chaveSessao="";
function chave(){return cfg.lembrar?cfg.key:chaveSessao}
function salvarCfg(){const c=Object.assign({},cfg);if(!c.lembrar)c.key="";save("cfg",c)}

const LDB=(()=>{let dbp=null;
  const open=()=>dbp||(dbp=new Promise((res,rej)=>{const r=indexedDB.open("oficina-leitura",1);
    r.onupgradeneeded=()=>r.result.createObjectStore("docs");r.onsuccess=()=>res(r.result);r.onerror=()=>{dbp=null;rej(r.error)}}));
  const req=r=>new Promise((res,rej)=>{r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)});
  const err=e=>({code:e&&e.name==="QuotaExceededError"?"quota_exceeded":"unavailable",message:String(e&&e.message||e)});
  const store=async m=>(await open()).transaction("docs",m).objectStore("docs");
  const getP=async p=>{try{return await req((await store("readonly")).get(p))}catch(e){throw err(e)}};
  const putP=async(p,v)=>{try{await req((await store("readwrite")).put(v,p))}catch(e){throw err(e)}};
  const delP=async p=>{try{await req((await store("readwrite")).delete(p))}catch(e){throw err(e)}};
  const all=async()=>{try{const s=await store("readonly");const [ks,vs]=await Promise.all([req(s.getAllKeys()),req(s.getAll())]);return ks.map((k,i)=>[k,vs[i]])}catch(e){throw err(e)}};
  const cl=o=>o===undefined?undefined:JSON.parse(JSON.stringify(o));
  const merge=(a,b)=>{const o=Object.assign({},a);for(const k in b){const v=b[k];o[k]=v&&typeof v==="object"&&!Array.isArray(v)&&o[k]&&typeof o[k]==="object"&&!Array.isArray(o[k])?merge(o[k],v):v}return o};
  const snap=(id,v)=>({id,exists:v!==undefined,data:()=>cl(v)});
  function doc(path){const id=path.split("/").pop();return {id,path,
    get:async()=>snap(id,await getP(path)),
    set:async d=>putP(path,cl(d)),
    update:async d=>{const cur=await getP(path);if(cur===undefined)throw {code:"invalid_argument",message:"documento inexistente"};await putP(path,merge(cur,cl(d)))},
    delete:async()=>delP(path),
    collection:sub=>col(path+"/"+sub)}}
  function col(path,filt=[],ord=null){return {path,
    doc:id=>doc(path+"/"+(id||Date.now().toString(36)+Math.random().toString(36).slice(2,6))),
    where:(f,op,v)=>col(path,filt.concat([[f,op,v]]),ord),
    orderBy:f=>col(path,filt,f),
    get:async()=>{const pre=path+"/";
      let rows=(await all()).filter(([k])=>k.startsWith(pre)&&!k.slice(pre.length).includes("/"));
      rows=rows.filter(([k,v])=>filt.every(([f,op,val])=>op!=="=="||(v&&v[f]===val)));
      if(ord)rows.sort((a,b)=>(a[1][ord]>b[1][ord])-(a[1][ord]<b[1][ord]));
      const docs=rows.map(([k,v])=>snap(k.slice(pre.length),v));return {docs,size:docs.length,empty:!docs.length}}}}
  return {doc,collection:col,all,putRaw:putP,limpar:async()=>{try{await req((await store("readwrite")).clear())}catch(e){throw err(e)}},ping:open};
})();

function b64(blob){return new Promise((res,rej)=>{const r=new FileReader();r.onload=()=>res(String(r.result).split(",")[1]);r.onerror=()=>rej(r.error);r.readAsDataURL(blob)})}
/* Leitura tolerante de JSON vindo de chats (cópia da tela, blocos de código, pequenos defeitos) */
function jsonReparar(s){let o="",dentro=false,esc=false;
  for(let i=0;i<s.length;i++){const c=s[i];
    if(dentro){
      if(esc){o+=c;esc=false;continue}
      if(c==="\\"){o+=c;esc=true;continue}
      if(c==='"'){let j=i+1;while(j<s.length&&/\s/.test(s[j]))j++;const n=s[j];
        if(j>=s.length||n===","||n===":"||n==="}"||n==="]"){dentro=false;o+=c}else o+='\\"';continue}
      if(c==="\n"){o+="\\n";continue}if(c==="\r")continue;if(c==="\t"){o+="\\t";continue}
      o+=c}
    else{if(c==='"'){dentro=true;o+=c;continue}
      if(c==="/"&&s[i+1]==="/"){while(i<s.length&&s[i]!=="\n")i++;continue}
      o+=c}}
  return o.replace(/,(\s*[}\]])/g,"$1")}
function jsonFechar(s,a){const ab=s[a],fe=ab==="{"?"}":"]";let d=0,dentro=false,esc=false;
  for(let i=a;i<s.length;i++){const c=s[i];
    if(dentro){if(esc)esc=false;else if(c==="\\")esc=true;else if(c==='"'){let j=i+1;while(j<s.length&&/\s/.test(s[j]))j++;const n=s[j];if(j>=s.length||n===","||n===":"||n==="}"||n==="]")dentro=false}continue}
    if(c==='"'){dentro=true;continue}
    if(c==="{"||c==="[")d++;else if(c==="}"||c==="]"){d--;if(d===0)return i}}
  return -1}
function parseFlex(t){
  t=String(t||"").replace(/[\u200b-\u200d\ufeff]/g,"").replace(/\u00a0/g," ")
    .replace(/^[ \t]*(json|JSON|Copiar código|Copy code|Copiar|Copy|Editar|Edit|Code|Código)[ \t]*$/gm,"");
  {const m=t.match(/[\[{]\s*["\[{]/);if(m&&jsonFechar(t,m.index)<0){parseFlex.erro="cortada";return undefined}}
  const cands=[t.trim()];
  for(const m of t.matchAll(/```[a-zA-Z]*\s*([\s\S]*?)```/g))cands.push(m[1]);
  for(let a=0;a<t.length;a++){const c=t[a];if(c!=="{"&&c!=="[")continue;const b=jsonFechar(t,a);
    if(b>a){cands.push(t.slice(a,b+1));if(c==="{"&&b-a>40)a=b}}
  const ab=t.search(/[\[{]/),fe=Math.max(t.lastIndexOf("}"),t.lastIndexOf("]"));if(ab>=0&&fe>ab)cands.push(t.slice(ab,fe+1));
  let melhor,tam=-1,erro="";
  for(const s of cands){for(const x of [s,jsonReparar(s)]){try{const v=JSON.parse(x);if(v&&typeof v==="object"&&x.length>tam){melhor=v;tam=x.length}break}catch(e){erro=erro||e.message}}}
  parseFlex.erro=melhor===undefined?erro:"";return melhor}
function parseTol(t){return parseFlex(t)}
function makeSample(){
  const call=async(input,opt)=>{opt=opt||{};const key=chave();if(!key)throw {code:"sem_chave"};
    const model=opt.modelTier==="quick"?cfg.mQuick:cfg.mDefault;
    try{const content=[];
      for(const b of [].concat(opt.images||[]))content.push({type:"image",source:{type:"base64",media_type:b.type||"image/jpeg",data:await b64(b)}});
      content.push({type:"text",text:String(input)});
      let r;
      try{r=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",signal:opt.signal,
        headers:{"content-type":"application/json","x-api-key":key,"anthropic-version":"2023-06-01","anthropic-dangerous-direct-browser-access":"true"},
        body:JSON.stringify({model,max_tokens:opt.maxTokens||8000,messages:[{role:"user",content}]})})}
      catch(e){if(e&&e.name==="AbortError")throw e;throw {code:"rede"}}
      if(!r.ok){let m="";try{const j=await r.json();m=j&&j.error&&j.error.message||""}catch(e){}
        const c=r.status===401||r.status===403?"chave_invalida":r.status===429?"rate_limited":r.status===404||(r.status===400&&/model/i.test(m))?"modelo":(r.status===400&&/credit|billing|balance/i.test(m))?"saldo":r.status===413?"prompt_too_large":r.status>=500?"upstream_error":"invalid_request";
        throw {code:c,message:m}}
      const j=await r.json();const text=(j.content||[]).filter(x=>x.type==="text").map(x=>x.text).join("");
      if(!text.trim())throw {code:"empty_completion"};
      return {text,truncated:j.stop_reason==="max_tokens"};
    }catch(e){if(e&&e.name==="AbortError")throw {code:"cancelled"};throw e}};
  const fn=(i,o)=>call(i,o);
  fn.json=async(i,o)=>{const {text,truncated}=await call(String(i)+"\n\nResponda somente com o JSON pedido, sem nenhum texto antes ou depois.",o);
    if(truncated)throw {code:"invalid_json",text};const v=parseTol(text);if(v===undefined)throw {code:"invalid_json",text};return v};
  return fn;
}

/* --- Ponte copiar e colar: usa a IA que a pessoa já tem (ChatGPT, Gemini, Claude…), sem chave --- */
let filaPonte=Promise.resolve();
function copiarTexto(t){if(navigator.clipboard&&window.isSecureContext)return navigator.clipboard.writeText(t);
  return new Promise((res,rej)=>{const a=document.createElement("textarea");a.value=t;a.setAttribute("readonly","");a.style.cssText="position:fixed;opacity:0;top:0;left:0";document.body.appendChild(a);a.select();
    try{document.execCommand("copy")?res():rej()}catch(e){rej(e)}a.remove()})}
function estiloPonte(){if(document.getElementById("ponteCss"))return;const st=document.createElement("style");st.id="ponteCss";st.textContent=`
.ponte{position:fixed;inset:0;z-index:40;background:rgba(8,18,36,.55);display:grid;place-items:center;padding:16px}
.ponte-box{background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:16px;box-shadow:0 16px 48px rgba(0,0,0,.3);width:min(620px,100%);max-height:calc(100vh - 32px);overflow:auto;padding:18px 20px;display:flex;flex-direction:column;gap:12px}
.ponte-box h2{font-size:1.1rem}
.ponte-passos{margin:0;padding-left:1.3em;display:flex;flex-direction:column;gap:10px}
.ponte-passos li::marker{font-weight:700;color:var(--accent)}
.ponte-ias{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
.ponte-ias a{text-decoration:none;display:inline-flex;align-items:center}
.ponte textarea{min-height:9rem;font-family:var(--f-mono);font-size:.85rem}
.ponte pre{white-space:pre-wrap;overflow-wrap:anywhere;font:.78rem/1.45 var(--f-mono);max-height:16rem;overflow:auto;margin:0;background:var(--bg);padding:10px;border-radius:8px}
.ponte .erro{color:var(--bad);font-weight:600}`;document.head.appendChild(st)}
function pedidoPonte(texto,json,o){return new Promise((res,rej)=>{estiloPonte();const ant=document.activeElement;
  const w=document.createElement("div");w.className="ponte";w.setAttribute("role","dialog");w.setAttribute("aria-modal","true");w.setAttribute("aria-labelledby","pnT");
  const kb=Math.max(1,Math.round(texto.length/1000));
  w.innerHTML=`<div class="ponte-box"><div class="stack" style="gap:4px"><span class="eyebrow">Pedido para a IA · cerca de ${kb} mil caracteres</span><h2 id="pnT">Use a sua IA para esta etapa</h2></div>
   <ol class="ponte-passos">
    <li><div class="row"><button class="btn primary" id="pnCp" type="button">Copiar o pedido</button><span class="note" id="pnCpOk" role="status"></span></div></li>
    <li>Cole numa conversa da IA que você usa e envie.<div class="ponte-ias"><a class="btn small" href="https://chatgpt.com/" target="_blank" rel="noopener">Abrir o ChatGPT</a><a class="btn small" href="https://gemini.google.com/app" target="_blank" rel="noopener">Abrir o Gemini</a><a class="btn small" href="https://claude.ai/new" target="_blank" rel="noopener">Abrir o Claude</a></div></li>
    <li><label for="pnR">Quando a resposta terminar, copie a resposta inteira e cole aqui${json?" (pode incluir o bloco de código)":""}:</label></li></ol>
   <textarea id="pnR" spellcheck="false" placeholder="Cole aqui a resposta da IA"></textarea>
   <p class="note" id="pnE" role="alert"></p>
   <div class="row"><button class="btn primary" id="pnOk" type="button">Usar esta resposta</button><button class="btn" id="pnX" type="button">Cancelar</button></div>
   <details><summary>Ver o pedido</summary><pre></pre></details>
   <p class="note">Dica: use uma conversa nova para cada estudo. Se a IA pedir confirmação ou fizer perguntas, peça que ela responda só no formato pedido.</p></div>`;
  w.querySelector("pre").textContent=texto;document.body.appendChild(w);
  const fim=(ok,v)=>{w.remove();if(o&&o.signal)o.signal.removeEventListener("abort",ab);try{ant&&ant.focus&&ant.focus()}catch(e){}ok?res(v):rej(v)};
  const ab=()=>fim(false,{code:"cancelled"});if(o&&o.signal){if(o.signal.aborted){ab();return}o.signal.addEventListener("abort",ab)}
  const cp=w.querySelector("#pnCp");cp.onclick=async()=>{try{await copiarTexto(texto);w.querySelector("#pnCpOk").textContent="Copiado. Agora cole na sua IA."}catch(e){w.querySelector("details").open=true;w.querySelector("#pnCpOk").textContent="Não deu para copiar sozinho: abra “Ver o pedido”, selecione tudo e copie."}};
  w.querySelector("#pnX").onclick=()=>fim(false,{code:"cancelled"});
  w.addEventListener("keydown",e=>{if(e.key==="Escape"){e.preventDefault();fim(false,{code:"cancelled"})}});
  w.querySelector("#pnOk").onclick=()=>{const t=w.querySelector("#pnR").value.trim(),E=w.querySelector("#pnE");
    if(!t){E.className="note erro";E.textContent="Cole a resposta da IA no campo acima.";return}
    if(json){const v=parseFlex(t);if(v===undefined){E.className="note erro";
      if(parseFlex.erro==="cortada"){E.innerHTML="A resposta parece ter sido cortada no meio. Na sua IA, peça <b>continue</b> e cole aqui as duas partes juntas, ou envie o pedido de novo numa conversa nova."}
      else{E.innerHTML='A LIO não encontrou os dados no formato pedido. Confira se copiou a resposta inteira. Se copiou, leve este pedido de correção à IA e cole a nova resposta aqui. <button class="btn small" type="button" id="pnFix">Copiar pedido de correção</button>';
        const erro=parseFlex.erro;E.querySelector("#pnFix").onclick=async()=>{try{await copiarTexto("A sua resposta anterior não é um JSON válido"+(erro?" (erro: "+erro+")":"")+". Reenvie a resposta completa, somente o JSON, em um único bloco de código, com aspas duplas retas e sem comentários.");E.querySelector("#pnFix").textContent="Copiado"}catch(e){}}}
      return}fim(true,v)}
    else fim(true,t)};
  setTimeout(()=>cp.focus(),0)})}
function makePonte(){
  const run=(t,json,o)=>{const p=filaPonte.then(()=>pedidoPonte(t,json,o));filaPonte=p.catch(()=>{});return p};
  const fn=async(i,o)=>{if(o&&o.images&&o.images.length)throw {code:"invalid_request",message:"imagens"};return {text:await run(String(i),false,o),truncated:false}};
  fn.json=async(i,o)=>run(String(i)+"\n\nResponda somente com o JSON pedido, em um único bloco de código, sem nenhum texto antes ou depois.",true,o);
  return fn}
const baixarLocal={save:async({filename,data})=>{const blob=data instanceof Blob?data:new Blob([data],{type:/\.html$/.test(filename)?"text/html;charset=utf-8":/\.json$/.test(filename)?"application/json":/\.csv$/.test(filename)?"text/csv;charset=utf-8":"text/markdown;charset=utf-8"});
  const u=URL.createObjectURL(blob),a=document.createElement("a");a.href=u;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),4000);return {status:"saved"}}};

let modo=load("modo",null);
(()=>{let h=(location.hash||"").replace("#","");if(h==="participante")h="aluno";if(h==="professor"||h==="mediador"||h==="aluno"){modo=h==="aluno"?"aluno":"prof";save("modo",modo);if(h!=="aluno")save("modoUso","mediador")}})();
if(modo!=="prof"&&modo!=="aluno")modo=(chave()||cfg.via==="manual")?"prof":"aluno";
const ehAluno=()=>modo==="aluno";
const CAP={ready:false,db:null,user:null,sample:null,dl:baixarLocal,uid:null,imgMax:0};
function atualizarSample(){const m=cfg.via==="manual";CAP.sample=ehAluno()?null:m?makePonte():chave()?makeSample():null;CAP.imgMax=CAP.sample&&!m?6:0;CAP.ponte=m}
async function initCaps(){
  try{if(!window.indexedDB)throw 0;await LDB.ping();CAP.db=LDB;CAP.uid="local";CAP.prof=!ehAluno()}catch(e){CAP.db=null}
  atualizarSample();CAP.ready=true;
  if(tab==="estudo"&&est.view==="lib")estRender();
  if(["ex1","ex2","ex3"].includes(tab)&&usandoPDF())go();
  if(tab==="revisar")renderRev();
  renderTabs();if(tab==="prof"){if(CAP.prof&&mediando())renderProf();else{tab="inicio";go()}}else if(tab==="inicio")renderInicio();
}
