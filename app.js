const body = document.querySelector('#ranking-body');
const status = document.querySelector('#status');
const updatedAt = document.querySelector('#updated-at');
const refreshButton = document.querySelector('#refresh');

const money = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
const duration = (seconds) => {
  const total = Math.round(Number(seconds));
  return `${Math.floor(total / 60)}min ${String(total % 60).padStart(2, '0')}s`;
};
const date = (value) => new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(value));

function row(item) {
  const tr = document.createElement('tr');
  [ `${item.posicao}º`, item.apelido, money.format(item.valor_ganho), duration(item.tempo_segundos), date(item.data_hora) ]
    .forEach((text) => { const td = document.createElement('td'); td.textContent = text; tr.append(td); });
  return tr;
}

async function loadRanking() {
  refreshButton.disabled = true;
  body.replaceChildren();
  status.textContent = 'Consultando o ranking...';
  try {
    const response = await fetch('/api/ranking');
    if (!response.ok) throw new Error('Não foi possível consultar os resultados.');
    const items = await response.json();
    if (!items.length) status.textContent = 'Ainda não há partidas registradas.';
    else { status.textContent = ''; items.forEach((item) => body.append(row(item))); }
    updatedAt.textContent = `Atualizado em ${new Date().toLocaleString('pt-BR')}`;
  } catch (error) { status.textContent = 'Não foi possível consultar o ranking. Tente novamente.'; updatedAt.textContent = ''; }
  finally { refreshButton.disabled = false; }
}

refreshButton.addEventListener('click', loadRanking);
loadRanking();
