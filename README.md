# DIMAS Tag

App de tagueamento de treinos e jogos de futebol: botões de tag por grupo (Comportamentos-chave, Conceitos e Ação), atletas por função, campograma 0–100 no jogo, blocos/períodos com relógio e exportação em XML (formato de instâncias Sportscode/Hudl).

É um app de arquivo único (`src/dimas-tag.html`). A pasta `public/` contém a versão **instalável e offline** (PWA), gerada por `build.py`.

## Rodar no PC (offline)

1. Abra a versão hospedada (Firebase) no Chrome ou Edge **uma vez com internet**.
2. Clique no ícone **Instalar** na barra de endereço (ou menu ⋮ → *Instalar DIMAS Tag*).
3. O app abre em janela própria e funciona **sem internet** a partir daí. As análises, o elenco e os protocolos ficam salvos no próprio navegador do PC.

Sem Firebase, dá para rodar localmente também:

```bash
cd public
python3 -m http.server 8080
# abra http://localhost:8080 e instale do mesmo jeito
```

> Abrir o `index.html` direto do disco (duplo clique) funciona para usar, mas o navegador não instala nem guarda o app offline por `file://`. Use um servidor local ou o Firebase.

## Publicar no GitHub Pages (sem instalar nada)

O workflow `.github/workflows/pages.yml` publica `public/` no GitHub Pages a cada push em `main`. Na primeira vez, se ele falhar por o Pages estar desligado: *Settings* → *Pages* → *Source*: **GitHub Actions**, e rode o workflow de novo em *Actions*. O app fica em `https://rennato158.github.io/Dimas-Tag/`; abra no Chrome e clique em **Instalar**.

## Publicar no Firebase Hosting

Uma vez, no seu PC:

```bash
npm install -g firebase-tools
firebase login
firebase use --add        # escolha o projeto do seu console Firebase
```

Cada publicação:

```bash
python3 build.py          # regenera public/index.html e public/sw.js
firebase deploy --only hosting
```

O `firebase.json` já aponta para `public/` e evita cache do `index.html` e do `sw.js`, então cada deploy chega aos aparelhos já instalados na próxima abertura.

### Deploy pelo GitHub (opcional)

O workflow `.github/workflows/firebase-deploy.yml` roda manualmente (aba *Actions* → *Deploy Firebase Hosting* → *Run workflow*). Para usá-lo:

1. No console Firebase: *Configurações do projeto* → *Contas de serviço* → *Gerar nova chave privada* (JSON).
2. No GitHub: *Settings* → *Secrets and variables* → *Actions* → novo secret `FIREBASE_SERVICE_ACCOUNT` com o conteúdo do JSON, e outro `FIREBASE_PROJECT_ID` com o id do projeto.

## Atualizar o app

Edite `src/dimas-tag.html`, rode `python3 build.py` e publique. O service worker troca de versão a cada build, então os PCs instalados pegam a nova versão sozinhos.

## Estrutura

```
src/dimas-tag.html        fonte do app (arquivo único)
build.py                  gera public/index.html + public/sw.js
sw.template.js            modelo do service worker
public/                   site pronto para hospedar
  index.html
  manifest.webmanifest
  sw.js
  icons/
  vendor/                 JSZip e SheetJS locais (sem CDN)
firebase.json             configuração do Hosting
```
