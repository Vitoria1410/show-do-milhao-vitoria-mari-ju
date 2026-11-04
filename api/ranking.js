export default async function handler(request, response) {
  const { SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY } = process.env;
  if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY) {
    return response.status(500).json({ error: 'Configuração do servidor ausente.' });
  }

  const url = new URL(`${SUPABASE_URL}/rest/v1/ranking`);
  url.searchParams.set('select', 'posicao,apelido,valor_ganho,tempo_segundos,data_hora');
  url.searchParams.set('order', 'posicao.asc');
  url.searchParams.set('limit', '10');

  try {
    const result = await fetch(url, {
      headers: { apikey: SUPABASE_SERVICE_ROLE_KEY, Authorization: `Bearer ${SUPABASE_SERVICE_ROLE_KEY}` }
    });
    if (!result.ok) throw new Error('Supabase respondeu com erro');
    response.setHeader('Cache-Control', 'no-store');
    return response.status(200).json(await result.json());
  } catch {
    return response.status(502).json({ error: 'Falha ao consultar o banco.' });
  }
}
