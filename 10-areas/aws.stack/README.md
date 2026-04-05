## Final recommended architecture

This is the final shape I recommend, superseding the earlier marimo-first draft. The stable part to preserve from that draft is the **API-first resource model with narrow read and command surfaces**, while the primary operator surface should now be **Managed Grafana**, with only a **small custom action plane** for mutations. 

## 1. Control planes

### A. Authority plane

This is the only authoritative system.

* **API Gateway HTTP API**
* **Lambda**
* **Step Functions**
* **EventBridge**
* **DynamoDB**
* **SQS + DLQ**
* **Secrets Manager**
* **CloudWatch**

Responsibilities:

* provider ingress
* command handling
* workflow orchestration
* state persistence
* audit and replay
* observability emission

### B. Operator plane

This is read-heavy and action-light.

* **Amazon Managed Grafana** as the main operator UI
* **tiny custom action surface** behind API Gateway + Lambda for write actions only

Responsibilities:

* lifecycle visibility
* live delivery tracking visibility
* incidents and exceptions
* a few audited mutations

---

## 2. Operator surface

### Primary operator UI: Managed Grafana

Grafana is the default console.

It should host two main lanes:

#### Lane 1 — AWS order lifecycle

Panels for:

* orders by state
* awaiting approval
* approval latency
* dispatch failures
* delivery completions
* stuck workflows
* DLQ depth
* notification failures

#### Lane 2 — Uber Direct live tracking

Panels for:

* active deliveries
* courier status
* ETA drift
* near-handoff alerts
* delivery exceptions
* live or near-live map panel

### Action model

Do **not** build a large custom operator app.

Instead, expose only a small set of mutation endpoints:

* `POST /orders/{id}/approve`
* `POST /orders/{id}/reject`
* `POST /orders/{id}/dispatch/retry`
* `POST /orders/{id}/customer-notification`
* `POST /deliveries/{id}/handoff-action`

Grafana links, buttons, or drill-through flows can point into these actions, or into tiny internal forms if needed.

---

## 3. Service boundaries

### Ingress APIs

Provider-facing:

* `POST /providers/twilio/inbound-sms`
* `POST /providers/uber-direct/status`

Operator-facing:

* `GET /orders`
* `GET /orders/{id}`
* `GET /orders/{id}/events`
* `GET /incidents`
* `GET /metrics/summary`
* `GET /orders/{id}/tracking`

Mutation-facing:

* `POST /orders/{id}/approve`
* `POST /orders/{id}/reject`
* `POST /orders/{id}/dispatch/retry`

## 4. Runtime flow

### Order intake

* Twilio webhook hits API Gateway
* Lambda verifies and normalizes payload
* event emitted to EventBridge
* Step Functions execution starts
* DynamoDB state initialized

### Approval

* workflow enters approval-needed state
* approval becomes visible in Grafana read model
* operator approves/rejects via small action endpoint
* Lambda validates, audits, and signals workflow continuation

### Dispatch

* workflow requests Uber Direct dispatch
* Lambda adapter calls Uber Direct
* provider correlation persisted
* status updates return through Uber webhook ingress

### Tracking

* Uber status webhook updates delivery read model
* DynamoDB and metrics update
* Grafana map and lifecycle panels refresh

### Completion

* delivery completion event
* customer thank-you notification
* workflow finalized
* metrics and audit records emitted

---

## 5. Data model split

### System of record

* **DynamoDB**

  * orders
  * provider correlation
  * idempotency
  * action audit
  * delivery tracking snapshot

### Event backbone

* **EventBridge**

  * normalized domain events only

### Workflow state

* **Step Functions**

  * lifecycle progression
  * wait states
  * retries
  * compensation paths

### Failure isolation

* **SQS + DLQ**

  * webhook buffering
  * fragile provider callbacks
  * retry exhaustion capture

---

## 6. Observability model

### AWS-native base plane

Use AWS-native observability first.

* CloudWatch metrics
* CloudWatch logs
* CloudWatch alarms
* Embedded Metric Format from Lambdas
* Step Functions execution metrics
* API Gateway metrics
* DynamoDB metrics
* DLQ alarms

### Main UI

* Managed Grafana consumes observability and read-model feeds
* no separate browser console unless proven necessary

### Decision rule

If Grafana covers the operator workflow acceptably, stop there.
Only add another UI tier if a required action or workflow is genuinely blocked.

---

## 7. Security and policy

### Auth boundary

* API Gateway authorizer for operator actions
* provider signature validation for inbound webhooks

### Mutation requirements

Every state-mutating action should require:

```json id="33c8p3"
{
  "actor": "ops_user_id",
  "reason": "payment confirmed",
  "idempotency_key": "..."
}
```

### Enforcement

* authorization in Lambda
* state legality checks before mutation
* audit record on every mutation
* conditional writes in DynamoDB for state transitions

---

## 8. Deployment model

### Default

* deploy control plane on AWS serverless
* provision Grafana workspace as the operator UI
* no marimo service by default
* no Android app by default

### Optional later

Only if needed:

* marimo as a sibling projection
* PWA/mobile shell
* dedicated browser console

Those remain optional expansions, not part of the recommended baseline. This follows the same API-first contract model from the earlier draft, but avoids turning marimo into the primary operator console. 

---

## 9. Final shape

```text id="k1qiwh"
Providers
  -> API Gateway
    -> Lambda adapters
      -> EventBridge
      -> Step Functions
      -> DynamoDB
      -> SQS/DLQ

Operator reads
  -> Managed Grafana
    -> CloudWatch + read models + tracking views

Operator actions
  -> API Gateway
    -> Lambda command handlers
      -> Step Functions / DynamoDB / EventBridge
```

## 10. Final recommendation

Use:

* **Managed Grafana** for the operator console
* **API Gateway + Lambda** for the small mutation surface
* **Step Functions + EventBridge + DynamoDB** as the authority plane
* **CloudWatch** as the observability base
* **no additional UI tier unless Grafana proves insufficient**

This is the lowest-complexity architecture that still closes the loop.

