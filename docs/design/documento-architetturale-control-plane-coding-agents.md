
# Documento architetturale — Setup portabile e DAG-ready per coding agents
## Control plane condiviso, governance locale per repo, piano machine-readable e viste generate

**Versione:** 1.0  
**Stato:** proposta architetturale consolidata  
**Lingua:** italiano  
**Audience:** umano owner/orchestrator, coding agents, reviewer tecnici  
**Scopo:** definire un modello generale, portabile e incrementale per usare coding agents su più repository con:
- workflow condiviso e versionato;
- vincoli software locali per singolo repo;
- piano esecutivo machine-readable;
- capacità futura di esecuzione DAG-oriented e multi-agent;
- crescita graduale dell’automazione Git/GitHub senza introdurre subito un sistema troppo pesante.

---

## Indice

1. [Executive summary](#1-executive-summary)
2. [Contesto, problema e obiettivi](#2-contesto-problema-e-obiettivi)
3. [Fonti autorevoli e razionale delle scelte](#3-fonti-autorevoli-e-razionale-delle-scelte)
4. [Decisioni architetturali già prese](#4-decisioni-architetturali-già-prese)
5. [Architettura generale a 3 livelli](#5-architettura-generale-a-3-livelli)
6. [Authority model e canonical source rule](#6-authority-model-e-canonical-source-rule)
7. [Distribuzione delle responsabilità tra file e directory](#7-distribuzione-delle-responsabilità-tra-file-e-directory)
8. [Perché `PLAN.yaml` come source of truth](#8-perché-planyaml-come-source-of-truth)
9. [Perché `PLAN.md` e `PLAN.dot` come viste generate](#9-perché-planmd-e-plandot-come-viste-generate)
10. [Tassonomia condivisa: item, azioni, stati, ruoli ed effort](#10-tassonomia-condivisa-item-azioni-stati-ruoli-ed-effort)
11. [Modello di esecuzione DAG-ready](#11-modello-di-esecuzione-dag-ready)
12. [Commit groups, blocchi di sviluppo e chiusura](#12-commit-groups-blocchi-di-sviluppo-e-chiusura)
13. [Subagent e portabilità cross-tool](#13-subagent-e-portabilità-cross-tool)
14. [Automazione Git/GitHub in fasi](#14-automazione-gitgithub-in-fasi)
15. [Struttura concreta dei 3 livelli](#15-struttura-concreta-dei-3-livelli)
16. [Cosa va nei vari livelli: file, autorità e non-goal](#16-cosa-va-nei-vari-livelli-file-autorità-e-non-goal)
17. [Primo MVP repo-agnostic da setuppare](#17-primo-mvp-repo-agnostic-da-setuppare)
18. [Istruzioni da dare all’agent per realizzare il setup](#18-istruzioni-da-dare-allagent-per-realizzare-il-setup)
19. [Roadmap di crescita: cosa fare prima e cosa differire](#19-roadmap-di-crescita-cosa-fare-prima-e-cosa-differire)
20. [Mappatura dell’approccio al caso DUCT e ad altri repo esistenti](#20-mappatura-dellapproccio-al-caso-duct-e-ad-altri-repo-esistenti)
21. [Sintesi finale](#21-sintesi-finale)
22. [Pacchetto di handoff per continuare la conversazione altrove](#22-pacchetto-di-handoff-per-continuare-la-conversazione-altrove)
23. [Riferimenti](#23-riferimenti)

---

## 1. Executive summary

La proposta architetturale consolidata è la seguente:

- **Livello 0 — central control plane repository**  
  Un repository dedicato, versionato e portabile tra macchine, che contiene il modello condiviso:
  workflow cross-repo, tassonomia, template, prompt, script di sync/render/validation, e — in fasi successive — skill e tooling di supporto.

- **Livello 1 — workspace runtime layer**  
  Una root di workspace che contiene i repository reali e i file condivisi che gli agenti devono leggere davvero a runtime (`AGENTS.md`, `CLAUDE.md` o equivalenti). Questo livello non è il source of truth del control plane: è la sua materializzazione runtime.

- **Livello 2 — repo-local layer**  
  Ogni singolo repository ha i propri file locali sottili: vincoli software, mappa del repo, piano locale, eventuali ADR e documentazione architetturale locale.

Le scelte centrali già fissate sono:

1. **Nessun `PLAN` globale condiviso tra repo.**  
   Il piano del lavoro è sempre locale al repository/subproject.

2. **Sì a una tassonomia condivisa.**  
   Ciò che si condivide è il vocabolario operativo: item types, action taxonomy, lifecycle, ruoli, effort, e regole di dipendenza.

3. **La source of truth del piano è machine-readable.**  
   Il formato consigliato è `PLAN.yaml`.  
   `PLAN.md` e `PLAN.dot` sono viste generate.

4. **Il piano è scritto da un orchestrator/planner agent, non dall’umano a mano.**  
   L’umano definisce missione, vincoli, scelte e limiti; l’agente traduce in `PLAN.yaml`.

5. **La sequenzialità resta umana, non più runtime-globale.**  
   L’umano continuerà a pensare in milestone/sprint/item.  
   L’agente potrà eseguire gli item secondo dipendenze esplicite e blocchi compatibili.

6. **Il modello dei subagent deve essere neutro e portabile.**  
   I concetti condivisi sono ruolo, effort, trigger e profilo strumenti; la mappatura su Codex, Claude, Copilot e altri tool si fa a valle.

7. **L’automazione Git/GitHub va introdotta in fasi.**  
   Prima naming branch, commit groups, update piano e viste.  
   Solo dopo push, draft PR, merge con `develop`, e ancora dopo eventuale auto-merge finale.

Questa architettura è la migliore, ad oggi, non perché esista come standard unico pubblicato da un singolo vendor, ma perché allinea in modo pulito i pattern documentati da:
- OpenAI / Codex (`AGENTS.md` gerarchici, task paralleli, worktree isolati);
- Anthropic / Claude Code (memorie gerarchiche, subagent separati, import modulari);
- GitHub Copilot (istruzioni repository-wide, path-specifiche e precedence del file più vicino);
- Kilo (custom modes / specializzazione per workflow).

---

## 2. Contesto, problema e obiettivi

### 2.1 Problema di partenza

L’uso efficace dei coding agents su più repository tende a degenerare in uno di questi due estremi:

1. **Tutto locale a ogni repo**  
   Ogni repository ha il proprio `AGENTS.md`, il proprio piano, le proprie regole, i propri template.  
   Risultato: duplicazione, drift, manutenzione costosa, portabilità bassa.

2. **Tutto centralizzato in un singolo documento mostruoso**  
   Un unico file prova a governare workflow, architettura software, piano del lavoro, rationale e istruzioni tool-specifiche.  
   Risultato: authority mixing, contesto gonfio, conflitti, rigidità, scarsa leggibilità.

La proposta qui formalizzata evita entrambi gli estremi:
- centralizza il **modello comune**;
- lascia locale il **contenuto specifico del repo**;
- separa workflow, architettura, tracking ed eventuale rationale.

### 2.2 Obiettivi

Gli obiettivi del modello sono:

- **portabilità** tra repository;
- **portabilità** tra coding agents e orchestratori;
- **contesto stabile e riusabile**;
- **riduzione dell’entropia documentale**;
- **separazione rigorosa delle authority**;
- **preparazione a un futuro DAG-oriented**;
- **adozione incrementale**: niente big-bang.

### 2.3 Non-obiettivi

Non sono obiettivi immediati:

- costruire subito un vero DAG runtime engine;
- introdurre subito un sistema di merge/push/PR completamente automatico;
- definire subito plugin o skill custom per ogni tool;
- convertire ogni repo esistente al modello completo in una sola iterazione;
- imporre un unico layout software a tutti i repository.

---

## 3. Fonti autorevoli e razionale delle scelte

Le decisioni qui formalizzate sono sostenute dalle seguenti evidenze/documentazioni:

### 3.1 OpenAI / Codex
OpenAI documenta che:
- Codex può lavorare su **molti task in parallelo**;
- ogni task gira in un **ambiente isolato**;
- `AGENTS.md` guida Codex su come navigare il codebase, quali comandi usare e quali pratiche seguire;
- il file può vivere anche fuori dal repo e la semantica è **gerarchica per directory scope**.

**Implicazione architetturale:** il livello workspace con `AGENTS.md` condiviso ha senso runtime; il livello repo locale ha senso per override e constraints locali.

### 3.2 Anthropic / Claude Code
Anthropic documenta che:
- `CLAUDE.md` è memoria/istruzione in Markdown;
- i file possono essere caricati gerarchicamente;
- `@import` permette modularità;
- i subagent hanno contesto separato, propri tool, e sono definiti da Markdown + YAML frontmatter (`name`, `description`, `tools`);
- i subagent aiutano a preservare il contesto principale.

**Implicazione architetturale:** il modello di ruolo/effort neutro è utile; il layer condiviso può essere importato in modo modulare; il planner/orchestrator come single-writer del piano è una buona scelta.

### 3.3 GitHub Copilot
GitHub documenta che:
- esistono istruzioni repository-wide e path-specific;
- `AGENTS.md`, `CLAUDE.md` o `GEMINI.md` possono essere usati come agent instructions;
- i file più vicini al contesto specifico hanno più priorità;
- istruzioni sovrapposte o confliggenti possono creare comportamento non deterministico.

**Implicazione architetturale:** la canonical source rule è indispensabile; un file per concern è migliore di molti file ridondanti.

### 3.4 OpenAI Structured Outputs e Prompt Caching
OpenAI documenta che:
- Structured Outputs aderisce a uno schema ed è più affidabile di output JSON “libero”;
- l’ordine delle chiavi segue lo schema;
- il Prompt Caching richiede **exact prefix matches** e premia contenuti stabili e ripetuti.

**Implicazione architetturale:** `PLAN.yaml` come source of truth è una scelta forte; file condivisi stabili e poco variabili sono desiderabili.

### 3.5 GitHub branch protection, auto-merge e merge queue
GitHub documenta che:
- protected branches possono impedire deletion, force-push, merge non autorizzati;
- auto-merge esiste ma richiede checks/review appropriate;
- la merge standard su PR produce merge commit coerenti con la preferenza per preservare la storia separata;
- merge queue non è un prerequisito realistico per ogni setup base.

**Implicazione architetturale:** l’automazione Git/GitHub deve essere introdotta per fasi, non tutta subito.

---

## 4. Decisioni architetturali già prese

Questa sezione raccoglie le decisioni già emerse e considerate consolidate.

### 4.1 Decisioni consolidate

1. **Tre livelli distinti**
   - livello 0 = control plane condiviso e versionato;
   - livello 1 = materializzazione runtime condivisa nella workspace root;
   - livello 2 = repository locali.

2. **No `PLAN` globale**
   - il piano è sempre locale al repo/subproject.

3. **Tassonomia comune sì**
   - item types, action taxonomy, lifecycle, ruoli, effort e semantica delle dipendenze sono condivisi.

4. **`PLAN.yaml` come source of truth**
   - `PLAN.md` e `PLAN.dot` sono viste generate.
   - `PLAN.svg` o simili sono render grafici opzionali.

5. **Lo YAML non viene scritto a mano dall’umano**
   - l’umano fornisce intenzioni, vincoli e decisioni;
   - un planner/orchestrator agent aggiorna `PLAN.yaml`.

6. **Single-writer rule**
   - un solo agente owner del piano può scrivere la source of truth del piano;
   - gli altri agenti possono proporre modifiche o produrre evidenze, ma non scrivono direttamente il piano canonico.

7. **La sequenzialità non è più una regola runtime globale**
   - la sequenzialità resta semantica umana di milestone/sprint/item;
   - l’esecuzione è dependency-driven.

8. **Commit su blocchi verificati**
   - non più necessariamente “un item = un commit”;
   - il boundary naturale diventa il `commit_group` verificato.

9. **Portabilità cross-agent come requisito**
   - il modello shared deve essere neutro;
   - gli adapter verso i vari agenti vengono dopo.

10. **Git automation per fasi**
    - prima branch e commit groups;
    - poi push e draft PR;
    - solo più avanti merge/auto-merge.

### 4.2 Decisioni ancora differite

Queste non sono scartate, ma rinviate:

- auto-push;
- apertura PR automatica non-draft;
- auto-merge finale;
- cleanup automatico branch feature;
- merge queue;
- subagent reali per ogni tool;
- DAG runtime completo;
- skill custom per ogni agente;
- orchestrazione fully autonomous end-to-end.

---

## 5. Architettura generale a 3 livelli

## 5.1 Livello 0 — Central Control Plane Repository

### Definizione
È un repository dedicato che contiene il modello condiviso e versionato del sistema agentico.

### Scopi
- versionare il workflow comune;
- versionare tassonomie e schema del piano;
- ospitare template e script di bootstrap/sync/render;
- fungere da source of truth portabile tra più PC.

### Non-scopi
- non ospita i repository di prodotto;
- non sostituisce i file locali di ciascun repo;
- non governa direttamente l’architettura software di ogni progetto.

### Contenuto tipico
- workflow condiviso;
- tassonomia item/actions/states;
- schema del `PLAN.yaml`;
- template di `AGENTS.md`, `ARCHITECTURE.md`, `REPO_MAP.md`;
- script `sync`, `render`, `validate`, `bootstrap`;
- eventuali prompt condivisi;
- eventuali skill e metadati di supporto.

---

## 5.2 Livello 1 — Workspace Runtime Layer

### Definizione
È la root del filesystem sotto cui vivono i repository reali e i file condivisi che gli agenti leggono effettivamente a runtime.

### Scopi
- dare scope gerarchico alle istruzioni comuni;
- materializzare `AGENTS.md` e altri file condivisi in posizioni rilevanti per i tool;
- evitare duplicazione del workflow in ogni repo.

### Non-scopi
- non è il posto dove si modifica a mano il modello condiviso;
- non è il posto dove si definisce il piano di ogni progetto;
- non è il posto dove si mantengono versioni divergenti delle stesse authority.

### Contenuto tipico
- `AGENTS.md` workspace-wide;
- `CLAUDE.md` workspace-wide o file equivalenti;
- repository reali sotto la root.

---

## 5.3 Livello 2 — Repo-local Layer

### Definizione
È il livello del singolo repository o subproject.

### Scopi
- definire i vincoli software locali;
- definire l’architettura del progetto;
- mantenere il piano del lavoro locale;
- tenere la mappa locale del repo;
- ospitare eventuali ADR locali.

### Non-scopi
- ridefinire il workflow globale condiviso;
- ridefinire la tassonomia condivisa;
- ridefinire la canonical source rule senza decisione esplicita.

### Contenuto tipico
- `AGENTS.md` locale (workflow/authority locale, entry point alle altre authority);
- `ARCHITECTURE.md` o `docs/architecture/*`;
- `PLAN.yaml`;
- `PLAN.md` e `PLAN.dot` generati;
- `REPO_MAP.md`;
- eventuali `docs/adr/*`.

---

## 6. Authority model e canonical source rule

### 6.1 Principio di base

**Ogni concern deve avere una sola authority canonica.**

Questa è la regola più importante del sistema.  
Se non viene rispettata, tutto il resto diventa fragile.

### 6.2 Concerns principali

| Concern | Authority canonica consigliata |
|---|---|
| Workflow operativo agentico | `AGENTS.md` |
| Vincoli software / boundaries / design | `ARCHITECTURE.md` o `docs/architecture/*` |
| Tracking esecutivo locale | `PLAN.yaml` |
| Vista testuale del piano | `PLAN.md` (generato) |
| Vista grafo del piano | `PLAN.dot` / `PLAN.svg` (generati) |
| Rationale decisionale | `docs/adr/*` |
| Mappa pratica del codebase | `REPO_MAP.md` |
| Template e policy condivise cross-repo | livello 0 (`agent-os/`) |

### 6.3 Regola di precedenza

La precedenza generale consigliata è:

1. decisioni e istruzioni esplicite dell’umano;
2. `AGENTS.md` per il workflow e la mappa delle authority;
3. `ARCHITECTURE.md` / `docs/architecture/*` per i vincoli software;
4. `PLAN.yaml` per il lavoro attivo locale;
5. codice, test, config e artefatti reali come evidenza implementativa;
6. viste generate (`PLAN.md`, `PLAN.dot`) come artefatti informativi, non autoritativi.

### 6.4 Regola di non-duplicazione

- `AGENTS.md` **può rimandare** a `ARCHITECTURE.md`, ma non deve duplicarne il contenuto dettagliato.
- `PLAN.yaml` **può riferire** decisioni architetturali, ma non deve ridiventare una costituzione tecnica.
- `PLAN.md` e `PLAN.dot` non devono contenere materiale non derivabile o non coerente con la source of truth.

---

## 7. Distribuzione delle responsabilità tra file e directory

## 7.1 `AGENTS.md`
### Ruolo
Contratto operativo e mappa delle authority.

### Deve contenere
- scopo;
- authority map;
- canonical source rule;
- regole di workflow;
- escalation / stop conditions;
- tassonomia richiamata o rimando al file condiviso;
- regole di commit/checkpoint generali;
- dove leggere `ARCHITECTURE`, `PLAN`, `REPO_MAP`, eventuali ADR.

### Non deve contenere
- tutta l’architettura tecnica dettagliata;
- il piano attivo completo;
- rationale storiche estese;
- tabelle operative lunghe del piano.

---

## 7.2 `ARCHITECTURE.md` / `docs/architecture/*`
### Ruolo
Fonte normativa dei vincoli software, delle boundaries, dei contratti e delle invarianti del progetto.

### Deve contenere
- confini di package/moduli;
- ownership di sottosistemi;
- contratti pubblici;
- invarianti semantiche;
- limiti di modifica autorizzata;
- pattern consentiti o vietati;
- interfacce e boundary rule.

### Non deve contenere
- tracker operativo del lavoro;
- checklist di commit;
- cronologia degli item.

---

## 7.3 `PLAN.yaml`
### Ruolo
Source of truth locale per tracking e orchestrazione del lavoro.

### Deve contenere
- missione/milestone attiva;
- sprint attivo;
- tassonomia usata;
- elenco item;
- stati;
- dipendenze;
- ruoli/effort;
- commit groups;
- eventuali artifact/checks/notes.

### Non deve contenere
- lunghi testi architetturali;
- workflow agentico generale;
- rationale prolisse non operative.

---

## 7.4 `PLAN.md`
### Ruolo
Vista umana leggibile.

### Deve contenere
- rendering leggibile di missione/sprint/item;
- eventuali tabelle o sezioni chiare per stati e dipendenze;
- note comprensibili da un reviewer umano.

### Non deve essere editato a mano
È una vista generata.

---

## 7.5 `PLAN.dot` / `PLAN.svg`
### Ruolo
Vista grafo.

### Deve mostrare
- nodi;
- dipendenze;
- cluster (per sprint o per commit group);
- eventuale stato e tipo come attributi visuali.

### Non deve essere editato a mano
È una vista generata.

---

## 7.6 `REPO_MAP.md`
### Ruolo
Mappa pratica del codebase.

### Deve contenere
- entry point;
- moduli principali;
- test map;
- hot paths;
- aree fragili.

### Non deve diventare
- una seconda architettura normativa;
- un secondo `AGENTS.md`.

---

## 7.7 `docs/adr/*`
### Ruolo
Rationale e decisioni irreversibili o strutturali.

### Va introdotto quando
- il progetto diventa abbastanza stabile da richiedere memoria decisionale;
- la distinzione tra “regola attuale” e “perché è stata scelta” diventa utile.

---

## 7.8 `SKILLS/`
### Ruolo
Automazione riusabile, istruzioni operative specializzate, packaging di workflow.

### Posizione consigliata
- al livello 0 nel control plane;
- eventualmente con adapter o shim locali solo dove necessario.

### Non deve diventare
- la fonte normativa dell’architettura software di un repo, salvo dichiarazione esplicita.

---

## 8. Perché `PLAN.yaml` come source of truth

## 8.1 Motivazione principale
Il piano non è solo testo: è struttura.

Hai già deciso che il piano deve poter contenere:
- item types;
- actions;
- states;
- dependencies;
- roles;
- effort;
- commit groups.

Questi concetti sono più naturali in un formato dati che in prose libera.

## 8.2 Perché non `PLAN.md` come source of truth
Il Markdown è eccellente per:
- lettura umana;
- review;
- discussione.

È meno eccellente per:
- validazione forte;
- dipendenze esplicite;
- grouping e parallelismo;
- rendering deterministico multiplo;
- single-writer orchestration.

## 8.3 Perché non `.dot` come source of truth
DOT è ottimo per rappresentare il grafo.  
Non è ottimo come unica fonte del dominio, perché il tuo piano contiene più del solo grafo:
- metadata di esecuzione;
- semantica degli item;
- ruoli/effort;
- commit groups;
- rationale operative.

Per questo la scelta corretta è:

- `PLAN.yaml` = modello dati
- `PLAN.dot` = vista grafo

---

## 9. Perché `PLAN.md` e `PLAN.dot` come viste generate

## 9.1 `PLAN.md`
Serve per:
- leggere il piano;
- fare review umana;
- discutere stato, dipendenze e blocchi;
- avere una vista orientata al testo.

## 9.2 `PLAN.dot`
Serve per:
- visualizzare il DAG;
- capire parallelismo e colli di bottiglia;
- vedere cluster per sprint o commit group;
- generare SVG/PDF/PNG.

## 9.3 Regola di determinismo
La traduzione:
- `PLAN.yaml -> PLAN.md`
- `PLAN.yaml -> PLAN.dot`

deve essere **deterministica** e fatta da tool/script, non da LLM in modo libero.

---

## 10. Tassonomia condivisa: item, azioni, stati, ruoli ed effort

## 10.1 Item types

### `X`
Milestone container.  
Non eseguibile di default.  
Serve a contenere un obiettivo macro.

### `S`
Sprint container.  
Non eseguibile di default.  
Serve a raggruppare un tranche di lavoro umano.

### `Q`
Blocking question / decision gate.  
Item eseguibile.  
Serve a fermare il flusso e richiedere una decisione esplicita.

### `D`
Documentation / planning / governance item.  
Item eseguibile.  
Serve a modificare o produrre documentazione, piano, governance, rationale operative.

### `M`
Implementation / integration / refactor item.  
Item eseguibile.  
Serve a modificare codice o integrazione.

### `F`
Fix / hotfix item.  
Item eseguibile.  
Serve a correggere un problema puntuale o un bug.

### `T`
Test / validation item.  
Item eseguibile.  
Serve a scrivere, aggiornare o eseguire test/gate.

### `C`
Checkpoint / review / closure gate item.  
Item eseguibile.  
Serve a produrre una chiusura controllata di una tranche di lavoro.

---

## 10.2 Action taxonomy

Le actions sono ortogonali all’item type.

### `audit`
Leggere, mappare, capire, caratterizzare.

### `plan`
Creare o aggiornare la struttura del lavoro.

### `design`
Definire una soluzione locale entro architettura già autorizzata.

### `implement`
Scrivere o modificare codice.

### `refactor`
Ristrutturare preservando la semantica esterna.

### `test`
Aggiungere o aggiornare test.

### `verify`
Eseguire validazioni, gate e controllare l’esito.

### `document`
Aggiornare documentazione o rationale.

### `review`
Rileggere criticamente e fare assessment qualitativo.

### `checkpoint`
Produrre una chiusura intermedia con evidenze.

### `decide`
Formalizzare una decisione umana o la risposta a un `Q`.

### `migrate`
Spostare ownership/boundary/flow senza cambiare output attesi.

---

## 10.3 Regole di coerenza type/actions

Regole consigliate:

- `Q` deve avere almeno `review` o `decide`
- `D` tende ad avere `plan`, `document`, `review`, `checkpoint`
- `M` tende ad avere `design`, `implement`, `refactor`, `migrate`, `verify`
- `F` tende ad avere `implement`, `test`, `verify`
- `T` tende ad avere `test`, `verify`
- `C` tende ad avere `review`, `checkpoint`, `verify`

Queste regole non sono un sistema di type-checking rigido, ma servono a evitare combinazioni prive di senso.

---

## 10.4 Lifecycle states

Stati consigliati:

- `planned`
- `ready`
- `in_progress`
- `blocked`
- `review`
- `verified`
- `done`

Semantica:

- `planned`: esiste ma non è ancora pronto;
- `ready`: tutte le dipendenze minime sono soddisfatte;
- `in_progress`: in lavorazione;
- `blocked`: fermo per impedimento o decisione mancante;
- `review`: completato tecnicamente ma in verifica;
- `verified`: ha superato i gate richiesti;
- `done`: chiuso logicamente e amministrativamente.

---

## 10.5 Ruoli astratti

Ruoli condivisi consigliati:

- `orchestrator`
- `implementer`
- `tester`
- `reviewer`
- `documenter`
- `researcher`

Non sono ancora subagent specifici di un tool.  
Sono una semantica astratta, portabile.

---

## 10.6 Effort

Effort condiviso consigliato:

- `low`
- `medium`
- `high`

Serve a:
- stimare il peso di un item;
- scegliere eventualmente modelli/subagent diversi;
- decidere se un item può stare in un blocco o se va isolato.

---

## 10.7 Metadata esecutivi

Campi consigliati:

- `depends_on`
- `role`
- `effort`
- `commit_group`
- `scope`
- `artifacts_in`
- `artifacts_out`
- `checks`
- `triggers`
- `tools_profile`
- `notes`

---

## 11. Modello di esecuzione DAG-ready

## 11.1 Regola fondamentale

L’umano pianifica in:
- milestone
- sprint
- item

L’agente esegue in:
- dipendenze
- gruppi compatibili
- eventuale parallelismo controllato

Quindi:

\[
item_i \text{ è eseguibile} \iff deps(item_i)\subseteq done\_or\_verified
\]

## 11.2 Regola di parallelismo
Il parallelismo è consentito solo se:
- le dipendenze sono soddisfatte;
- lo scope è compatibile;
- non c’è collisione evidente sui file o sui boundary;
- il blocco risultante ha chiusura verificabile.

## 11.3 Regola di grouping
L’agente può raggruppare item compatibili in un `commit_group` comune se:
- il gruppo è semanticamente coerente;
- i gate richiesti sono compatibili;
- il reviewer può valutare il blocco senza perdere tracciabilità.

## 11.4 Regola sulle collisioni
Se due item:
- toccano lo stesso scope sensibile,
- richiedono decisioni umane diverse,
- o producono evidenze incompatibili,

allora non vanno raggruppati automaticamente.

## 11.5 Sequenzialità umana, non runtime
La sequenzialità resta nel modo in cui l’umano pensa, parla e ordina il piano.
Non è più una legge assoluta di esecuzione.

---

## 12. Commit groups, blocchi di sviluppo e chiusura

## 12.1 Perché non più “un item = un commit” come legge universale
Quella regola è disciplinata ma troppo rigida per:
- blocchi coerenti di sviluppo;
- parallelismo controllato;
- multi-agent futuri;
- riduzione dell’overhead.

## 12.2 Nuova regola
Il boundary naturale diventa il **commit group verificato**.

### Regola
Un `commit_group` può chiudersi con un commit solo se:
- tutti gli item del gruppo sono almeno `review` o `verified`;
- i check richiesti dal gruppo sono verdi;
- il gruppo è semanticamente leggibile;
- la tracciabilità item -> evidenze -> commit resta chiara.

## 12.3 Commit groups come cluster
Un `commit_group` può essere visualizzato anche come cluster nel DAG.

---

## 13. Subagent e portabilità cross-tool

## 13.1 Regola generale
Il modello shared deve rimanere **neutro**.

Non va scritto usando primitive proprietarie di un singolo tool.

## 13.2 Mappatura concettuale

### Codex / OpenAI
- `AGENTS.md` gerarchici;
- scope di directory;
- task paralleli e ambienti isolati;
- buona integrazione con un orchestrator che usa `PLAN.yaml` come control plane.

### Claude Code
- `CLAUDE.md` gerarchici;
- `@import`;
- subagent in `.claude/agents/`;
- contesti separati;
- buon fit per ruoli/effort.

### GitHub Copilot
- repository-wide / path-specific instructions;
- `AGENTS.md` supportato;
- precedence dei file più vicini;
- buon fit per il layer di istruzioni e per i vincoli locali.

### Kilo e altri
- custom modes e configurazioni specializzate;
- mapping possibile a partire da ruoli/effort/triggers neutrali.

## 13.3 Campo condiviso consigliato
Per portabilità, nel piano e nel modello condiviso usare:

- `role`
- `effort`
- `triggers`
- `tools_profile`

e poi mappare a valle.

---

## 14. Automazione Git/GitHub in fasi

## 14.1 Principio generale
Automatizzare tutto subito è un errore.  
Le azioni irreversibili o potenzialmente costose vanno introdotte più tardi.

## 14.2 Vincoli strategici già fissati
- `develop` non va mai rimosso;
- prima della PR finale va verificato l’allineamento con `develop`;
- preferenza per **merge** e non **rebase**;
- la storia separata dei rami va preservata;
- il merge finale non è da automatizzare all’inizio.

## 14.3 Fasi

### Fase A — foundation
Automatico:
- naming branch;
- update `PLAN.yaml`;
- rendering `PLAN.md` / `PLAN.dot`;
- commit locali per commit group.

Non automatico:
- push;
- PR;
- merge.

### Fase B — collaboration
Automatico:
- push del branch feature;
- apertura PR draft;
- verifica stato `develop`;
- merge di `develop` nel feature branch prima dei check finali.

Ancora non automatico:
- merge finale.

### Fase C — controlled merge
Automatico:
- auto-merge della PR quando tutti i check richiesti sono verdi e le review richieste sono soddisfatte.

### Fase D — hygiene
Opzionale:
- cleanup branch feature post-merge;
- mai per `develop`.

---

## 15. Struttura concreta dei 3 livelli

## 15.1 Livello 0 — central repo

```text
agent-os/
├── workflow/
│   ├── shared-workflow.md
│   ├── item-taxonomy.md
│   ├── lifecycle.md
│   ├── git-automation-policy.md
│   └── portability-model.md
├── schemas/
│   ├── plan.schema.json
│   └── ...
├── templates/
│   ├── repo-AGENTS.md.template
│   ├── repo-ARCHITECTURE.md.template
│   ├── repo-REPO_MAP.md.template
│   └── PLAN.yaml.template
├── scripts/
│   ├── sync-workspace.sh
│   ├── render-plan.py
│   ├── validate-plan.py
│   └── bootstrap-repo.sh
├── prompts/
│   ├── orchestrator.md
│   ├── reviewer.md
│   └── ...
└── skills/
```

## 15.2 Livello 1 — workspace runtime

```text
work/
├── AGENTS.md
├── CLAUDE.md
├── repo-a/
├── repo-b/
└── repo-c/
```

## 15.3 Livello 2 — repo locale

```text
repo/
├── AGENTS.md
├── ARCHITECTURE.md
├── REPO_MAP.md
├── PLAN.yaml
├── PLAN.md          # generated
├── PLAN.dot         # generated
├── docs/
│   └── adr/
└── ...
```

---

## 16. Cosa va nei vari livelli: file, autorità e non-goal

## 16.1 Livello 0
### Va qui
- workflow condiviso;
- tassonomia;
- schema;
- script;
- template;
- skill condivise.

### Non va qui
- piano attivo di uno specifico repo;
- vincoli software specifici di uno specifico progetto.

## 16.2 Livello 1
### Va qui
- file condivisi runtime che gli agenti devono leggere per scope.

### Non va qui
- source of truth modificata a mano;
- contenuti che devono divergere da macchina a macchina senza controllo.

## 16.3 Livello 2
### Va qui
- `AGENTS.md` locale;
- `ARCHITECTURE.md`;
- `PLAN.yaml`;
- `REPO_MAP.md`;
- ADR locali.

### Non va qui
- duplicazione manuale del workflow condiviso;
- copia completa del control plane.

---

## 17. Primo MVP repo-agnostic da setuppare

## 17.1 Scopo dell’MVP
Avere una base solida, minima e scalabile per:
- workflow condiviso;
- repo locali sottili;
- piano machine-readable;
- viste generate;
- nessuna automazione Git pericolosa ancora attiva.

## 17.2 File minimi dell’MVP

### Livello 0
- `workflow/shared-workflow.md`
- `workflow/item-taxonomy.md`
- `workflow/lifecycle.md`
- `templates/repo-AGENTS.md.template`
- `templates/repo-ARCHITECTURE.md.template`
- `templates/repo-REPO_MAP.md.template`
- `templates/PLAN.yaml.template`
- `scripts/sync-workspace.sh`
- `scripts/render-plan.py`
- `scripts/validate-plan.py`

### Livello 1
- `AGENTS.md`
- `CLAUDE.md` (se usi Claude)

### Livello 2
- `AGENTS.md`
- `ARCHITECTURE.md`
- `REPO_MAP.md`
- `PLAN.yaml`

## 17.3 Cosa NON mettere nell’MVP
- subagent reali per ogni tool;
- auto-push;
- auto-merge;
- merge queue;
- orchestrazione multi-agent completa;
- `ADR` obbligatori dappertutto;
- generatori di skill custom.

---

## 18. Istruzioni da dare all’agent per realizzare il setup

Questa sezione è pensata per il tuo caso esplicito: **sarà un agent a creare tutto**.  
Tu non scriverai a mano né `.md` né `.yaml`.

## 18.1 Prompt/istruzioni di alto livello all’agent

### Obiettivo
“Crea un control plane centrale portabile e versionato, una workspace root con file condivisi runtime, e un bootstrap minimale dei repository locali con `AGENTS.md`, `ARCHITECTURE.md`, `REPO_MAP.md` e `PLAN.yaml`, seguendo la struttura e le authority formalizzate in questo documento.”

### Vincoli
- non introdurre file superflui;
- non introdurre automazioni Git irreversibili;
- non duplicare concern in più file;
- rispettare il modello a 3 livelli;
- usare `PLAN.yaml` come source of truth del piano;
- generare `PLAN.md` e `PLAN.dot` da script deterministici;
- mantenere il sistema repo-agnostic;
- non imporre vincoli software specifici se non nel repo locale;
- predisporre il modello per esecuzione dependency-driven, non per sequenzialità globale.

## 18.2 Sequenza di lavoro da far seguire all’agent

### Fase 1 — creare il repo centrale
1. creare la struttura `agent-os/`;
2. creare workflow condiviso, tassonomia, lifecycle;
3. creare template minimi;
4. creare script di sync/render/validate.

### Fase 2 — creare la workspace root runtime
1. creare `work/AGENTS.md` a partire dal workflow condiviso;
2. creare `work/CLAUDE.md` o equivalente se serve;
3. verificare che i file siano nel path giusto per gli agenti target.

### Fase 3 — bootstrap del primo repo
1. creare `repo/AGENTS.md` locale sottile;
2. creare `repo/ARCHITECTURE.md` minimale;
3. creare `repo/REPO_MAP.md`;
4. creare `repo/PLAN.yaml` iniziale;
5. generare `repo/PLAN.md` e `repo/PLAN.dot`;
6. validare coerenza del piano e rendering.

### Fase 4 — validazione
1. controllare che le authority siano non-ambigue;
2. controllare che `PLAN.yaml` sia la sola source of truth del piano;
3. controllare che non ci siano duplicazioni improprie;
4. testare il bootstrap su almeno un repo reale.

## 18.3 Istruzione forte da dare all’agent sul piano
“Non scrivere manualmente `PLAN.md` o `PLAN.dot`; scrivi solo `PLAN.yaml` e genera tutte le viste con gli script di rendering.”

## 18.4 Istruzione forte da dare all’agent sulla governance
“`AGENTS.md` governa il workflow e le authority; `ARCHITECTURE.md` governa i vincoli software; `PLAN.yaml` governa il tracking esecutivo locale. Non mescolare le tre concern.”

---

## 19. Roadmap di crescita: cosa fare prima e cosa differire

## 19.1 Fase 1 — foundation
Realizzare:
- control plane centrale;
- tassonomia;
- lifecycle;
- `PLAN.yaml`;
- rendering deterministico;
- file locali minimi.

## 19.2 Fase 2 — DAG readiness
Realizzare:
- `depends_on`;
- `commit_group`;
- `role`;
- `effort`;
- visualizzazione `PLAN.dot`;
- grouping logic di base.

## 19.3 Fase 3 — subagent portability
Realizzare:
- ruoli neutrali;
- mapping verso Claude/Codex/Copilot;
- eventuale `tools_profile`;
- eventuali template per subagent o custom modes.

## 19.4 Fase 4 — Git automation foundations
Realizzare:
- policy branch;
- naming branch;
- commit groups -> commit reali;
- eventuale push controllato;
- eventuale draft PR.

## 19.5 Fase 5 — advanced automation
Differire fino a stabilità:
- auto-merge;
- cleanup branch automatico;
- multi-agent orchestration completa;
- queue/scheduler esterno;
- skill custom avanzate.

---

## 20. Mappatura dell’approccio al caso DUCT e ad altri repo esistenti

Questa sezione serve a preservare il collegamento con il caso reale da cui si è partiti, senza rendere il documento DUCT-specifico.

### 20.1 Caso DUCT
Nel root DUCT attuale:
- le authority locali sono `AGENTS.md` e `PLAN.md`;
- l’agente non può pushare;
- non c’è una milestone attiva;
- `X5` risulta già chiusa.

Quindi l’applicazione del modello astratto al caso DUCT implica:
- nuova milestone (`X9`) per la rifondazione della governance;
- split tra `AGENTS.md`, `ARCHITECTURE.md` e `PLAN.yaml`;
- passaggio da sequential execution constitution a dependency-driven execution;
- preservazione della user decision supremacy;
- nessun cambiamento runtime nel primo milestone di governance.

### 20.2 SignalProcessing
È il miglior esempio esistente del principio di canonical source rule:
- `AGENTS.md` per operational behavior;
- `docs/architecture/*` per technical architecture;
- `docs/adr/*` per rationale;
- `PLAN.md` per chronology/tracking.

Questo repo conferma che lo split di concern non è solo sensato ma già praticato con successo.

### 20.3 SmartBox
È un esempio forte di:
- planning-before-execution;
- atomicità;
- dual tracking;
- PASS/NON-PASS discipline.

Da lì conviene preservare:
- la disciplina del tracking;
- la serietà dei checkpoint;
- la distinzione netta tra chiusura e semplice avanzamento del lavoro.

### 20.4 9_DNAIS
Il caso 9_DNAIS ha mostrato un anti-pattern da evitare: una root non autoritativa che rimanda a path assoluti locali non portabili.  
Il modello a 3 livelli proposto qui risolve proprio quel problema:
- source of truth portabile;
- materializzazione runtime corretta;
- repo locali chiari.

---

## 21. Sintesi finale

### 21.1 Tesi principale
La soluzione migliore, ad oggi, per un setup portabile e scalabile per coding agents non è:
- né “tutto in ogni repo”,
- né “un solo file globale per tutto”.

È:

\[
\text{central control plane} + \text{workspace runtime layer} + \text{repo-local thin layer}
\]

### 21.2 Corollari principali
- il workflow si condivide, il piano no;
- la tassonomia si condivide, i vincoli software no;
- il piano si struttura, poi si renderizza in testo e grafo;
- l’umano decide, l’orchestrator traduce nel piano;
- i worker eseguono, ma non sono owner del piano;
- la sequenzialità resta semantica umana, non vincolo runtime assoluto;
- l’automazione Git si introduce a strati, non in un colpo solo.

### 21.3 Formula finale del modello
\[
\text{human planning} = \text{milestone/sprint/item}
\]

\[
\text{machine execution} = \text{deps + roles + effort + commit groups}
\]

\[
\text{control plane} = \text{shared workflow + taxonomy + templates + tooling}
\]

\[
\text{repo governance} = \text{workflow authority + software constraints + local plan}
\]

---

## 22. Pacchetto di handoff per continuare la conversazione altrove

Questa sezione è progettata apposta per poter riprendere il lavoro in un’altra chat, con un altro agent o in un altro strumento.

### 22.1 Stato attuale del design
- è stato definito un modello architetturale a 3 livelli;
- è stato deciso che il workflow condiviso vive nel control plane centrale;
- è stato deciso che il piano è locale al repo;
- è stato deciso che il piano è machine-readable (`PLAN.yaml`);
- è stato deciso che `PLAN.md` e `PLAN.dot` sono viste generate;
- è stata decisa una tassonomia condivisa di item e actions;
- è stato deciso di far decadere la sequenzialità runtime globale a favore di dipendenze esplicite;
- è stato deciso di usare ruoli/effort neutrali per portabilità cross-tool;
- è stato deciso di introdurre l’automazione Git/GitHub in fasi.

### 22.2 Prompt di handoff consigliato
Puoi incollare in un’altra conversazione qualcosa di simile:

> Sto progettando un setup portabile per coding agents basato su 3 livelli:
> 1) control plane centrale versionato,  
> 2) workspace root runtime condivisa,  
> 3) layer locale per repo.  
>  
> Decisioni già prese:
> - no `PLAN` globale condiviso;
> - sì a tassonomia condivisa di item/actions/states/roles/effort;
> - `PLAN.yaml` come source of truth locale;
> - `PLAN.md` e `PLAN.dot` come viste generate;
> - un solo orchestrator/planner agent è owner del piano;
> - gli item si scrivono in sequenza umana ma si eseguono dependency-driven;
> - commit su commit groups verificati;
> - automazione Git/GitHub introdotta in fasi, non tutta insieme.  
>  
> Voglio continuare da qui e trasformare il design in:
> - schema iniziale di `PLAN.yaml`;
> - template iniziali di `AGENTS.md`, `ARCHITECTURE.md`, `REPO_MAP.md`;
> - script `render-plan` e `validate-plan`;
> - piano operativo dell’MVP.

### 22.3 Minimo contesto che deve sempre essere ricordato
- una concern deve avere una sola authority canonica;
- `AGENTS.md` non deve diventare un mostro che contiene anche tutta l’architettura;
- `ARCHITECTURE.md` non deve diventare un piano;
- `PLAN.yaml` non deve diventare una seconda costituzione del repo;
- `PLAN.md` e `PLAN.dot` non si editano a mano;
- l’umano non edita la source of truth del piano: la aggiorna l’orchestrator a partire dai prompt/decisioni.

---

## 23. Riferimenti

### OpenAI / Codex
- Introducing Codex — OpenAI  
  https://openai.com/index/introducing-codex/
- Structured Outputs — OpenAI Platform  
  https://platform.openai.com/docs/guides/structured-outputs
- Prompt Caching — OpenAI Platform  
  https://platform.openai.com/docs/guides/prompt-caching
- Prompting / prompt objects / versioning — OpenAI Platform  
  https://platform.openai.com/docs/guides/prompting

### Anthropic / Claude Code
- Claude Code Memory  
  https://docs.anthropic.com/en/docs/claude-code/memory
- Claude Code Subagents  
  https://docs.anthropic.com/en/docs/claude-code/sub-agents

### GitHub Copilot / GitHub
- About customizing GitHub Copilot responses  
  https://docs.github.com/en/copilot/concepts/prompting/response-customization
- Adding repository custom instructions for GitHub Copilot  
  https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
- About protected branches  
  https://docs.github.com/github/administering-a-repository/about-protected-branches
- Automatically merging a pull request  
  https://docs.github.com/github/collaborating-with-issues-and-pull-requests/automatically-merging-a-pull-request
- About pull request merges  
  https://docs.github.com/github/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges
- Merging a pull request with a merge queue  
  https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request-with-a-merge-queue

### Graphviz
- DOT language  
  https://graphviz.org/doc/info/lang.html
- Graphviz outputs  
  https://graphviz.org/docs/outputs/

### Kilo
- Custom Modes  
  https://kilo.ai/docs/features/custom-modes

### Repositories analizzati come precedenti interni
- `NickF93/MH-PatchCore-Private`
- `nAIs-BO/SignalProcessing`
- `nAIs-BO/SmartBox`
- `nAIs-BO/9_DNAIS`
- `matt-k-wong/mkw-DAG-architect`

---

## Chiusura

Questo documento formalizza il modello architetturale consolidato emerso finora.  
Il prossimo passo naturale non è discutere ancora a livello astratto, ma passare a un deliverable tecnico concreto:

1. schema `PLAN.yaml`;  
2. template di `AGENTS.md`;  
3. template di `ARCHITECTURE.md`;  
4. template di `REPO_MAP.md`;  
5. script `render-plan` e `validate-plan`;  
6. bootstrap dell’MVP nel control plane centrale e nella workspace root.

