# SOLID Refactoring Log (Pessoa 3 - Pagamentos)

This document captures technical evidence for PDF part 8 after each relevant change.

## Baseline (before Pessoa 3 changes)

### Context
- Date: 2026-05-21
- Scope: payment architecture for card, pix, boleto, and crypto extension

### Baseline Quality Evidence
- Test suite: 15 passed
- Command: `python -m pytest -q`

### Initial Violations Observed
- SRP: payment logic concentrated in `legacy.Sis.proc_pag` with mixed responsibilities.
- OCP: adding new payment methods requires changing conditional blocks in legacy flow.
- DIP: business flow depends on concrete branches instead of abstract payment contracts.

---

## Phase 1 - Contracts and domain support

### Change Summary
- Added `PaymentProcessor` abstraction in `src/services/payment_processor.py`.
- Extended `Order` model with optional `payment_type` in `src/models/order.py`.
- Extended repository contract with `update_payment_type` in `src/repositories/order_repository_interface.py`.

### Violations Addressed
- DIP: introduced an abstraction for payment processing contract.
- SRP (partial): order model now carries payment metadata explicitly instead of implicit flow-only state.

### Why this is safe
- `payment_type` is optional (`None` default), so existing order creation remains backward compatible.
- No behavior change was introduced in legacy payment flow in this phase.

### Evidence To Attach In PDF
- Diff excerpts of the 3 files above.
- Baseline + post-change tests passing.
- Rationale mapping: violation -> change -> expected architectural impact.

---

## Phase 2 - Payment strategies (card, pix, boleto)

### Change Summary
- Added concrete strategies in `src/services/payment_strategies.py`.
- Added strategy resolver/factory in `src/services/payment_processor_factory.py`.

### Violations Addressed
- OCP: new payment methods are added as new classes and mapping entries, no central conditional branch required.
- SRP: each payment strategy now owns only acceptance policy for one payment mode.

### Evidence To Attach In PDF
- Strategy class list (card, pix, boleto).
- Resolver mapping showing type -> strategy.
- Unit tests validating boleto does not auto-approve.

---

## Phase 3 - Dependency injection in application service

### Change Summary
- Extended `OrderService` to receive `PaymentProcessorFactory` by dependency injection.
- Added `process_payment` orchestration to fetch order, set payment type, execute strategy, and update status when needed.

### Violations Addressed
- DIP: `OrderService` depends on payment abstractions/resolver instead of concrete conditional logic.
- SRP (partial): payment decision is delegated to strategies, service coordinates use-case flow.

### Evidence To Attach In PDF
- Constructor signature before/after in `OrderService`.
- Tests with mocks proving service collaboration (`update_payment_type`, `update_status`).

---

## Phase 4 - Crypto extension

### Change Summary
- Added `CryptoPaymentProcessor` and resolver mapping for `PaymentType.Crypto`.
- Added payment tests including crypto approval flow.

### Violations Addressed
- OCP proof point: crypto added by extension, without changing card/pix/boleto strategy behavior.

### Evidence To Attach In PDF
- Crypto strategy implementation diff.
- Crypto unit test and passing result.

---

## Static analysis and metrics (executed 2026-05-21)

### ruff
- Auto-fixed 3 simple issues in `tests/integration/test_crypto_integration.py` (unused imports removed).

### mypy
- Focused type-check on payment scope: Success — no issues found after adding package markers.

### radon
- Cyclomatic complexity highlights:
	- `src/legacy.py` has several high-complexity methods (e.g., `Sis.add_ped` C(11)).
	- New payment module code has low complexity (A-rated).

### Next steps
- Record coverage metrics for payment modules (tests currently 23 passing). Run `coverage run -m pytest` and `coverage html` for artifact generation.

---

## Coverage run (2026-05-21)

Summary (select files):

```
TOTAL                                              385     16    96%
src\factories\order_factory.py                      39      1    97%   12
src\repositories\order_repository_interface.py      22      6    73%   12, 16, 20, 24, 28, 32
src\repositories\sqlite_order_repository.py         43      5    88%   72, 106-108, 111
src\services\payment_processor.py                    9      2    78%   10, 15
src\services\payment_strategies.py                  22      1    95%   18
```

Notes:
- Overall coverage for the project is 96%.
- `order_repository_interface.py` has lower coverage because interface methods are abstract and not directly executed by tests; consider adding interface-focused tests or excluding from coverage if desired.
- `payment_processor.py` has 78% because abstract base methods are not called directly; this is expected.

---

## Final decision for legacy scope

### Strategy chosen
- Keep `src/legacy.py` as the Golden Master reference.
- Avoid large refactors in the legacy file unless a change is required to preserve behavior or to document a specific violation.
- Concentrate the real SOLID improvements in the new architecture (`models`, `repositories`, `services`, strategies, and tests).

### Why this matches the PDF
- The assignment asks to identify violations, propose solutions, and preserve behavior during refactoring.
- The safest approach is to document the legacy problems and demonstrate their resolution in the new structure rather than rewriting the historical reference.

### Section 8 draft points
1. Legacy analysis: `legacy.py` concentrates SRP/OCP/DIP violations in one monolithic class.
2. Solution path: split responsibilities into model, repository, service, and strategy layers.
3. Evidence: Golden Master tests remain green; new payment tests pass; coverage is 96%; mypy and ruff are clean in the payment scope.
4. Extension proof: crypto payment was added without changing existing card/pix/boleto strategy classes.
5. Risk management: legacy file remains stable to avoid breaking the reference behavior required by the course.



