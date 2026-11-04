// Elementos da interface
const body = document.querySelector('#ranking-body');
const status = document.querySelector('#status');
const updatedAt = document.querySelector('#updated-at');
const refreshButton = document.querySelector('#refresh');
const gameFilter = document.querySelector('#game-filter');
const btnConfig = document.querySelector('#btn-config');
const configPanel = document.querySelector('#config-panel');
const inputAnonKey = document.querySelector('#input-anon-key');
const btnSaveKey = document.querySelector('#btn-save-key');

// Formatadores
const money = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });

const duration = (seconds) => {
  const total = Math.round(Number(seconds));
  const min = Math.floor(total / 60);
  const sec = String(total % 60).padStart(2, '0');
  return `${min}min ${sec}s`;
};

const formatDate = (value) => {
  try {
    return new Intl.DateTimeFormat('pt-BR', {
      dateStyle: 'short',
      timeStyle: 'short'
    }).format(new Date(value));
  } catch {
    return value || '-';
  }
};

// Obter configurações do Supabase
function getSupabaseConfig() {
  const config = window.SUPABASE_CONFIG || {};
  const url = (config.url || 'https://mkgbeemjhvpvjmqbwtfl.supabase.co').replace(/\/$/, '');
  const anonKey = config.anonKey || localStorage.getItem('supabase_anon_key') || '';
  return { url, anonKey };
}

// Configuração de cabeçalhos da requisição Supabase
function getHeaders(anonKey) {
  return {
    'apikey': anonKey,
    'Authorization': `Bearer ${anonKey}`,
    'Accept': 'application/json'
  };
}

// Alternar exibição do painel de configuração de chave
if (btnConfig && configPanel) {
  btnConfig.addEventListener('click', () => {
    configPanel.classList.toggle('hidden');
    const { anonKey } = getSupabaseConfig();
    if (inputAnonKey) inputAnonKey.value = anonKey;
  });
}

if (btnSaveKey && inputAnonKey) {
  btnSaveKey.addEventListener('click', () => {
    const key = inputAnonKey.value.trim();
    if (!key) {
      alert('Por favor, informe a chave anon pública do Supabase.');
      return;
    }
    localStorage.setItem('supabase_anon_key', key);
    alert('Chave salva com sucesso!');
    configPanel.classList.add('hidden');
    init();
  });
}

// Renderiza uma linha na tabela
function createRow(item) {
  const tr = document.createElement('tr');
  const values = [
    `${item.posicao}º`,
    item.nome_jogo || '-',
    item.apelido,
    money.format(Number(item.valor_ganho) || 0),
    duration(item.tempo_segundos),
    formatDate(item.data_hora)
  ];

  values.forEach((text) => {
    const td = document.createElement('td');
    td.textContent = text;
    tr.append(td);
  });

  return tr;
}

