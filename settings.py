from ast import literal_eval
from sys import stderr, exit
from keyword import kwlist
from pathlib import Path


def _error(file_name, line, line_text, text):
    stderr.write("配置文件错误：\n"
                 f'  文件 "{Path(file_name).resolve()}", 第{line}行\n'
                 f'    {line_text}\n'
                 + text)
    exit(-1)


class _Settings:
    def __init__(self):
        setting_file_name = ".options"
        with open(setting_file_name, "rb") as f:
            first_line = f.readline().strip()
            if first_line.startswith(b"!encoding="):
                encoding = first_line[10:].decode("ascii")
            else:
                encoding = "utf-8"
        with open(setting_file_name, encoding=encoding) as f:
            this_value = ""
            for n, line in enumerate(f):
                line = line.strip()
                if this_value:
                    if line == "\\":
                        try:
                            self.__dict__[key] = literal_eval(this_value)
                        except:
                            self.__dict__[key] = this_value
                        this_value = ""
                        continue
                    this_value += line + "\n"
                    continue
                if line.startswith("#"):
                    continue
                elif line.startswith("!"):
                    continue
                elif "=" in line:
                    key, value = [s.strip() for s in line.split("=", 1)]
                    if key.isidentifier() and key not in kwlist:
                        if value == "\\":
                            this_value = " "
                            continue
                        try:
                            self.__dict__[key] = literal_eval(value)
                        except:
                            self.__dict__[key] = value
                    else:
                        _error(
                            Path(setting_file_name).resolve(),
                            n + 1,
                            line,
                            f'标识符错误："{key}" 不是合法的标识符。\n'
                        )
                elif line:
                    _error(
                        Path(setting_file_name).resolve(),
                        n + 1,
                        line,
                        f'格式错误：应为 "<标识符名称>=<值>"。\n'
                    )


settings = _Settings()
