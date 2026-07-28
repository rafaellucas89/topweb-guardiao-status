#!/usr/bin/env bash
# ligar-pagina.sh — liga a página de status TopWeb num passo só.
# Uso:   bash ~/topweb-guardiao-status/ligar-pagina.sh
#        (opcional: passe um PAT dedicado como argumento -> bash ligar-pagina.sh ghp_xxx)
# Faz: grava o secret GH_PAT -> dispara os workflows -> espera a gh-pages -> liga o Pages -> mostra o link.
set -uo pipefail
R="rafaellucas89/topweb-guardiao-status"
TOKEN="${1:-$(gh auth token)}"

echo "==> 1/4 gravando secret GH_PAT no repo..."
printf '%s' "$TOKEN" | gh secret set GH_PAT --repo "$R" && echo "   ✅ secret gravado" \
  || { echo "   ❌ falhou ao gravar o secret — abortando"; exit 1; }

echo "==> 2/4 disparando workflows (setup, uptime, site)..."
gh workflow run setup.yml  --repo "$R" 2>/dev/null && echo "   ✅ Setup CI"
sleep 5
gh workflow run uptime.yml --repo "$R" 2>/dev/null && echo "   ✅ Uptime CI"
gh workflow run site.yml   --repo "$R" 2>/dev/null && echo "   ✅ Static Site CI"

echo "==> 3/4 aguardando a branch gh-pages nascer (1 a 3 min)..."
ok=0
for i in $(seq 1 40); do
  if gh api "repos/$R/branches/gh-pages" >/dev/null 2>&1; then ok=1; echo "   ✅ gh-pages criada"; break; fi
  printf '.'; sleep 15
done
[ "$ok" = 0 ] && echo "   ⚠️ gh-pages ainda não apareceu — os workflows podem estar rodando; rode de novo em uns minutos."

echo "==> 4/4 ligando o GitHub Pages..."
if printf '{"source":{"branch":"gh-pages","path":"/"}}' | gh api -X POST "repos/$R/pages" --input - >/dev/null 2>&1; then
  echo "   ✅ Pages ativado"
else
  echo "   ℹ️ Pages já estava ligado ou precisa ser ligado à mão (Settings > Pages > branch gh-pages)"
fi

echo ""
echo "🛡️  Pronto. A página sobe em ~1 min:"
echo "    https://rafaellucas89.github.io/topweb-guardiao-status"
echo "    Acompanhe os workflows: https://github.com/$R/actions"
