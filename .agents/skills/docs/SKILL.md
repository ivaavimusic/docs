```markdown
# docs Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development patterns and conventions used in the `docs` repository, a TypeScript codebase with a focus on documentation-related tooling. You'll learn about file naming, import/export styles, commit message conventions, and how to write and run tests. While no specific workflows or frameworks are detected, this guide provides best practices and suggested commands to streamline your development process.

## Coding Conventions

### File Naming
- Use **camelCase** for all file names.
  - Example: `myComponent.ts`, `userGuide.ts`

### Import Style
- Use **relative imports** for modules within the repository.
  - Example:
    ```typescript
    import { helperFunction } from './utils/helperFunction';
    ```

### Export Style
- Use **named exports** for all modules.
  - Example:
    ```typescript
    // In utils/helperFunction.ts
    export function helperFunction() { ... }

    // In another file
    import { helperFunction } from './utils/helperFunction';
    ```

### Commit Message Convention
- Follow the **Conventional Commits** standard.
- Use the `docs:` prefix for documentation-related changes.
  - Example:
    ```
    docs: update API usage examples in README
    ```

## Workflows

### Creating a Documentation Update
**Trigger:** When you need to update or add documentation.
**Command:** `/update-docs`

1. Create or update documentation files using camelCase naming.
2. Use relative imports if including code snippets or utilities.
3. Commit your changes with a message like:
    ```
    docs: add section on usage patterns
    ```
4. Open a pull request for review.

### Writing and Running Tests
**Trigger:** When adding new features or updating existing code.
**Command:** `/run-tests`

1. Create a test file named with the pattern `*.test.*` (e.g., `myComponent.test.ts`).
2. Write tests using your preferred framework (not specified).
3. Run the tests using the appropriate command for your test runner.
4. Ensure all tests pass before committing.

## Testing Patterns

- Test files follow the `*.test.*` naming convention.
  - Example: `helperFunction.test.ts`
- The testing framework is not specified; use the one preferred by your team.
- Place test files alongside the code they test or in a dedicated `tests` directory.

## Commands
| Command        | Purpose                                         |
|----------------|-------------------------------------------------|
| /update-docs   | Start a documentation update workflow           |
| /run-tests     | Run all tests in the repository                 |

```