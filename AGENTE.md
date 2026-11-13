# Instruções para a rotina diária do Vagalume Daily

Objetivo: toda manhã, atualizar `noticias.json` com a edição do dia (boas notícias do Brasil e do mundo) e publicar. O Cloudflare Pages publica sozinho a cada commit na branch `main`.

## Regras de ouro (nunca quebrar)
1. **Nada de notícia não verificada.** Para cada item, abra a página da fonte (WebFetch) e confirme o fato, os números e a data de publicação. Use a página original (agência, órgão oficial, jornal, revista científica), não um resumo de terceiros, quando possível.
2. **Só notícias recentes**: de preferência dos últimos 7 dias; máximo 30 dias (o validador reprova mais que isso).
3. **Positivas e coletivas**: progresso que beneficia muitas pessoas, ambiente, ciência, saúde, cooperação. Evite política partidária, mercado financeiro puro, celebridades e qualquer coisa sensacionalista. Se uma notícia tem ressalva importante, escreva a ressalva no resumo.
4. **Não invente nada.** Se não conseguir verificar, não inclua.
5. **Mínimo de 5 notícias verificadas** (1 destaque + 4 outras). Meta: 8 a 10, com mistura de Brasil e Mundo e de frentes diferentes.
6. Se não alcançar o mínimo, **não publique**: mantenha o arquivo anterior e avise o dono (JY) com o motivo.

## Formato de `noticias.json`
```
{ "edicao": "AAAA-MM-DD", "atualizado_em": "ISO com fuso -03:00",
  "destaque": {region, cat, title, dek, src, url, date},
  "noticias": [ {region, cat, title, dek, src, url, date}, ... ] }
```
- `region`: `br` ou `mundo`. `date`: data de publicação da fonte, `AAAA-MM-DD`. `url`: começa com `https://`.
- `cat` (use exatamente): ciencia, saude, ambiente, cultura, paz, democracia, alimentar, pobreza, biodiversidade, infra.
- `title` até 140 caracteres; `dek` (resumo) até 420, em português claro, com os números principais.
- `src`: nome do veículo/órgão. Se a fonte é republicação, cite "X (via Y)".
- O destaque é a notícia mais forte e mais bem verificada do dia.

## Passo a passo
1. Buscar candidatas (WebSearch; boas notícias Brasil + mundo; agências oficiais; Agência Brasil/Gov, OMS, Inpe, revistas científicas).
2. Verificar cada uma abrindo a fonte. Descartar o que não confirmar.
3. Escrever `noticias.json` (substitui o anterior).
4. Rodar `python3 validar_noticias.py`. Só continuar se imprimir APROVADO.
5. Atualizar `lastmod` em `sitemap.xml` para a data da edição.
6. Commit na `main` com a mensagem `Edição AAAA-MM-DD` e push.
7. Avisar o dono com um resumo curto: quantas notícias, qual o destaque, e qualquer dúvida de verificação.
