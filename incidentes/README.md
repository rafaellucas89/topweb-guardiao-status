# Incidentes do Guardião anti-DDoS (visão pública)

Cada ataque volumétrico mitigado pelo Guardião vira um **registro público resumido** aqui — transparência de
qualidade de serviço, versionada no git (append-only, com timestamp por commit).

> 🔒 **Esta é a visão pública, sanitizada de propósito.** Ela mostra *que* houve um ataque e que o serviço
> ficou estável — **não** o mecanismo de defesa. O detalhe operacional (prefixo exato, community BGP, upstream,
> tática de mitigação, tempo de reação preciso) é **confidencial** e fica só no repositório privado de rede.
> Publicar o playbook entregaria a um atacante o mapa de como contornar a defesa.

## Convenção
Um arquivo por incidente material (uma janela de ataque), **não** por ciclo:
```
incidentes/AAAA/MM/<timestamp>.json   # resumo canônico (máquina)
incidentes/AAAA/MM/<timestamp>.md     # resumo legível (cliente/gestor)
```

## Schema público do `.json` (só campos não-sensíveis)
| campo | significado |
|---|---|
| `id` | identificador do incidente (timestamp) |
| `inicio` | início aproximado do ataque (ISO-8601 UTC) |
| `duracao_min` | duração aproximada da mitigação, em minutos |
| `tipo` | classe do ataque (ex.: "volumétrico") |
| `pico_faixa` | faixa aproximada do pico (ex.: "10–20 Gbps") — não o valor exato |
| `mitigado` | bool — se a defesa atuou |
| `resultado` | frase de status (ex.: "serviço estável, sem impacto perceptível") |

Campos **deliberadamente ausentes** do público: prefixo/IP exato, community BGP, nome do upstream, tática,
tempo de reação preciso. Tudo isso vive na trilha privada `guardiao-eventos.jsonl` (repo de rede).

## Como é gerado
`tools/publicar-incidente.py` lê a trilha do daemon e emite **apenas o resumo sanitizado** acima.
Publicação (commit+push nesta vitrine) via deploy key de escopo mínimo — passo à parte no `SETUP.md`.

> Regra de ouro: 1 arquivo por incidente, nunca por pacote/ciclo — e nada que ajude um atacante.
