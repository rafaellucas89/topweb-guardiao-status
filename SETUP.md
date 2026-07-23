# Como subir a página de status TopWeb (Upptime)

> Esta pasta é um repositório Git pronto pra push. O Upptime roda **100% no GitHub** (Actions + Pages),
> não precisa de servidor. Passos que são **seus** (push + secret + Pages) — o auto-mode me impede de fazer.

## Antes de tudo — confira 1 coisa
No `.upptimerc.yml`, o `owner:` está como **`rafaellucas89`**. Se seu usuário/org do GitHub for outro, troque lá
(e nas URLs do `navbar`/`assignees`).

## Caminho A — recomendado (workflows sempre atuais)
1. No GitHub, abra **https://github.com/upptime/upptime** → botão **“Use this template”** → crie o repo
   **`topweb-guardiao-status`** (público, pra ter Pages de graça).
2. Substitua o `.upptimerc.yml` do repo novo pelo desta pasta (é o único arquivo TopWeb-específico).
3. Copie a pasta `incidentes/` (convenção dos relatórios do Guardião) pra dentro do repo.
4. Vá para o **Passo comum** abaixo.

## Caminho B — push direto desta pasta
Esta pasta já tem os workflows (`.github/workflows/*.yml`, fixados em `@master`). Se preferir não usar o template:
```bash
cd ~/topweb-guardiao-status
git remote add origin git@github.com:rafaellucas89/topweb-guardiao-status.git
git push -u origin master
```
> Nota: o Caminho A garante os workflows na versão exata que o Upptime espera; o B usa `@master` (sempre resolve,
> mas menos previsível). Para produção séria, o A é mais robusto.

## Passo comum — o que liga o Upptime (obrigatório)
1. **Token (GH_PAT):** crie um *Personal Access Token classic* em GitHub → Settings → Developer settings →
   Tokens (classic), com escopos **`repo`** e **`workflow`**. No repo do status, em
   **Settings → Secrets and variables → Actions → New repository secret**, nome **`GH_PAT`**, valor = o token.
   (O Upptime usa esse token pra commitar os resultados e abrir Issues de incidente.)
2. **Pages:** Settings → Pages → Source = **Deploy from a branch** → branch **`gh-pages`** (o Upptime cria essa
   branch no primeiro build) → `/ (root)`.
3. **Rodar agora:** aba **Actions** → workflow **“Setup CI”** → *Run workflow*. Depois rode **“Uptime CI”**.
   Em ~5 min a primeira medição aparece; a página fica em
   `https://rafaellucas89.github.io/topweb-guardiao-status`.

## Depois (opcional, deixa mais completo)
- **CNAME próprio** (ex.: `status.topwebtelecom.net.br`): adicione `status-website: { cname: status.topwebtelecom.net.br }`
  no `.upptimerc.yml` + registro CNAME no DNS apontando pro `github.io`.
- **Incidentes do Guardião**: ver `incidentes/README.md` — o daemon publica cada mitigação de DDoS como um
  relatório versionado nesta mesma vitrine (precisa de uma deploy key com escopo mínimo; passo à parte).

## O que a página mostra
- **Status ao vivo + histórico** de cada serviço público da TopWeb, medido a cada 5 min de fora da rede
  (a “visão do mundo” que um monitor interno não pega).
- **Tempo de resposta** (gráficos) e **uptime %** por serviço, com histórico versionado no próprio git.
- **Incidentes** — quando um serviço cai, o Upptime abre uma Issue automaticamente; quando o Guardião mitiga um
  DDoS, publica um relatório em `/incidentes`.
