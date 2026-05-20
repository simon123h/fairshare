# Architecture of FairShare Web

This document describes the high-level architecture and project structure of the FairShare web application.

## Project Structure (under `src/`)

- **`components/`**: Reusable Vue components (BalanceTable, ExpenseForm, etc.).
- **`composables/`**: Shared logic using Vue's Composition API (e.g., `useI18n.ts`, `useProjects.ts`).
- **`models/`**: TypeScript interfaces and classes defining the domain data (e.g., `Expense.ts`, `Ledger.ts`).
- **`locales/`**: JSON files containing translations for various languages.
- **`views/`**: Top-level page components (HomeView, ProjectView).
- **`router/`**: Vue Router configuration.
- **`styles/`**: Global CSS variables and base styles.

## Design Principles

- **Component-Based UI:** The interface is built from small, focused components for maintainability.
- **Composition over Inheritance:** Logical concerns are extracted into composables.
- **Strong Typing:** TypeScript is used throughout to ensure data consistency and prevent runtime errors.
- **i18n First:** All user-facing strings are managed through `vue-i18n` with support for multiple languages.

## Data Flow

The application uses a reactive state management approach. Local projects and expenses are managed through composables that handle calculation logic and persistence (currently in-memory/local).
