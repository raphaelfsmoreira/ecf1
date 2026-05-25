# Sprint 2 Feature Specification

## Context

This repository already contains a partial refactor of the legacy order system.
The legacy implementation in `src/legacy.py` mixes order creation, discounts, payment processing, notifications, persistence, reporting, and the special `PedEspecial` subclass in a single inheritance-based design.

The current refactor direction introduces a cleaner domain model with `Order`, `OrderItem`, `OrderRepositoryInterface`, `SQLiteDatabase`, and `OrderRepository`, but the Sprint 2 architecture is still missing the required Strategy, Observer/Pub-Sub, Factory, and explicit dependency injection layers.

The goal of this sprint is to complete the design refactor so the system can grow through new classes and abstractions instead of editing existing behavior-heavy classes.

## Goal

Implement Sprint 2 of the project with strong adherence to OCP, DIP, and LSP, while preserving the existing Golden Master behavior.

The implementation must remain compatible with the current `src/` layout and should use the existing domain model as the anchor for the new design.

## Current Repository Anchor Points

- `src/legacy.py` contains the old behavior and should be treated as the behavior reference, not as the target design.
- `src/database/database_interface.py` and `src/database/database.py` already define a persistence abstraction.
- `src/repositories/order_repository_interface.py` and `src/repositories/order_repository.py` provide the current repository layer.
- `src/models/order.py`, `src/models/order_item.py`, and `src/models/enums.py` define the refactored domain model.
- `src/main.py` is currently only a bootstrap entry point and should evolve into composition-root style wiring.
- `src/strategies/`, `src/observers/`, and `src/services/` are currently empty and are the natural places to add the Sprint 2 behavior.

## Mandatory Deliverables

1. Strategy pattern for discounts and payment methods.
2. Observer or Pub/Sub pattern for notifications.
3. Factory Method or Abstract Factory for order creation.
4. Explicit dependency injection: constructors receive abstractions, never create concrete collaborators internally.
5. `PedEspecial` must be corrected or removed; if it remains, it must obey Liskov Substitution.
6. Full type hints verified with `mypy --strict`.
7. Class diagram in PlantUML or Mermaid.
8. Three required extensions implemented.
9. Git tag `sprint-2` marking the final code delivery.

## Required Extensions

These three features come from the project brief and must be implemented after the main refactor.

1. Crypto payment with a 2% fee over the order total.
2. WhatsApp notifications available for all customer types.
3. Progressive volume discount: 3 or more units of the same item receive an additional 15% discount.

Critical rule: each extension must be implemented without modifying existing classes. Only add new classes, new strategies, new observers, or new factories.

## Architecture Target

The refactored design should follow this direction:

- `Order` remains a pure domain entity.
- `OrderRepository` only persists and hydrates orders.
- A service layer coordinates order creation, payment, status changes, and notifications.
- Discount rules are encapsulated in interchangeable Strategy classes.
- Payment methods are encapsulated in interchangeable Strategy classes.
- Notifications are published through an Observer/Pub-Sub abstraction.
- Order creation is centralized in a factory rather than scattered across services or UI/bootstrap code.
- Concrete classes are wired only in the composition root.

## Design Constraints

- Do not let constructors instantiate concrete repositories, publishers, strategies, or notifiers.
- Do not keep business rules inside repositories.
- Do not keep notification side effects inside payment or discount code.
- Do not use inheritance as a shortcut for special-case behavior if composition can express it more safely.
- Preserve the behavior covered by the Golden Master tests.
- Keep public APIs and filenames stable where possible, but prioritize the architecture target over preserving the legacy shape.

## LSP Requirement For `PedEspecial`

The legacy `PedEspecial` in `src/legacy.py` is an example of a fragile subtype because it changes payment/status behavior in ways that do not preserve the parent contract.

Preferred solution:

- eliminate `PedEspecial` and represent the special behavior with composition, strategies, or factories instead of inheritance.

Acceptable fallback:

- keep a specialized order type only if it can be substituted anywhere an `Order` is expected without changing correctness, invariants, or lifecycle rules.

## Suggested Implementation Boundaries

The implementation may create new modules such as:

- `src/strategies/discount_strategy.py`
- `src/strategies/payment_strategy.py`
- `src/observers/notification_observer.py`
- `src/factories/order_factory.py`
- `src/services/order_service.py`
- `src/services/payment_service.py`
- `src/services/notification_service.py`

The exact filenames may vary, but the separation of responsibilities should remain clear.

## Behavioral Acceptance Criteria

### Strategy: Discounts

- The system must support multiple discount algorithms without editing the order service each time a new rule is added.
- Existing discounts must be represented as strategies.
- The new progressive volume discount must be introduced as a new strategy, not a branch in a central method.

### Strategy: Payments

- Credit card, PIX, boleto, and crypto must be modeled as interchangeable payment strategies.
- Crypto payment must apply the 2% fee and must be implemented as an extension.
- Payment processing must not depend on `if/elif` chains in business-facing services.

### Observer / Pub-Sub: Notifications

- Standard customers receive email.
- VIP customers receive email and SMS.
- Corporate customers receive email and account-manager notification.
- WhatsApp becomes available to all customer types as an additional notification channel.
- Notification dispatch must be driven by observer/subscriber registration, not hard-coded branching in the order flow.

### Factory Method / Abstract Factory: Orders

- Order creation must be centralized in a factory abstraction.
- The factory must encapsulate the choice of which order object or order configuration to create.
- The caller should not need to know the concrete order wiring details.

### Explicit Dependency Injection

- Services and factories must receive repositories, strategies, and publishers through constructors or equivalent explicit injection points.
- No class should instantiate its own concrete collaborator when an abstraction is available.

### Typing

- All new and modified code paths must be fully type hinted.
- The sprint is not complete until `mypy --strict` passes on `src/`.

## Testing Expectations

The following tests should exist or be updated:

- Golden Master regression tests still pass unchanged.
- Unit tests for each discount strategy.
- Unit tests for each payment strategy, including crypto fee behavior.
- Unit tests for notification routing per customer type and for the WhatsApp extension.
- Unit tests for factory behavior.
- A regression test that confirms `PedEspecial` no longer violates the parent contract, or that the class has been removed.
- Static type checking in CI or local validation with `mypy --strict`.

## Documentation Deliverable

Produce a class diagram in either PlantUML or Mermaid that shows:

- domain entities
- repositories and interfaces
- strategies
- observers or pub-sub components
- factories
- service layer
- dependency direction

The diagram should make DIP visible by showing dependencies flowing toward abstractions.

## Recommended Implementation Order

1. Freeze the current behavior with tests and identify the interfaces needed for the new design.
2. Introduce discount and payment strategies.
3. Introduce notification observers or subscribers.
4. Add the order factory and move object creation behind it.
5. Replace direct concrete instantiation with explicit injection.
6. Remove or neutralize `PedEspecial` so LSP holds.
7. Add the three extensions as new classes only.
8. Tighten typing until `mypy --strict` passes.
9. Generate the UML diagram and tag the release.

## Final Validation Checklist

- `pytest` passes, including Golden Master coverage.
- `mypy --strict src/` passes.
- The UML diagram is checked into the repository.
- The three extensions are present and implemented only by addition.
- `git tag sprint-2` exists on the final commit.