// Carregar lista de jogos para o select
async function loadGames() {
  const { url, anonKey } = getSupabaseConfig();
  if (!anonKey) {
    status.innerHTML = '⚠️ Chave pública do Supabase não configurada. Clique em <strong>⚙️ Chave Supabase</strong> acima para informá-la.';
    gameFilter.innerHTML = '<option value="">Sem chave de acesso</option>';
    return [];
  }

  try {
    const response = await fetch(`${url}/rest/v1/jogos?select=id,nome&order=nome.asc`, {
      headers: getHeaders(anonKey)
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const games = await response.json();

    gameFilter.innerHTML = '';
    if (!games.length) {
      gameFilter.innerHTML = '<option value="">Nenhum jogo cadastrado</option>';
      return [];
    }

    games.forEach((game) => {
      const option = document.createElement('option');
      option.value = game.id;
      option.textContent = game.nome;
      gameFilter.append(option);
    });

    return games;
  } catch (err) {
    console.error('Erro ao listar jogos:', err);
    gameFilter.innerHTML = '<option value="">Falha ao listar jogos</option>';
    return [];
  }
}

// Ordenação e desempate no cliente (usado caso a view ranking ainda não tenha sido criada no banco)
function processRankingClientSide(partidas, nomeJogo) {
  // Ordenação: 1º Maior valor -> 2º Menor tempo -> 3º Data mais antiga -> 4º ID
  partidas.sort((a, b) => {
    if (Number(b.valor_ganho) !== Number(a.valor_ganho)) {
      return Number(b.valor_ganho) - Number(a.valor_ganho);
    }
    if (Number(a.tempo_segundos) !== Number(b.tempo_segundos)) {
      return Number(a.tempo_segundos) - Number(b.tempo_segundos);
    }
    if (a.data_hora !== b.data_hora) {
      return a.data_hora.localeCompare(b.data_hora);
    }
    return String(a.id).localeCompare(String(b.id));
  });

  // Filtrar melhor partida de cada apelido (sem repetição de apelido)
  const melhores = new Map();
  for (const p of partidas) {
    const apelidoChave = (p.apelido || '').trim().toLowerCase();
    if (!melhores.has(apelidoChave)) {
      melhores.set(apelidoChave, p);
    }
  }

  // Pegar os 10 primeiros e atribuir posição
  return Array.from(melhores.values()).slice(0, 10).map((item, index) => ({
    posicao: index + 1,
    nome_jogo: nomeJogo,
    apelido: item.apelido,
    valor_ganho: item.valor_ganho,
    tempo_segundos: item.tempo_segundos,
    data_hora: item.data_hora
  }));
}

// Carregar o ranking oficial para o jogo selecionado
async function loadRanking() {
  const { url, anonKey } = getSupabaseConfig();
  const selectedGameId = gameFilter.value;
  const selectedGameName = gameFilter.options[gameFilter.selectedIndex]?.text || '';

  if (!anonKey) {
    status.innerHTML = '⚠️ Informe a chave pública do Supabase em <strong>⚙️ Chave Supabase</strong> para consultar os dados.';
    return;
  }

  if (!selectedGameId) {
    body.replaceChildren();
    status.textContent = 'Nenhum jogo selecionado.';
    return;
  }

  refreshButton.disabled = true;
  body.replaceChildren();
  status.textContent = 'Consultando o ranking no Supabase...';

  try {
    // 1. Tenta consultar diretamente da View 'ranking'
    const viewUrl = `${url}/rest/v1/ranking?jogo_id=eq.${selectedGameId}&select=posicao,nome_jogo,apelido,valor_ganho,tempo_segundos,data_hora&order=posicao.asc&limit=10`;
    let response = await fetch(viewUrl, { headers: getHeaders(anonKey) });
    let items = [];

    if (response.ok) {
      items = await response.json();
    } else {
      // 2. Se a view não existir ou der erro, consulta a tabela 'partidas' com fallback inteligente
      console.warn('View ranking não respondeu, usando fallback na tabela partidas.');
      const partidasUrl = `${url}/rest/v1/partidas?jogo_id=eq.${selectedGameId}&select=id,jogo_id,apelido,valor_ganho,tempo_segundos,data_hora`;
      const fallbackResponse = await fetch(partidasUrl, { headers: getHeaders(anonKey) });
      if (!fallbackResponse.ok) {
        throw new Error(`Falha HTTP ${fallbackResponse.status}: ${await fallbackResponse.text()}`);
      }
      const rawPartidas = await fallbackResponse.json();
      items = processRankingClientSide(rawPartidas, selectedGameName);
    }

    if (!items.length) {
      status.textContent = 'Ainda não há partidas registradas para este jogo.';
    } else {
      status.textContent = '';
      items.forEach((item) => body.append(createRow(item)));
    }

    updatedAt.textContent = `Atualizado em ${new Date().toLocaleString('pt-BR')}`;
  } catch (error) {
    console.error('Erro ao consultar ranking:', error);
    status.textContent = 'Não foi possível consultar os resultados online. Verifique sua conexão e a chave configurada.';
    updatedAt.textContent = '';
  } finally {
    refreshButton.disabled = false;
  }
}

// Event Listeners
refreshButton.addEventListener('click', loadRanking);
gameFilter.addEventListener('change', loadRanking);

// Inicialização
async function init() {
  const { anonKey } = getSupabaseConfig();
  if (inputAnonKey && anonKey) inputAnonKey.value = anonKey;

  const games = await loadGames();
  if (games.length) {
    await loadRanking();
  }
}

init();
