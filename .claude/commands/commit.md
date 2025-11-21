# Claude Command: Commit

This command helps you create well-formatted commits with conventional commit messages and emoji.

## Usage

To create a commit, just type:
```
/commit
```

## What This Command Does

1. Checks which files are staged with `git status`
2. If no files are staged, automatically adds all modified and new files with `git add`
3. Performs a `git diff` to understand what changes are being committed
4. Analyzes the diff to determine if multiple distinct logical changes are present
5. If multiple distinct changes are detected, suggests breaking the commit into multiple smaller commits
6. For each commit (or the single commit if not split), creates a commit message using emoji conventional commit format

## Best Practices for Commits

- **Atomic commits**: Each commit should contain related changes that serve a single purpose
- **Split large changes**: If changes touch multiple concerns, split them into separate commits
- **Conventional commit format**: Use the format `emoji <type>: <description>`
- **Present tense, imperative mood**: Write commit messages as commands (e.g., "add feature" not "added feature")
- **Concise first line**: Keep the first line under 72 characters
- **No Claude attribution**: NEVER mention Claude or Claude Code in commit messages

## Commit Types and Emojis

Use ONE emoji per commit based on the primary type of change:

- ✨ `feat`: New feature or functionality
- 🐛 `fix`: Bug fix (non-critical)
- 🚑️ `fix`: Critical hotfix
- 📝 `docs`: Documentation changes
- 🎨 `style`: Code structure/formatting improvements
- ♻️ `refactor`: Code refactoring (no behavior change)
- 🚚 `refactor`: Move or rename files/resources
- ⚡️ `perf`: Performance improvements
- ✅ `test`: Add or update tests
- 🔧 `chore`: Configuration, tooling, maintenance
- 🔥 `chore`: Remove code or files
- 📦️ `chore`: Update dependencies or packages
- ➕ `chore`: Add a dependency
- ➖ `chore`: Remove a dependency
- 🚀 `ci`: CI/CD changes
- 💚 `fix`: Fix CI build
- 🔒️ `fix`: Security fixes
- ♿️ `feat`: Accessibility improvements
- 🗃️ `chore`: Database migrations or schema changes
- 🌐 `feat`: Internationalization/localization changes

## Guidelines for Splitting Commits

When analyzing the diff, consider splitting commits based on these criteria:

1. **Different concerns**: Changes to unrelated parts of the codebase
2. **Different types of changes**: Mixing features, fixes, refactoring, etc.
3. **File patterns**: Changes to different types of files (e.g., source code vs documentation)
4. **Logical grouping**: Changes that would be easier to understand or review separately
5. **Size**: Very large changes that would be clearer if broken down

## Examples

**Good commit messages for this Django/Wagtail project:**
- ✨ feat: add speaker bio field to Speaker model
- ✨ feat: implement new StreamField block for video embeds
- 🐛 fix: correct sponsor logo display on homepage
- 🐛 fix: resolve meetup sync timezone issue
- 📝 docs: update CLAUDE.md with new task commands
- ♻️ refactor: simplify SpeakersPage queryset logic
- ♻️ refactor: extract common page mixins to core app
- 🎨 style: improve Wagtail admin panel layout
- 🔥 chore: remove deprecated Meetup API v2 code
- 📦️ chore: update Wagtail to 6.2.x
- 📦️ chore: upgrade Django to 5.0.14
- ➕ chore: add django-extensions for development
- ➖ chore: remove unused celery dependency
- 🚀 ci: update Heroku deployment configuration
- 💚 fix: resolve failing Docker build
- 🔒️ fix: patch Django security vulnerability
- ♿️ feat: improve navigation accessibility for screen readers
- 🗃️ chore: add migration for new Session fields
- 🌐 feat: add French translation for sponsor pages

**Example of splitting commits:**

If you modify both a Wagtail page model AND update a management command, split into:
1. ✨ feat: add session_type field to Session model
2. ♻️ refactor: update import-sessionize command to handle new field

If you fix multiple unrelated issues, split into:
1. 🐛 fix: correct speaker ordering on TalksPage
2. 🐛 fix: resolve Redis connection timeout in dev settings
3. 🗃️ chore: add missing migration for sponsors app

## Important Notes

- If specific files are already staged, the command will only commit those files
- If no files are staged, it will automatically stage all modified and new files
- The commit message will be constructed based on the changes detected
- Before committing, the command will review the diff to identify if multiple commits would be more appropriate
- If suggesting multiple commits, it will help you stage and commit the changes separately
- **CRITICAL**: Never add "Generated with Claude Code" or similar attributions to commits
