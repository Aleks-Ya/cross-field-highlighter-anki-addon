# Developer manual

**Table of content**

<!--TOC-->

- [Setup Python virtual environment](#setup-python-virtual-environment)
- [Tests](#tests)
- [SonarQube](#sonarqube)
- [Local deploy](#local-deploy)
- [Build](#build)
- [Execute GitHub Actions locally](#execute-github-actions-locally)
- [Render documentation](#render-documentation)
- [Release](#release)
- [Icons](#icons)

<!--TOC-->

---

## Setup Python virtual environment

1. Install Tox:
    1. Install PIPX: `pip install pipx`
    2. Install Tox: `pipx install tox`
2. Install PyEnv:
    1. Install PyEnv: `brew install pyenv`
    2. Install VirtualEnv: `brew install pyenv-virtualenv`
3. Create virtual environment:
    1. `pyenv install 3.9.18`
    2. `pyenv virtualenv 3.9.18 cross-field-highlighter-anki-addon`
4. Install Anki packages
    1. Activate virtual environment: `pyenv activate cross-field-highlighter-anki-addon`
    2. Install packages: `pip install -r requirements.txt`

## Tests

Run automated tests:

1. Prerequisites: [Setup Python virtual environment](#setup-python-virtual-environment)
2. Activate virtual environment: `pyenv cross-field-highlighter-anki-addon`
3. Run unit-tests: `tox`

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

1. Build ZIP: `python setup.py dist` (includes unit-tests)
2. Output: `./dist/note-size-X.X-X.zip`

## Execute GitHub Actions locally

1. Install `act`: `brew install act`
2. Run: `act`

## Render documentation

1. Install: `pip install md-toc`
2. Edit documentation in `docs-template` folder
3. Update documentation: `./docs_render.sh`
4. Output docs: `docs` folder
5. Commit `docs` folder

## Release

1. Update `CHANGELOG.md` manually
2. Update documentation: `./docs_render.sh`
3. Check SonarQube warnings: https://sonarcloud.io/project/overview?id=Aleks-Ya_cross-field-highlighter-anki-addon
4. Increment version:
    1. Major: `bump-my-version bump major`
    2. Minor: `bump-my-version bump minor`
    3. Patch: `bump-my-version bump patch`
5. Build ZIP: `python setup.py dist`
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
   https://forums.ankiweb.net/t/cross-field-highlighter-addon-spotlight-word-in-text-support-thread/52592

## Icons

Highlight Editor button: https://icon-icons.com/icon/highlight/96729
Erase Editor button: https://icon-icons.com/icon/rubber/96712
