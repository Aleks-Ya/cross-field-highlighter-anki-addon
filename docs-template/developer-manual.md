# Developer manual

**Table of content**

<!--TOC-->

---

## Setup Python virtual environment

1. Install Tox:
    1. Install PIPX: `pip install pipx`
    2. Install Tox: `pipx install tox`
2. Install PyEnv: `brew install pyenv pyenv-virtualenv`
3. Create virtual environment:
    1. `pyenv install 3.9.18`
    2. `pyenv virtualenv 3.9.18 cross-field-highlighter-anki-addon`
4. Install Anki packages
    1. Activate virtual environment: `pyenv activate cross-field-highlighter-anki-addon`
    2. Install packages: `pip install -U pip -r requirements/anki-qt6-current.txt -r requirements/dev.txt -r requirements/tests.txt`

## Tests

Run automated tests:

1. Prerequisites: [Setup Python virtual environment](#setup-python-virtual-environment)
2. Activate virtual environment: `pyenv cross-field-highlighter-anki-addon`
3. Run tests:
    1. Unit tests (without integration tests): `tox`
    2. Integration tests: `tox -- tests -m integration`
    3. Unit tests for given environment: `tox -e anki-qt6-earliest`

Make UI visible during tests:  
File `conftest.py`, fixture `visual_qtbot`, set positive delay: `VisualQtBot(qtbot, 1000)`

## SonarQube

Report at [SonarCloud](https://sonarcloud.io/project/overview?id=Aleks-Ya_cross-field-highlighter-anki-addon)

Scan locally:

1. Prepare once
    1. Install Sonar Scanner: `brew install sonar-scanner`
    2. Find config file `sonar-scanner.properties`: `sonar-scanner -v`
    3. Add token to `sonar-scanner.properties`: `sonar.token=XXX`
2. Execute
    1. Generate coverage report: `tox`
    2. Run Scanner: `sonar-scanner`
    3. See report at https://sonarcloud.io/project/overview?id=Aleks-Ya_cross-field-highlighter-anki-addon

## Local deploy

Run: `./deploy_locally.sh ~/.local/share/Anki2/addons21/cross_field_highlighter`

## Build

1. Build ZIP: `./build_dist.sh` (includes unit-tests)
2. Output: `./dist/note-size-X.X-X.zip`

## Execute GitHub Actions locally

1. Install `act`: `brew install act`
2. Run: `act`

## Render documentation

1. Install: `pip install md-toc`
2. Edit documentation in `docs-template` folder
3. Update documentation: `./render_docs.sh`
4. Output docs: `docs` folder
5. Commit `docs` folder

## Release

1. Update `CHANGELOG.md` manually
2. Update documentation: `./render_docs.sh`
3. CI:
    1. Push: `git push`
    2. Check GitHub actions: https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/actions
    3. Check SonarQube warnings: https://sonarcloud.io/project/overview?id=Aleks-Ya_cross-field-highlighter-anki-addon
4. Increment version:
    1. Major: `bump-my-version bump major -v`
    2. Minor: `bump-my-version bump minor -v`
    3. Patch: `bump-my-version bump patch -v`
5. Build ZIP: `./build_dist.sh`
    1. Install and test on the earliest Anki version (Qt5)
    2. Install and test on the current Anki version (Qt6)
6. Upload ZIP to the Addon page:
    1. Page: https://ankiweb.net/shared/info/1312127886
    2. Title: `🎨 Cross-Field Highlighter - spotlight word in text`
    3. Tags: -
    4. Support page: https://forums.ankiweb.net/t/cross-field-highlighter-addon-spotlight-word-in-text-support-thread
    5. Attach the distribution file
    6. Update `Description` from `docs-template/addon-info-description.md`
7. Push Git branch and tags: `git push --follow-tags`
8. Create a GitHub release from tag
9. Notify support thread:
    1. URL: https://forums.ankiweb.net/t/cross-field-highlighter-addon-spotlight-word-in-text-support-thread/52592
    2. Update the 1st post from `anki-forum-support-thread-first-post.md`
    3. Add post about new version

## Icons

Highlight Editor button: https://icon-icons.com/icon/highlight/96729
Erase Editor button: https://icon-icons.com/icon/rubber/96712
Select all: https://icon-icons.com/icon/select-all-on-regular/204978
Select none: https://icon-icons.com/icon/select-all-off-regular/204236
