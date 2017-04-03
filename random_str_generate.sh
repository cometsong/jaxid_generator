function random_str_generate() {
    # generate a random string of passed length, default 64 chars
    rand_length=${1:-64}
    cat /dev/urandom | tr -dc 'a-zA-Z0-9@#$%^&*()_+=-~<>?:{},./;[]' | fold -w ${rand_length} | head -n 1
}
random_str_generate "${@}"
