# deploy merges changes from devel repo
git checkout deploy && \
    git pull \
    --verbose --no-edit --tags \
    development devel

# leave submod versions static    #--recurse-submodules  \
