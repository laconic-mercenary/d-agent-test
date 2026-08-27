# Known Deficiencies — single-host-linux-rce

Engine-level gaps and quirks discovered while building and auditing this
scenario. These are documented here rather than silently worked around,
because they generalize beyond this one scenario. Where a workaround was
applied in `scenario.yaml`, it's noted — but the underlying engine behavior
still exists and will resurface for other scenarios that hit the same paths.

None of these were fixed in engine code as part of this scenario; they're
flagged for a future dedicated fix.

---

## 1. Paired `connection` event for a URL-referencing process produces a second, contradictory network flow

**Where:** `network_transaction_planner.py` (process→network auto-correlation) vs. the scenario-reference's own "Storyline process+connection pairing" guidance.

A `process` event whose command line references a URL (e.g. `curl http://...`)
already triggers accurate, fully-formed auto-generated connection/HTTP/file
evidence from the command line alone — correct method, URI, user agent, and a
`files.log` entry, all traceable back to the process's PID via its `ecar`
`FLOW` record.

The scenario-reference documentation instructs authors to *also* declare an
explicit `connection` event for such commands ("always add a paired
connection event with hostname set"). For curl specifically, doing so does
not merge with or get suppressed by the auto-generated evidence — it creates
a **second, independent network flow** to the same destination. If that
explicit event doesn't also specify `method`/`uri`, the engine fills it with
unrelated generic content (in this scenario's case, an auto-filled `GET
/assets/main.css` request with a different user agent), producing two
disconnected, contradictory pieces of network evidence for what should be
one logical fetch. No validation warning surfaces this duplication.

**Workaround used here:** the `evt-c2-fetch` step declares only the `process`
event (curl); the paired `connection` event was deliberately omitted.

**Suggested fix:** either (a) have the paired-connection guidance in
`docs/reference/scenario-reference.md` explicitly call out that some tools
(curl, wget) already auto-correlate and should NOT also get an explicit
connection event, or (b) make the engine merge/reconcile an explicit
connection event with a process's own auto-correlated flow when they target
the same destination, instead of treating them as two independent flows.

---

## 2. Two sequential `process` events meant to represent one causal action get mis-parented

**Where:** process-execution bundle's parent resolution (`spawn_rules.yaml`-driven), no cross-event linkage within a storyline step.

Declaring `sh -c id` as one `process` event and then a separate
`/usr/bin/id` process event (intending the second to represent "the shell
runs id") does **not** parent the second process under the first. There is
no concept of "this event is the child of the sibling event above it" in the
storyline schema — each declared process event resolves its own parent
independently via `spawn_rules.yaml`/process history. With no matching rule
tying a bare `id` to the just-declared `sh`, the engine fell back to
fabricating a plausible-but-unrelated `www-data` login/bash session as the
`id` process's parent — silently detaching it from the actual exploit chain.
Nothing at validate-time or generation-time flags this.

**Workaround used here:** the `evt-rce` step declares only the `/bin/sh`
event with `command_line: "sh -c id"`; the standalone `/usr/bin/id` process
event was removed, since the shell's own command line already documents the
`id` execution.

**Suggested fix:** either (a) add an explicit parent-hint field to the
`process` event schema for intra-step chaining, or (b) have the engine
default an unresolvable bare process to the most recently declared sibling
process in the same storyline/red-herring step before falling back to
`spawn_rules.yaml`/fabrication, or (c) add a validate-time warning when a
declared process's resolved parent doesn't match any sibling process
declared in the same step.

---

## 3. Plaintext-HTTP-to-HTTPS redirect policy silently overrides an authored `status_code`

**Where:** `_apply_plaintext_http_policy` / `plaintext_http_redirect_status`
(`proxy_uri.py`, `network_transaction_planner.py`).

For any plaintext (port 80) `connection` event whose destination is a public
IP and whose hostname classifies as "browser-like public" (the default
unless the hostname matches a non-browser prefix like `api.`, `cdn.`,
`assets.`, etc., or carries specific non-browser tags), the engine forces a
301/302 response regardless of an author-specified `status_code` — unless
that status is already 301/302. This is intentional, documented realism (a
real HTTPS-enforcing site won't serve real content over plaintext HTTP), but
it has a sharp edge: it's easy to author an exploit whose narrative requires
a synchronous 200 (e.g., "the app processes the payload and code executes
immediately after"), and have the engine silently substitute a redirect that
contradicts that causality — with no warning that the authored `status_code`
was overridden.

**Workaround used here:** the exploited hostname was changed from a generic
`app.*` domain to an `api.*` subdomain, which the engine's
`_NON_BROWSER_HOST_PREFIXES` list excludes from the redirect policy — a
legitimate modeling choice (the request is machine-driven, hitting an
admin/API surface, not a browser hitting a marketing page), but this only
works because the escape hatch happens to be hostname-prefix-driven.

**Suggested fix:** (a) have `eforge validate` or `eforge generate` warn when
an authored `status_code` on a `connection`/`beacon` event is overridden by
this policy, and/or (b) add an explicit override field — either on the
`connection` event itself or on `environment.network_identities` — so a
scenario author can assert "this specific domain does not enforce the
public-web HTTPS-redirect default" without relying on hostname-prefix
side effects or editing package-level config reserved for reusable domain
libraries.

---

## 4. DNS-before-TCP causal expansion issues a DNS query for a bare IP literal

**Where:** DNS-prerequisite path (`dns_lookup.py` /
`network_transaction_planner.py`), missing an `ipaddress.ip_address(...)`
literal guard.

For a `connection` with no `hostname` field, targeting a destination IP
directly (raw-IP C2, no DNS trail expected — and documented as such:
"Storyline connection events to raw C2 IPs will skip DNS emission"), the
engine's automatic DNS-before-TCP causal expansion still fires, treating the
destination IP *string* as if it were a domain name: it issues an `A` query
for `"154.16.92.201"` and gets back `154.16.92.201` as the answer, producing
a technically nonsensical (though mostly harmless) `dns.json`/`conn.json`
pair. A comparable guard already exists elsewhere in the codebase (e.g.
`plaintext_http_redirect_status` checks `ip_address(dst_ip).is_private`
before proceeding) but is missing from this path.

**Workaround used here:** none available at the scenario-authoring level —
this is purely a side effect of the engine's own process→network
auto-correlation (see #1), with no scenario field to suppress it once the
paired explicit `connection` event (which could have carried an empty/no
DNS hint) was removed. Documented as a caveat in the grading answer key
instead.

**Suggested fix:** add an IP-literal guard to the DNS-prerequisite trigger
path so a bare-IP destination (no `hostname`) never generates a DNS lookup,
matching the documented behavior.

---

## Not a deficiency (for context)

**HTTPS/TLS opacity is by design, not a bug.** Early in building this
scenario, the second-stage C2 fetch was modeled over HTTPS specifically to
keep the payload's contents undeterminable from network evidence. That
correctly produced zero response-body/file evidence for the connection (no
Zeek decryption is modeled). This was a deliberate design tradeoff, not an
engine defect — it was later reverted to plain HTTP for a different reason
(simplicity, avoiding interaction with deficiency #1 above), not because the
HTTPS opacity itself was wrong.
