#!/bin/bash

echo "Pushing to github ... "
COMMENT="Puttin shit in other shit"

git add -A .
git commit -m "$COMMENT"
git remote add origin https://github.com/stan-the-man/Serendipity.git
git remote -v
git push origin master


echo "Finished adding!" 
