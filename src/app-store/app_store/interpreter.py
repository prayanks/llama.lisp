import secrets
import bcrypt

try:
    from catalog import latest_version
except ImportError:
    from app_store.catalog import latest_version

chosen_versions = {}


def _is_list(sexp):
    return isinstance(sexp, list)


def interactive_input(prompt, docs=""):
    print("==> Entering interactive input")
    print(docs)
    inp = input(f"==> {prompt}: ").strip()
    print(f"==> recieved {inp} for {prompt}")
    return inp


def choose_version(app_name, default_version):
    if app_name in chosen_versions:
        return chosen_versions[app_name]

    latest = latest_version(app_name)
    if latest:
        prompt = f"==> Version for {app_name} [default: {default_version}, latest: {latest}]: "
    else:
        prompt = f"==> Version for {app_name} [default: {default_version}, latest: unknown]: "

    inp = input(prompt).strip()
    if inp == "":
        inp = default_version

    chosen_versions[app_name] = inp
    return inp


def hash_password(password):
    # https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/
    bytes = password.encode()
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash.decode()


def str_format(fstring, *args):
    return fstring.format(*args)


def strip_prefix(value, prefix):
    if value.startswith(prefix):
        return value[len(prefix) :]
    return value


def gen_password(length=16):
    return secrets.token_urlsafe(length)


standard_lib = {
    "choose-version": choose_version,
    "gen-password": gen_password,
    "hash-password": hash_password,
    "interactive-input": interactive_input,
    "format": str_format,
    "strip-prefix": strip_prefix,
    "gen-password-hex32": lambda: secrets.token_bytes(32).hex(),
}


def config_lisp(sexp, env=standard_lib):
    if _is_list(sexp):
        if len(sexp) > 0 and sexp[0] == "let":
            assert len(sexp) == 3
            varialbes = sexp[1]
            body = sexp[2]
            for var_name, var_value in varialbes:
                assert isinstance(var_name, str)
                env[var_name] = config_lisp(var_value, env)

            return config_lisp(body, env)
        elif len(sexp) > 0 and sexp[0] == "unquote":
            quoted_sexp = sexp[1]
            if _is_list(quoted_sexp):
                # function
                fn_name = quoted_sexp[0]
                args = config_lisp(quoted_sexp[1:], env)
                return env[fn_name](*args)
            else:
                # variable
                return env[quoted_sexp]
        else:
            return [config_lisp(x, env) for x in sexp]
    else:
        # atom
        return sexp


if __name__ == "__main__":
    import sys
    from parser import parse_sexp

    print(config_lisp(parse_sexp(open(sys.argv[-1]).read())))
