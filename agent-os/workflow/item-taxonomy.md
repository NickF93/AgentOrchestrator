# Item Taxonomy

## Item Types
- X: milestone container (non-executable)
- S: sprint container (non-executable)
- Q: decision gate / blocking question
- D: documentation or governance work
- M: implementation, integration, refactor
- F: fix or hotfix
- T: test or validation
- C: checkpoint, review, closure gate

## Action Taxonomy
- audit
- plan
- design
- implement
- refactor
- test
- verify
- document
- review
- checkpoint
- decide
- migrate

## Recommended Type/Action Coherence
- Q: review, decide
- D: plan, document, review, checkpoint
- M: design, implement, refactor, migrate, verify
- F: implement, test, verify
- T: test, verify
- C: review, checkpoint, verify

## Lifecycle States
- planned
- ready
- in_progress
- blocked
- review
- verified
- done

State flow:
- planned -> ready -> in_progress -> review -> verified -> done
- blocked is a side-state reachable from active states

## Roles
- orchestrator
- implementer
- tester
- reviewer
- documenter
- researcher

## Effort Levels
- low
- medium
- high

## Metadata Fields
- depends_on
- role
- effort
- commit_group
- scope
- artifacts_in
- artifacts_out
- checks
- triggers
- tools_profile
- notes
