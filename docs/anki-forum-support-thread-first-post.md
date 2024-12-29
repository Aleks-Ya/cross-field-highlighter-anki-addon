Hello all, I'd introduce a new addon for language learners.

**Please, share your feedback in this topic.**

---

## Introduction

[Cross-Field Highlighter](https://ankiweb.net/shared/info/1312127886) takes word or collocation from the source field and highlights it in the destination fields for better readability:  
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/short-description-3.png)

---

## Features

[details="Highlight"]

1. CFH takes word from the source field and highlights it in the destination fields.
2. Supported formats: Bold, Italic, Underlined, Yellow Background.
3. Word endings can differ: e.g. source word `study` will be also highlighted in forms of `studies`, `studied`, `studying`, etc.
4. Collocations are supported: if the source field contains several words (collocation), all these words will be highlighted excluding stop words.
5. Stop words: given stop words will be excluded from the source field (e.g. stop words `a` from `a cat` will be treated as `cat`).
6. Case-insensitive: the source collocation can be in any case.
7. Non-space-delimited languages (Japanese, Chinese, Thai, etc.) are supported.
8. Idempotence: repeating highlighting the same notes doesn't duplicate highlighting.
9. HTML tags are skipped from highlighting.
10. Highlighting notes selected in Browser or current note in Editor.
11. Shortcut support ("Ctrl+Shift+H" by default)

[/details]

[details="Erase"]

1. CFH removes previously added highlightings from fields.
2. CFH marks its own formatting, so it can erase exactly only its formatting and preserve other formatting.
3. Erasing notes selected in Browser or current note in Editor.
4. Shortcut support (not set by default)

[/details]

[details="Show in Browser"]

1. Show all highlighted notes
2. Show notes modified by the latest run

[/details]

---

## Remarks

* Current version is tested mostly for English and little for Japanese. If it doesn't work correctly for your language, leave a comment.
* If you're going to use this addon, please consider rating it on [the addon page](https://ankiweb.net/shared/info/1312127886). It shows that it's worth continuing to improve it.

---

## Screenshots

[details="Browser menu"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/browser-menu.png)
[/details]

[details="Buttons in Editor"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/editor-buttons.png)
[/details]

[details="Highlight dialog"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/dialog-highlight.png)
[/details]

[details="Supported formats"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/formats.png)
[/details]

[details="Languages without spaces (Japanese, Chinese, Thai, etc.)"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/space-delimited-language.png)  
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/furigana.png)
[/details]

[details="Highlighting progress"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/progress-highlight.png)
[/details]

[details="Highlighting statistics"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/statistics-highlight.png)
[/details]

[details="Erase dialog (removes previously added highlighting)"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/dialog-erase.png)
[/details]

[details="Addon configuration"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/addon-configuration-open.png)
[/details]

[details="About addon"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/about-dialog-open.png)
[/details]

[details="Test cases"]
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/test-cases-open.png)
[/details]

---

## Links

- [Addon Page](https://ankiweb.net/shared/info/1312127886)
- [Support forum thread](https://forums.ankiweb.net/t/cross-field-highlighter-addon-support-page/52592)
- [GitHub](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon)
- [Changelog](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/blob/master/CHANGELOG.md)
- [SonarQube](https://sonarcloud.io/project/overview?id=Aleks-Ya_cross-field-highlighter-anki-addon)
- [Test cases](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/blob/master/docs/cases.md)

[![Unit-tests](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/actions/workflows/python-app.yml/badge.svg)](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/actions/workflows/python-app.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Aleks-Ya_cross-field-highlighter-anki-addon&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Aleks-Ya_cross-field-highlighter-anki-addon) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Aleks-Ya_cross-field-highlighter-anki-addon&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Aleks-Ya_cross-field-highlighter-anki-addon)
