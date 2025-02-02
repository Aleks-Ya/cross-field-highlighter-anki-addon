set -e

if [ "$(ls -A docs)" ]; then
   rm -r docs/*
fi

rsync -a --exclude='images-krita' --exclude='uml' --exclude='pencil' docs-template/ docs/

files_with_toc=("README.md" "developer-manual.md" "addon-info-description.md")
for file in "${files_with_toc[@]}"; do
  md_toc -p -s 1 github docs/$file
done

cp docs/README.md README.md

tox -- tests tests/highlighter/render_cases_page_test.py
