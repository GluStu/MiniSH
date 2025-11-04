import shlex, readline, glob , os

built_ins = ['exit', 'type', 'echo', 'pwd', 'cd', 'history', 'ai']


def parser(command):
    return shlex.split(command)

def list_path_commands():
    paths = os.environ.get("PATH", "").split(os.pathsep)
    cmds = set()
    for d in paths:
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            full = os.path.join(d, name)
            if os.access(full, os.X_OK) and not os.path.isdir(full):
                cmds.add(name)
    return cmds

_path_cmds = list_path_commands()

def shell_completer(text, state):
    buf    = readline.get_line_buffer()
    begidx = readline.get_begidx()
    options = []
    if begidx == 0:
        options += [cmd for cmd in built_ins if cmd.startswith(text)]
        options += [cmd for cmd in _path_cmds if cmd.startswith(text)]
        options = sorted(set(options))
        if state < len(options):
            if len(options) == 1:
                return options[0] + ' '
            else:
                return options[state]
        return None

    else:
        matches = glob.glob(text + '*')
        matches.sort()
        matches = [
            m + ('/' if os.path.isdir(m) else ' ')
            for m in matches
        ]
        return matches[state] if state < len(matches) else None