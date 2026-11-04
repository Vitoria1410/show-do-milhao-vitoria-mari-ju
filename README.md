# Site do ranking

Publique esta pasta no Vercel. Nas variaveis de ambiente do projeto Vercel, informe `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY`. Nunca coloque a chave de servico no JavaScript do navegador ou no GitHub.

O endpoint `/api/ranking` consulta a view `ranking` do Supabase e o navegador recebe somente os 10 resultados exibidos.
