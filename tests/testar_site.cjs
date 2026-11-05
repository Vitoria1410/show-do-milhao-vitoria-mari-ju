const fs=require('fs'),vm=require('vm'),assert=require('assert');
const repo=require('path').resolve(__dirname,'..')+'/';
const elements={};
function el(){return {value:'1',textContent:'',innerHTML:'',disabled:false,options:[{text:'Jogo'}],selectedIndex:0,children:[],classList:{toggle(){},add(){}},addEventListener(){},replaceChildren(...items){this.children=[...items]},append(x){this.children.push(x)}}}
const context={document:{querySelector(s){return elements[s]??=el()},createElement:el},window:{SUPABASE_CONFIG:{url:'https://example.com',anonKey:'teste'}},localStorage:{getItem(){return ''}},console:{error(){},warn(){}},Intl,Date,Map,Number,String,atob,alert(){},fetch:async()=>({ok:true,json:async()=>[]})};
vm.createContext(context); vm.runInContext(fs.readFileSync(repo+'app.js','utf8'),context);
const checks=[];
async function test(name,fn){try{await fn();checks.push('PASSOU: '+name)}catch(e){checks.push('FALHOU: '+name+' — '+e.message);process.exitCode=1}}
(async()=>{
 await new Promise(r=>setImmediate(r));
 await test('Formatação monetária e duração',()=>{assert.match(vm.runInContext('money.format(1000000)',context),/1\.000\.000,00/);assert.equal(vm.runInContext('duration(125)',context),'2min 05s')});
 await test('Renderização preserva dados e posição do ranking oficial',()=>{
  const row=context.createRow({posicao:2,nome_jogo:'Jogo A',apelido:'<script>teste</script>',valor_ganho:5000,tempo_segundos:65,data_hora:'2026-11-04T12:00:00Z'});
  assert.equal(row.children[0].textContent,'2º');assert.equal(row.children[1].textContent,'Jogo A');
  assert.equal(row.children[2].textContent,'<script>teste</script>');assert.equal(row.children[4].textContent,'1min 05s');
 });
 elements['#game-filter'].value='1';
 await test('Ranking vazio mostra mensagem',async()=>{context.fetch=async()=>({ok:true,json:async()=>[]});await context.loadRanking();assert.match(elements['#status'].textContent,/não há partidas/)});
 await test('Falha de rede mostra mensagem e reativa atualização',async()=>{context.fetch=async()=>{throw Error('offline')};await context.loadRanking();assert.match(elements['#status'].textContent,/Não foi possível/);assert.equal(elements['#refresh'].disabled,false)});
 await test('Consulta oficial usa filtro de jogo e top 10',async()=>{let url;context.fetch=async u=>{url=u;return {ok:true,json:async()=>[]}};await context.loadRanking();assert.match(url,/jogo_id=eq\.1/);assert.match(url,/limit=10/)});
 await test('Falha ao listar jogos informa erro visível',async()=>{elements['#status'].textContent='';context.fetch=async()=>{throw Error('offline')};await context.loadGames();assert.match(elements['#game-filter'].innerHTML,/Falha ao listar jogos/);assert.match(elements['#status'].textContent,/Não foi possível listar/)});
 await test('Falha da view não consulta partidas brutas',async()=>{let chamadas=[];context.fetch=async u=>{chamadas.push(u);return {ok:false,status:403}};elements['#game-filter'].value='1';await context.loadRanking();assert.equal(chamadas.length,1);assert.match(chamadas[0],/rest\/v1\/ranking\?/);assert.match(elements['#status'].textContent,/Não foi possível/)});
 await test('Chave moderna usa apenas apikey',()=>{const h=context.getHeaders('sb_publishable_exemplo');assert.equal(h.apikey,'sb_publishable_exemplo');assert.equal(h.Authorization,undefined)});
 await test('Site rejeita chave administrativa moderna e legada',()=>{assert.throws(()=>context.getHeaders('sb_secret_exemplo'));const payload=Buffer.from(JSON.stringify({role:'service_role'})).toString('base64');assert.throws(()=>context.getHeaders('cabecalho.'+payload+'.assinatura'))});
 await test('Consultas simultâneas não duplicam linhas nem exibem resposta antiga',async()=>{
  const pendentes=[];context.fetch=()=>new Promise(resolve=>pendentes.push(resolve));elements['#game-filter'].value='1';
  const primeira=context.loadRanking(),segunda=context.loadRanking();
  const item=apelido=>({posicao:1,nome_jogo:'Jogo',apelido,valor_ganho:1000,tempo_segundos:30,data_hora:'2026-11-04T12:00:00Z'});
  pendentes[1]({ok:true,json:async()=>[item('Atual')]});await segunda;
  pendentes[0]({ok:true,json:async()=>[item('Antigo')]});await primeira;
  assert.equal(elements['#ranking-body'].children.length,1);
  assert.equal(elements['#ranking-body'].children[0].children[2].textContent,'Atual');
 });
 console.log(checks.join('\n'));
})();
