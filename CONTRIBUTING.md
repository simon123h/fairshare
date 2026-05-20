# Contributing to FairShare

Thank you for your interest in contributing to FairShare! This document provides guidelines for setting up your development environment and contributing to the web application.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/fairshare.git
   cd fairshare
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Run development server:**
   ```bash
   npm run dev
   ```

## Quality Assurance

### Tests

We use **Vitest** for unit and component testing.

```bash
# Run tests once
npm test

# Run tests in watch mode
npm run test:watch # (If defined in package.json, otherwise vite test)
```

### Linting & Type Checking

We use **TypeScript** for type safety and **vue-tsc** for build-time validation.

```bash
# Run type checking
npm run build # (This runs vue-tsc)
```

## CI/CD Pipeline

The project uses **GitLab CI/CD** and **GitHub Actions**. Each push automatically triggers:

1. Type checking and linting.
2. Unit and component tests.
3. Production build verification.

Ensure all checks pass in your pull request.
