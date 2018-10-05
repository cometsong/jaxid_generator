# deploy merges changes from devel repo

development_branch=${1:-devel}
production_branch=${2:-deploy}
development_repo=${3:-development}
with_submodules=${4:-nosubs}

if [[ "${with_submodules}" -eq "nosubs" ]]; then
   with_submodules='';
else
   with_submodules='--recurse-submodules';
fi

git checkout ${production_branch} && \
    git pull \
    --verbose --no-edit --tags ${with_submodules} \
    ${development_repo} ${development_branch}

