-- Migração não destrutiva: preserva perguntas e partidas existentes.
BEGIN;
CREATE OR REPLACE VIEW public.ranking AS
WITH melhor_partida_por_jogador AS (
    SELECT 
        p.id AS partida_id,
        p.jogo_id,
        j.nome AS nome_jogo,
        p.apelido,
        p.valor_ganho,
        p.tempo_segundos,
        p.data_hora,
        ROW_NUMBER() OVER (
            PARTITION BY p.jogo_id, LOWER(TRIM(p.apelido))
            ORDER BY 
                p.valor_ganho DESC,
                p.tempo_segundos ASC,
                p.data_hora ASC,
                p.id ASC
        ) AS rn
    FROM public.partidas p
    JOIN public.jogos j ON j.id = p.jogo_id
),
partidas_filtradas AS (
    SELECT *
    FROM melhor_partida_por_jogador
    WHERE rn = 1
)
SELECT 
    partida_id,
    jogo_id,
    nome_jogo,
    apelido,
    valor_ganho,
    tempo_segundos,
    data_hora,
    ROW_NUMBER() OVER (
        PARTITION BY jogo_id
        ORDER BY 
            valor_ganho DESC,
            tempo_segundos ASC,
            data_hora ASC,
            partida_id ASC
    ) AS posicao
FROM partidas_filtradas;

-- 5. PERMISSÕES: navegador somente lê jogos e ranking.
ALTER TABLE public.jogos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.perguntas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.partidas ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Leitura pública de jogos" ON public.jogos;
CREATE POLICY "Leitura pública de jogos" ON public.jogos FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS "Inserção pública de jogos" ON public.jogos;
DROP POLICY IF EXISTS "Leitura pública de perguntas" ON public.perguntas;
DROP POLICY IF EXISTS "Inserção pública de partidas" ON public.partidas;
DROP POLICY IF EXISTS "Leitura pública de partidas" ON public.partidas;

REVOKE ALL ON TABLE public.perguntas, public.partidas, public.jogos FROM PUBLIC, anon, authenticated;
REVOKE ALL ON TABLE public.ranking FROM PUBLIC, anon, authenticated;
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT SELECT ON public.jogos, public.ranking TO anon, authenticated;
-- A view deliberadamente expõe só campos do ranking, usando o proprietário.
ALTER VIEW public.ranking SET (security_invoker = false);
-- Credencial privada usada somente na execução controlada do Python/Colab.
GRANT SELECT ON public.perguntas TO service_role;
GRANT SELECT, INSERT ON public.jogos, public.partidas TO service_role;
GRANT USAGE, SELECT ON SEQUENCE public.jogos_id_seq TO service_role;

NOTIFY pgrst, 'reload schema';
COMMIT;
