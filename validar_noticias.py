#!/usr/bin/env python3
"""Valida noticias.json antes de publicar. Uso: python3 validar_noticias.py [noticias.json]
Sai com código 1 se algo estiver errado (e então NADA deve ser publicado)."""
import json, re, sys, datetime as dt
CATS={'ciencia','saude','ambiente','cultura','paz','democracia','alimentar','pobreza','biodiversidade','infra'}
MAX_IDADE_DIAS=30
def main(path='noticias.json'):
    erros=[]
    try: d=json.load(open(path,encoding='utf-8'))
    except Exception as e: print('ERRO: JSON inválido:',e); return 1
    try: ed=dt.date.fromisoformat(d['edicao'])
    except Exception: print('ERRO: campo "edicao" ausente ou fora do formato AAAA-MM-DD'); return 1
    hoje=dt.date.today()
    if abs((hoje-ed).days)>1: erros.append(f'edição {ed} não é de hoje ({hoje})')
    itens=([('destaque',d.get('destaque'))] if d.get('destaque') else [])+[(f'noticia {i+1}',n) for i,n in enumerate(d.get('noticias',[]))]
    if not d.get('destaque'): erros.append('falta o destaque')
    if len(itens)<5: erros.append(f'só {len(itens)} notícias (mínimo 5)')
    urls=set(); titulos=set()
    for nome,n in itens:
        for c in ('region','cat','title','dek','src','url','date'):
            if not str(n.get(c,'')).strip(): erros.append(f'{nome}: campo "{c}" vazio')
        if n.get('region') not in ('br','mundo'): erros.append(f'{nome}: region inválida')
        if n.get('cat') not in CATS: erros.append(f'{nome}: categoria inválida "{n.get("cat")}"')
        if not re.match(r'^https://[^ ]+\.[^ ]+',n.get('url','')): erros.append(f'{nome}: url precisa começar com https://')
        if n.get('url') in urls: erros.append(f'{nome}: url repetida')
        if n.get('title') in titulos: erros.append(f'{nome}: título repetido')
        urls.add(n.get('url')); titulos.add(n.get('title'))
        try:
            dd=dt.date.fromisoformat(n['date'])
            if dd>hoje: erros.append(f'{nome}: data no futuro ({dd})')
            elif (hoje-dd).days>MAX_IDADE_DIAS: erros.append(f'{nome}: notícia com {(hoje-dd).days} dias (máx {MAX_IDADE_DIAS})')
        except Exception: erros.append(f'{nome}: data fora do formato AAAA-MM-DD')
        if len(n.get('title',''))>140 or len(n.get('dek',''))>420: erros.append(f'{nome}: texto longo demais')
    if erros:
        print('REPROVADO:'); [print(' -',e) for e in erros]; return 1
    print(f'APROVADO: {len(itens)} notícias, edição {ed}.'); return 0
if __name__=='__main__': sys.exit(main(*sys.argv[1:]))
