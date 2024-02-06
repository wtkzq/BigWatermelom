from ast import literal_eval
from sys import stderr, exit
from keyword import kwlist
from pathlib import Path


class _Settings:
    def __init__(self):
        setting_file_name = ".options"
        with open(setting_file_name) as f:
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
                        stderr.write("配置文件错误：\n"
                                     f'  文件 "{Path(setting_file_name).resolve()}", 第{n + 1}行\n'
                                     f'    {f.name}\n'
                                     f'标识符错误："{key}" 不是合法的标识符。\n')
                        exit(-1)
                elif line:
                    stderr.write("配置文件错误：\n"
                                 f'  文件 "{Path(setting_file_name).resolve()}", 第{n + 1}行\n'
                                 f'    {line}\n'
                                 f'格式错误：应为 "<标识符名称>=<值>"。\n')
                    exit(-1)


settings = _Settings()
