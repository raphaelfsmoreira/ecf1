# Sprint 2 Implementation Plan

## Objective

Refactor the order system to satisfy Sprint 2 requirements with OCP, DIP, and LSP while preserving the Golden Master behavior from the legacy system.

## Plan

### 1. Establish Core Contracts

Create abstraction points for the behaviors that will be replaced by polymorphism:

- discount strategies
- payment strategies
- notification observers and publishers

This step creates the foundation for dependency injection and keeps the rest of the refactor from depending on concrete classes.

Status: completed.

### 2. Move Business Rules Into Strategies

Implement concrete discount and payment strategies for the current behavior.

### 3. Introduce Observer-Based Notifications

Model email, SMS, manager notification, and future WhatsApp delivery as subscribers.

### 4. Add Order Factory and Application Service

Centralize order creation and compose the service layer from abstractions only.

### 5. Remove or Neutralize `PedEspecial`

Eliminate the fragile inheritance behavior or make it fully LSP-compliant.

### 6. Add the Three OCP Extensions

Implement crypto payment, WhatsApp notifications, and progressive volume discount by adding new classes only.

### 7. Tighten Validation and Delivery

Finish type hints, run `mypy --strict`, produce the UML diagram, and tag the final commit as `sprint-2`.
