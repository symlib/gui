# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time
def tolog(strinfo):
        if strinfo!="'result': 'p'" or strinfo!="'result': 'f'":
            with open("./cli_scripts.log", "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write(time.strftime('%Y-%m-%d %H:%M:%S',
                                      time.localtime(time.time())) + ": " + strinfo + '\n' + content)

                f.close()
            print(strinfo)
        # for testlink steps populate
        fout=open("./testlink.notes","a")
        fout.write(strinfo+ '\n')

        fout.close()

if __name__ == "__main__":
    tolog("abcdefg")


