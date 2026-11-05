const fs=require('fs'),vm=require('vm'),assert=require('assert');
const repo=require('path').resolve(__dirname,'..')+'/';
const elements={};
function el(){return {value:'1',textContent:'',innerHTML:'',disabled:false,options:[{text:'Jogo'}],selectedIndex:0,children:[],classList:{toggle(){},add(){}},addEventListener(){},replaceChildren(){this.children=[]},append(x){this.children.push(x)}}}
const context={document:{querySelector(s){return elements[s]??=el()},createElement:el},window:{SUPABASE_CONFIG:{url:'https://example.com',anonKey:'teste'}},localStorage:{getItem(){return ''}},console:{error(){},warn(){}},Intl,Date,Map,Number,String,alert(){},fetch:async()=>({ok:true,json:async()=>[]})};
vm.createContext(context); vm.runInContext(fs.readFileSync(repo+'app.js','utf8'),context);
const checks=[];
async function test(name,fn){try{await fn();checks.push('PASSOU: '+name)}catch(e){checks.push('FALHOU: '+name+' — '+e.message);process.exitCode=1}}
(async()=>{
 await new Promise(r=>setImmediate(r));
 await test('Formatação monetária e duração',()=>{assert.match(vm.runInContext('money.format(1000000)',context),/1\.000\.000,00/);assert.equal(vm.runInContext('duration(125)',context),'2min 05s')});
 await test('Ranking: prêmio, tempo, data, ID e melhor apelido',()=>{
  const rows=[['4','Ana',5000,20],['2','Bia',5000,10],['1','Cris',5000,10],['3',' ANA ',1000,5]].map(([id,apelido,valor_ganho,tempo_segundos])=>({id,apelido,valor_ganho,tempo_segundos,data_hora:'2026-11-04T10:00:00Z'}));
  const out=context.processRankingClientSide(rows,'Jogo');assert.equal(out.map(x=>x.apelido).join(','),'Cris,Bia,Ana');
 });
 elements['#game-filter'].value='1';
 await test('Ranking vazio mostra mensagem',async()=>{context.fetch=async()=>({ok:true,json:async()=>[]});await context.loadRanking();assert.match(elements['#status'].textContent,/não há partidas/)});
 await test('Falha de rede mostra mensagem e reativa atualização',async()=>{context.fetch=async()=>{throw Error('offline')};await context.loadRanking();assert.match(elements['#status'].textContent,/Não foi possível/);assert.equal(elements['#refresh'].disabled,false)});
 await test('Consulta oficial usa filtro de jogo e top 10',async()=>{let url;context.fetch=async u=>{url=u;return {ok:true,json:async()=>[]}};await context.loadRanking();assert.match(url,/jogo_id=eq\.1/);assert.match(url,/limit=10/)});
 await test('Falha ao listar jogos informa erro visível',async()=>{elements['#status'].textContent='';context.fetch=async()=>{throw Error('offline')};await context.loadGames();assert.match(elements['#game-filter'].innerHTML,/Falha ao listar jogos/);assert.match(elements['#status'].textContent,/Não foi possível listar/)});
 console.log(checks.join('\n'));
})();
