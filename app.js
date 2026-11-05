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
  if (anonKey.startsWith('sb_secret_')) throw new Error('Use somente a chave pública no site.');
  if (anonKey.split('.').length === 3) {
    let role;
    try { role = JSON.parse(atob(anonKey.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'))).role; } catch {}
    if (role === 'service_role') throw new Error('Uma chave administrativa não pode ser usada no site.');
  }
  const headers = {
    'apikey': anonKey,
    'Accept': 'application/json'
  };
  if (!anonKey.startsWith('sb_publishable_')) headers.Authorization = `Bearer ${anonKey}`;
  return headers;
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
    try { getHeaders(key); } catch (error) { alert(error.message); return; }
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
    status.textContent = 'Não foi possível listar os jogos online. Verifique a conexão e tente novamente.';
    return [];
  }
}

// Carregar o ranking oficial para o jogo selecionado
async function loadRanking() {
  const { url, anonKey } = getSupabaseConfig();
  const selectedGameId = gameFilter.value;

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
    const viewUrl = `${url}/rest/v1/ranking?jogo_id=eq.${encodeURIComponent(selectedGameId)}&select=posicao,nome_jogo,apelido,valor_ganho,tempo_segundos,data_hora&order=posicao.asc&limit=10`;
    const response = await fetch(viewUrl, { headers: getHeaders(anonKey) });
    if (!response.ok) throw new Error(`Falha HTTP ${response.status}`);
    const items = await response.json();

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
refreshButton.addEventListener('click', async () => {
  if (!gameFilter.value) {
    await init();
  } else {
    await loadRanking();
  }
});
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
