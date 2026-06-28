# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running Tests
```bash
# Run all tests (current Anki version)
tox -e anki-current

# Run all test environments
tox

# Run a specific test file
tox -e anki-current -- tests/highlighter/text/test_regex_text_highlighter.py

# Run a single test by name
tox -e anki-current -- tests/highlighter/text/test_regex_text_highlighter.py::TestClass::test_method

# Run integration tests only
tox -e anki-current -- tests -m integration
```

### Build & Distribution
```bash
./build_dist.sh          # Produces dist/cross-field-highlighter-X.X.X.ankiaddon
./deploy_locally.sh ~/.local/share/Anki2/addons21/cross_field_highlighter
./render_docs.sh         # Renders docs/ from docs-template/
```

### Version Bumping
```bash
bump-my-version bump patch -v   # or minor / major
```

### Test Environments
- `anki-current` — latest stable Anki (defined in `requirements/anki-current.txt`)
- `anki-earliest` — oldest supported Anki
- `anki-beta` — beta Anki

Tests run headless via `QT_QPA_PLATFORM=offscreen`.

### Pytest Markers
- `@pytest.mark.performance` — performance tests
- `@pytest.mark.integration` — integration tests
- `@pytest.mark.skip_for_beta` / `skip_for_current` / `skip_for_earliest` — version-conditional skips

## Dependencies

All dependency versions are dictated by the current Anki version — do not introduce Dependabot or any automated dependency updates. Version pins in `requirements/` must stay in sync with what Anki ships.

## Architecture

### Entry Point
`cross_field_highlighter/__init__.py` registers two Anki hooks:
1. `collection_did_load` → captures collection reference via `CollectionHolder`
2. `profile_did_open` → triggers full addon initialization (lazy; everything boots here)

### Component Map

```
cross_field_highlighter/
├── config/          # Config load/save, user prefs, shortcuts, change listeners
├── highlighter/     # Core highlighting engine (no Anki/Qt dependencies)
│   ├── formatter/   # Wraps words in HTML: bold, italic, underline, <mark>
│   ├── language/    # Detects CJK vs space-delimited text
│   ├── tokenizer/   # Splits text into tokens; handles stop-word removal
│   ├── token/       # Matching strategies: start-with vs find-and-replace
│   ├── text/        # Highlights a single text string
│   ├── note/        # Highlights a single Anki note field
│   └── notes/       # Batch-highlights multiple notes with progress tracking
├── ui/              # All Anki/Qt-dependent code
│   ├── dialog/adhoc/  # Highlight and Erase dialog windows (MVC pattern)
│   ├── editor/      # Adds buttons to the card editor
│   ├── browser/     # Hooks into the card browser window
│   ├── menu/        # Context menu actions (highlight, erase, about)
│   ├── operation/   # HighlightOp / EraseOp with statistics reporting
│   └── widgets/     # Reusable Qt widgets (combo boxes, line edits)
└── common/          # CollectionHolder singleton
```

### Highlight Data Flow
User triggers action → Dialog collects params → `OpFactory` creates `HighlightOp` → `NotesHighlighter.highlight()` → `FieldHighlighter` → `RegexTextHighlighter` → tokenize → match → wrap in HTML tags → update note.

### Key Design Decisions
- **Strict layering**: `highlighter/` has zero Anki/Qt imports; `ui/` owns all framework coupling.
- **Constructor injection throughout**: fixtures in `tests/conftest.py` wire up the full graph.
- **Strategies for token matching**: `StartWithTokenHighlighter` vs `FindAndReplaceTokenHighlighter` are swapped based on language detection.
- **MVC dialogs**: each ad-hoc dialog has a separate model, view, and controller.
- **Type aliases** (`FieldName`, `Word`, etc.) defined in `highlighter/types.py` — use them for domain concepts.

### Configuration
Default config lives in `cross_field_highlighter/config.json`. User overrides are persisted to Anki's addon user_files directory via `UserFilesStorage`.

### Testing Conventions
- All fixtures are in `tests/conftest.py` (555+ lines) — check there before creating new ones.
- `tests/data.py` provides test data factories.
- `tests/visual_qtbot.py` wraps `pytest-qt` for dialog/widget tests.
- Dialog tests follow a view + controller pair pattern matching the production MVC structure.
