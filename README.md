# TopWeb — Status & Incidentes do Guardião

Página de status pública da TopWeb, movida a [Upptime](https://upptime.js.org) — roda **100% no GitHub**
(Actions + Pages), sem servidor. Mede a disponibilidade dos serviços TopWeb **de fora da rede** a cada 5 min
(a "visão do mundo" que um monitor interno não enxerga) e guarda o histórico versionado no próprio git.

> ⚙️ **Ainda não está no ar?** Siga o [`SETUP.md`](./SETUP.md) — 3 passos seus (push + token + Pages).

## O que tem aqui
- **Status ao vivo + uptime % + tempo de resposta** de cada serviço — o Upptime preenche esta seção do README
  automaticamente após o primeiro build.
- [`incidentes/`](./incidentes) — relatórios versionados de cada DDoS mitigado pelo **Guardião anti-DDoS**
  (o registro auditável, além do WhatsApp). Formato e convenção em [`incidentes/README.md`](./incidentes/README.md).
- [`tools/publicar-incidente.py`](./tools/publicar-incidente.py) — gera os relatórios a partir da trilha do daemon.

## Camadas de observabilidade da TopWeb (contexto)
| Camada | Onde | Público |
|---|---|---|
| Operacional, tempo real | monitoramento interno | NOC / engenharia |
| Alerta imediato | WhatsApp (NOC) | plantão |
| **Status público + histórico** | **este repo (Upptime + incidentes)** | gestor / cliente / auditoria |

Parte do roadmap **Guardião v2** — Fase 1 (observabilidade).
