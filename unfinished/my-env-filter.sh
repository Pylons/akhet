# This was the script I used to fix the author name/email after converting the
# repository from Mercurial to Git.
# It's in the 'unfinished' directory because there's no better place for it,
# but it works.

an="$GIT_AUTHOR_NAME"
am="$GIT_AUTHOR_EMAIL"
cn="$GIT_COMMITTER_NAME"
cm="$GIT_COMMITTER_EMAIL"

if [ "$GIT_AUTHOR_NAME" = "sluggoster" ]
then
    cn="Mike Orr"
    cm="sluggoster@gmail.com"
    an="Mike Orr"
    am="sluggoster@gmail.com"
fi

export GIT_AUTHOR_NAME="$an"
export GIT_AUTHOR_EMAIL="$am"
export GIT_COMMITTER_NAME="$cn"
export GIT_COMMITTER_EMAIL="$cm"
