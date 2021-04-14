# notes
dev
- experiments are interactive
- creation of computes via pipelines

```
if branch - 
  job: unit tests
if master
  stage: experiment
  if experiments
    - run deploy
  if not experiment
    stage: dev
    - job: unit tests - ci
    - job: deploy - cd
    stage: qa
    - job: deploy
    - job: integration tests
      - task: run pipelines
      - task: app insights metrics
      - task: notification 
      - task: approval gate
    stage: prod
    - job: deploy - canary/blue-green
```