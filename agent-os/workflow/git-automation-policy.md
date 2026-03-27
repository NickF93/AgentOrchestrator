# Git Automation Policy

## Principle
Introduce automation in phases. High-risk or irreversible operations come later.

## Branching and Merge Preferences
- Keep develop branch protected and never deleted.
- Prefer merge flow over rebase for integration in this model.
- Preserve branch history for reviewability.

## Automation Phases
### Phase A: Foundation
Allowed automation:
- branch naming conventions
- local commit creation by commit_group
- PLAN source updates
- generation of PLAN views

Not automated:
- push
- pull request creation
- merge

### Phase B: Collaboration
Allowed automation:
- push feature branches
- open draft PR
- merge develop into feature branch before final checks

Still not automated:
- final merge

### Phase C: Controlled Merge
Allowed automation:
- enable auto-merge only when required checks and review conditions are met

### Phase D: Hygiene
Optional automation:
- post-merge cleanup of feature branches
- never delete develop via automation

## Safety Rules
- Do not automate force-push.
- Do not automate destructive branch operations in early phases.
- Keep branch-protection compatibility as a hard requirement.
