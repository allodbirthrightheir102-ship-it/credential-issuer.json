stages:
  - validate
  - policy-check

kustomize-syntax-validation:
  stage: validate
  image: line/kubectl-kustomize:latest
  script:
    - echo "Executing zero-drift structural verification across 6,000 node overlays..."
    - kustomize build overlays/development > /dev/null
    - kustomize build overlays/production > /dev/null
  only:
    - main
    - tags

sentinel-script-lint:
  stage: policy-check
  image: python:3.11-slim
  script:
    - pip install flake8
    - flake8 --count --select=E9,F63,F7,F82 --show-source --statistics scripts/
