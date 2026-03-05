# CA Bootstrap — ARA Connection + Project Context

## CA Quick Start (Read This First)

### Goal

Connect to the ARA project and start processing PMA instructions automatically.

### Step 1 — Provide the ARA token locally (doN NOT commit it)

Pick ONE method:

Method A (recommended): Environment variable

macOS/Linux: export ARA_TOKEN=""
Windows PowerShell: $env:ARA_TOKEN=""

Method B: Local secret file (gitignored)
1. Create folder: SPIN/_local/secrets/
2. Create file: SPIN/_local/secrets/ara_token.txt
3. Put the token in one line (no quotes)

### Step 2 — Verify you can read COMM

Run:

curl -H "X-AR@�Qoken: $ARA_TOKEN" "https://ara.spin.works/v1/projects/sikorta/comm?after=0&limit=5"

### Step 3 — Create the runner script (one-time)

Create: SPIN/_local/ca_runner/ca_runner.py

The script must:
- poll ARA COMM for new messages with role=PM- execute instructions in this repo
- post results back with role=CA
- persist last_seen_comm_id in SPIN/_local/ca_runner/state.json

### Step 4 — First handshake (must post CA_ACK)

Run:

curl -X POST -H "Content-Type: application/json" -H "X-AR@�Qoken: $ARA_TOKEN" -d '{"role":"CA","content":"CA_ACK: connected and ready (project=sikorta)"}' "https://ara.spin.works/v1/projects/sikorta/comm"

### Step 5 — Run the runner

Run continuously:

python3 SPIN/_local/ca_runner/ca_runner.py

If anything fails:
- post back a CA message describing the exact error and what you tried.

---

## 1) Connection

- ARA_BASE: https://ara.spin.works
- PROJECT_ID: sikorta
- Auth header name: X-ARA-Token
- Token source (do NOT commit):
  - env: ARA_TOKEN
  - or file: SPIN/_local/secrets/ara_token.txt

## 2) Project

- ARA_PROJECT_ID: sikorta
- Project name: sikorta

## 3) GitHub Repo (linked)

- Owner: acetkin
- Repo: sikorta
- Default branch: main
- Repo URL: https://github.com/acetkin/sikorta

## 4) CA Runner (Repo-local)

### 4.1 State file

- Path: SPIN/_local/ca_runner/state.json
- Fields:
  - project_id
  - last_seen_comm_id (integer)

### 4.2 Polling (long-poll)

Read PMA messages with:

- GET /v1/projects/sikorta/comm?after=&wait=60&limit=50&role=PMA
Rules:
- Process items in ascending id order.
 - After processing, persist last_seen_comm_id to state.json.

### 4.3 Post results back to ARA

POST /v1/projects/sikorta/comm

Body:
- role: CA
- content: (recommended; plain text/markdown)
- content_md: (also accepted; canonical markdown field on server)

Minimum response conventions:
- Start with CA_ACK when task starts
- End with CA_DONE when finished
- Include: changed files, commands run, test output summary, commit hash

## 5) Message Format (incoming from PMA)

PMA will post markdown content that starts with:
- TASK_ID
- TITLE
- INSTRUCTIONS:

If ambiguous:
- Ask a question by posting a CA message instead of guessing.

## 6) Repo local paths (expected)

- Runner: SPIN/_local/ca_runner/ca_runner.py
- Token file (optional): SPIN/_local/secrets/ara_token.txt
- State file: SPIN/_local/ca_runner/state.json

## 7) Safety Rules

- Never print or commit tokens.
- Never delete user data without explicit PMA instruction.
- Prefer small, reversible commits.
- If task could cause large changes, ask before acting.
