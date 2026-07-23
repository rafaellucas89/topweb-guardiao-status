#!/usr/bin/env python3
# publicar-incidente.py — gera o RESUMO PÚBLICO sanitizado de cada ataque mitigado pelo Guardião.
# --------------------------------------------------------------------------------------------
# Lê a trilha privada do daemon (guardiao-eventos.jsonl, que TEM prefixo/community/reação) e escreve
# aqui APENAS campos não-sensíveis: início, duração, tipo, faixa de pico, "serviço estável".
#   incidentes/AAAA/MM/<ts>.json + .md   (1 arquivo por incidente material).
# NUNCA publica: prefixo/IP exato, community BGP, upstream, tática, tempo de reação preciso.
# Uso:  python3 tools/publicar-incidente.py [caminho-do-eventos.jsonl]
#       (default: ~/topweb-network-ops/guardiao-eventos.jsonl — repo PRIVADO)
# --------------------------------------------------------------------------------------------
import json, os, sys, datetime

EVENTS = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/topweb-network-ops/guardiao-eventos.jsonl")
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "incidentes")


def parse(ts):
    return datetime.datetime.fromisoformat(ts)


def faixa_pico(gbps):
    """Converte o pico exato numa FAIXA (não revela o valor medido)."""
    if gbps is None:      return "não medido"
    g = float(gbps)
    if g < 5:   return "< 5 Gbps"
    if g < 10:  return "5–10 Gbps"
    if g < 20:  return "10–20 Gbps"
    if g < 40:  return "20–40 Gbps"
    return "> 40 Gbps"


def build():
    if not os.path.exists(EVENTS):
        print(f"sem eventos em {EVENTS}"); return
    evs = []
    with open(EVENTS) as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                try: evs.append(json.loads(ln))
                except Exception: pass

    abertos = {}   # prefixo(interno, só p/ parear) -> evento de mitigacao
    incidentes = []
    for e in evs:
        tipo, pfx = e.get("tipo"), e.get("prefixo")
        if tipo == "mitigacao" and pfx:
            abertos[pfx] = e
        elif tipo == "reversao" and pfx and pfx in abertos:
            incidentes.append((abertos.pop(pfx), e))
    for pfx, m in abertos.items():
        incidentes.append((m, None))

    n = 0
    for m, r in incidentes:
        t_mit = parse(m["ts"])
        t_rev = parse(r["ts"]) if r else None
        iid = t_mit.strftime("%Y-%m-%dT%H%M%S")
        dur_min = round((t_rev - t_mit).total_seconds() / 60) if t_rev else None
        doc = {   # <-- SÓ campos públicos; nada de prefixo/community/upstream/reação
            "id": iid,
            "inicio": m["ts"],
            "duracao_min": dur_min,
            "tipo": "volumétrico",
            "pico_faixa": faixa_pico(m.get("gbps")),
            "mitigado": True,
            "resultado": ("serviço estável, sem impacto perceptível" if r else "mitigação em andamento"),
        }
        outdir = os.path.join(ROOT, t_mit.strftime("%Y"), t_mit.strftime("%m"))
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, iid + ".json"), "w") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        with open(os.path.join(outdir, iid + ".md"), "w") as f:
            f.write(render_md(doc))
        n += 1
        print(f"escrito (sanitizado): {t_mit.strftime('%Y/%m')}/{iid}")
    print(f"{n} incidente(s) público(s) gerado(s).")


def render_md(d):
    dur = f"~{d['duracao_min']} min" if d["duracao_min"] is not None else "— (em andamento)"
    return f"""# Incidente {d['id']}

| Campo | Valor |
|---|---|
| Início | {d['inicio']} |
| Tipo | Ataque {d['tipo']} |
| Pico aproximado | {d['pico_faixa']} |
| Duração da mitigação | {dur} |
| Mitigado automaticamente | {'sim' if d['mitigado'] else 'não'} |
| Resultado | {d['resultado']} |

A rede da TopWeb detectou um ataque {d['tipo']} e a mitigação automática atuou, mantendo os serviços
estáveis. Detalhes técnicos da resposta são tratados internamente pela equipe de rede.

*Resumo público gerado automaticamente. O detalhe operacional é confidencial.*
"""


if __name__ == "__main__":
    build()
