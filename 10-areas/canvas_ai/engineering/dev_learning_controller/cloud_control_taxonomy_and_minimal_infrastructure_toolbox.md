# Cloud Control Taxonomy

A reusable control-theoretic taxonomy for cloud provisioning and operation, designed for a **minimal, reproducible dev/execution substrate** (not a cloud-architect track).

## Core Terms

- **Plant**: the cloud account/subscription and its resources.
- **State**: the set of provisioned resources + configurations (what exists).
- **Reference model**: the desired state space (allowed/target configurations).
- **Controller**: the mechanism that drives state toward the reference model.
- **Observer**: mechanisms that measure/estimate state and surface deviations.
- **Actuators**: the APIs that create/update/destroy resources.

---

# Control Modes

## 1) Feedforward Control

**Definition**: Prevent undesired states by constraining actions *before* they change the plant.

### 1.1 IaC Feedforward (Primary)
- **Mechanism**: Terraform/OpenTofu plan/apply; module interfaces; variable constraints.
- **Strength**: explicit diffs; replayable; human-legible control signal.
- **Failure mode**: bypass via manual portal/CLI changes.

### 1.2 Workflow Feedforward
- **Mechanism**: CI gates; PR review; required checks.
- **Strength**: low effort guardrails; good for project-specific invariants.
- **Failure mode**: bypass via direct apply outside CI.

**When to use**: default for Tier 0–3 primitives; keeps control legible and testable.

---

## 2) Feedback Control

**Definition**: Detect deviations after the plant changes and correct/rollback.

### 2.1 Drift Feedback (Primary)
- **Mechanism**: Terraform state + drift detection; periodic plan in CI.
- **Control signal**: “state differs from desired; here is the delta.”
- **Actuation**: apply to converge; or destroy/recreate.

### 2.2 Operational Feedback
- **Mechanism**: logs/metrics (CloudWatch / Log Analytics minimal); CI job outcomes.
- **Control signal**: failures, latency, quota hits, cost spikes.

**When to use**: whenever you need *post-fact* correction and observability; keep scope minimal.

---

## 3) Saturation and Interlocks

**Definition**: Hard bounds at the actuator boundary that limit reachable state space.

### 3.1 Provider-Side Saturation (Optional Safety Interlocks)
- **Mechanism**: Azure Policy / AWS SCP-like constraints (or equivalent account-level denies).
- **Goal**: act as a *dead-man’s switch*, not a governance framework.

**Recommended minimal interlocks (only if needed)**:
- Region allowlist (prevent accidental cross-region spend)
- Instance-size ceiling (prevent runaway cost)
- Deny deletion of Terraform state backend resources (state bucket/container)

**When to use**: only when the cost/safety consequence is high and you want a hard backstop.

---

# CSA/NIST Mapping (Practical Interpretation)

- **CSA/NIST are reference models**, not controllers.
- For this workflow, treat them as:
  - **state-space definitions** (what is acceptable)
  - plus **evidence expectations** (what you need to show)
- Enforce primarily via **IaC feedforward + drift feedback**, with optional **provider saturation** only as safety bounds.

---

# Plane Model Integration

## Execution Plane
Where compute runs: CI runners, remote builders, devcontainers, ephemeral VMs.

## Cache Plane
Where accelerators live: object storage caches, container registries, artifact retention.

## Observer Plane
Where insight lives: CI artifacts, reports, optional Sourcegraph later.

Control-locus defaults:
- **IaC feedforward** controls the *Plant State* (Tier 0–3).
- **Feedback** (drift + CI outcomes) controls convergence and recovery.
- **Saturation** is optional hard bounding.

---

# Tier Model → Azure vs AWS Primitives

## Tier 0 — Identity & Access (minimal)
- Azure: Subscription + Entra identity; CI **Service Principal** + Role Assignment
- AWS: Account; CI **IAM Role** + Policy

## Tier 1 — Execution Substrate
- Azure: Linux VM (simple); optional ACI
- AWS: EC2 (simple); optional Fargate

## Tier 2 — Artifact & Cache Plane
- Azure: Blob Storage + ACR
- AWS: S3 + ECR

## Tier 3 — Networking (minimal)
- Azure: default VNet + NSG; public IP if needed
- AWS: default VPC + Security Group; public IP as needed

## Tier 4 — Automation
- CI: GitHub Actions / Azure Pipelines
- IaC: Terraform/OpenTofu (preferred) per-cloud stacks

## Tier 5 — Observability (optional)
- Azure: basic Log Analytics
- AWS: basic CloudWatch logs

---

# Boilerplate Candidates vs Not

## Strong Boilerplate Candidates
- CI identity (Azure SP / AWS IAM Role)
- VM provisioning (Linux VM / EC2)
- Object storage for artifacts/caches (Blob / S3)
- Container registry (ACR / ECR)
- Security rules (NSG / SG)
- Lifecycle/retention rules
- Remote state backends (per cloud)

## Not Boilerplate (Project-Specific)
- Build/test scripts
- CI workflow logic (jobs/steps)
- VM sizing decisions
- Application deployment logic
- Observability dashboards

---

# Minimalist Toolbox Repo Layout

A template repo intended to be copied or vendored into projects.

```
cloud-toolbox/
  README.md
  docs/
    control-taxonomy.md
    tier-to-primitives.md
    operating-rules.md

  infra/
    azure/
      backend/                 # state storage for tofu/tf
      stacks/
        base/                  # Tier 0–3: identity, vm, storage, registry, nsg
      modules/                 # small, single-purpose modules

    aws/
      backend/                 # state storage for tofu/tf
      stacks/
        base/                  # Tier 0–3: identity, ec2, s3, ecr, sg
      modules/

  scripts/
    az-login.sh
    aws-login.sh
    provision-azure.sh
    provision-aws.sh
    destroy-azure.sh
    destroy-aws.sh
    plan-azure.sh
    plan-aws.sh

  ci/
    examples/
      drift-check.yml          # periodic tofu plan
      provision-ephemeral.yml  # create/destroy ephemeral infra for jobs

  .tool-versions / .mise.toml  # optional tool pinning
```

## Design rules
- Prefer **OpenTofu/Terraform** as the primary controller.
- Keep Azure and AWS stacks separate; do not force symmetry.
- Use provider-side policies only as **saturation interlocks**.
- Keep scripts thin wrappers; no hidden logic.

---

# Default Operating Rules

1. **Primary controller**: IaC feedforward (tofu/tf) + drift feedback.
2. **Saturation**: only for cost/safety interlocks.
3. **No cross-cloud coupling** (no shared caches/state between clouds).
4. **One primary cloud per project**, other cloud is contrast/learning.
5. **Boilerplate covers Tier 0–3 only**; project logic remains project-owned.

