import csv
from collections import defaultdict, Counter
from pathlib import Path

AMAZONIA_UFS = {"AC","AM","AP","MA","MT","PA","RO","RR","TO"}
EXPECTED_YEARS = set(str(y) for y in range(2012, 2022))

files = {
    'desmatamento': Path('limpos/desmatamento/desmatamento_2012-2021.csv'),
    'idh': Path('limpos/idh/ipeadata_idh_2012-2021.csv'),
    'populacao': Path('limpos/populacao/populacao_estadual_2012-2021.csv')
}

issues = defaultdict(list)

for name, path in files.items():
    print(f"\n== Validando: {name} -> {path}")
    if not path.exists():
        print(f"  ERRO: arquivo não encontrado: {path}")
        issues[name].append('missing_file')
        continue
    with path.open(encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))
    rows = len(reader)
    print(f"  Linhas: {rows}")

    # normalize column names
    cols = reader[0].keys() if reader else []
    colmap = {c: c for c in cols}
    if name == 'idh' and 'Sigla' in cols:
        colmap['Sigla'] = 'UF'
    # build sets
    yrs = set()
    ufs = set()
    missing_counts = Counter()
    dup_counter = Counter()

    for r in reader:
        # get normalized UF
        uf = r.get('UF') or r.get('Sigla') or ''
        uf = (uf or '').strip().upper()
        yr = (r.get('ano') or '').strip()
        yrs.add(yr)
        if uf:
            ufs.add(uf)
        for k in ['UF','ano']:
            if (r.get(k) or r.get(k.lower()) or '') == '':
                missing_counts[k]+=1
        # count duplicates
        dup_counter[(uf, yr)] += 1
        # specific checks
        if name == 'desmatamento':
            try:
                area = float(r.get('area_km') or 'nan')
                if area < 0:
                    issues[name].append(f'negative_area {uf} {yr}')
            except:
                issues[name].append(f'bad_area_value {uf} {yr}')
        if name == 'idh':
            try:
                val = float(r.get('IDH') or 'nan')
                if not (0 <= val <= 1):
                    issues[name].append(f'idh_out_of_range {uf} {yr} {val}')
            except:
                issues[name].append(f'idh_not_numeric {uf} {yr}')
        if name == 'populacao':
            try:
                pv = int(float(r.get('populacao') or 'nan'))
                if pv < 0:
                    issues[name].append(f'pop_negative {uf} {yr}')
            except:
                issues[name].append(f'pop_not_int {uf} {yr}')

    unexpected_ufs = sorted([u for u in ufs if u and u not in AMAZONIA_UFS])
    missing_years = sorted(list(EXPECTED_YEARS - yrs))
    extra_years = sorted(list(yrs - EXPECTED_YEARS))
    dup_pairs = [k for k,v in dup_counter.items() if v>1]

    print(f"  UFs encontradas ({len(ufs)}): {sorted(ufs)}")
    if unexpected_ufs:
        print(f"  AVISO: UFs fora da Amazônia Legal: {unexpected_ufs}")
        issues[name].append('unexpected_ufs')
    print(f"  Anos encontrados ({len(yrs)}): {sorted(yrs)}")
    if missing_years:
        print(f"  AVISO: anos esperados ausentes: {missing_years}")
        issues[name].append('missing_years')
    if extra_years:
        print(f"  AVISO: anos extras não esperados: {extra_years}")
        issues[name].append('extra_years')
    if missing_counts:
        print(f"  Valores ausentes por coluna: {dict(missing_counts)}")
    if dup_pairs:
        print(f"  AVISO: pares (UF,ano) duplicados: {dup_pairs}")
        issues[name].append('duplicates')

print('\n== Resumo geral de issues detectadas')
any_issues = False
for name in files:
    if issues[name]:
        any_issues = True
        print(f"- {name}: {issues[name]}")
    else:
        print(f"- {name}: OK")

if any_issues:
    print('\nAlgumas questões foram detectadas (ver acima). Recomendo revisar os avisos e corrigir onde necessário.')
else:
    print('\nTodos os arquivos parecem coerentes.')


