# -*- coding: utf8 -*-
__author__ = 'te@nexttuesday.de'
"""

 )¯¯`'¯¸¯¯`,)¯¯|)¯¯)'‚/¯¯|\¯¯¯\')¯¯`'¯¸¯¯`,   ___   )¯¯ )'     )¯¯ )'         ___   )¯¯|)¯¯)'‚
(____)–-·´'(__(\ ¯¯¯(°\__'\|__/(____)–-·´'|¯¯(\__('(___(¸.––-,(___(¸.––-,°|¯¯(\__('(__(\ ¯¯¯(°
       °        ¯¯¯¯                    ° |__(/¯¯¯(‘      ¯¯¯        ¯¯¯  |__(/¯¯¯(‘     ¯¯¯¯
              '‚                        '‚    ¯¯¯¯'‘                          ¯¯¯¯'‘

Copyright (c) 2013, Thomas Einsporn
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
import locale
from time import time
from random import randint

"""
from http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
"""
def import_class(cl):
    d = cl.rfind(".")
    classname = cl[d+1:len(cl)]
    m = __import__(cl[0:d], globals(), locals(), [classname])
    return getattr(m, classname)

class propeller:

    style = None
    outlen = 0
    stylelen = 0
    outputts = 0
    interval = 0
    terminal = True
    encoding = ""
    finished = False

    def __init__(self, style="styles.spinner.Classic", updateinterval=300, *args, **kw):
        """
        instantiate style
        """
        styleClass = import_class(style)
        style = styleClass(*args, **kw)

        self.style = style
        self.interval = updateinterval

        if sys.stdout.isatty():
            self.encoding = sys.stdout.encoding
        else:
            self.terminal = False
            self.encoding = locale.getpreferredencoding()

    def update(self, userstring="", current=0, maximum=1):
        """
        early exit depending on updateinterval
        back paddle the amount of chars from previous output
        pass user string and get output from style
        """
        if self.terminal:
            if not (time() - self.outputts) * 1000 > self.interval:
                return
            sys.stdout.write('\b' * self.outlen)
            styleout = self.style.output(userstring=userstring, current=current, maximum=maximum)
            self.stylelen = len(styleout)
            output = userstring + styleout
            self.sysout(output)
            self.outputts = time()
        elif not self.finished:
            self.sysout(userstring)
            self.finished = True

    def end(self, output=None):
        """
        get last and final output from style
        output new line
        """
        if self.terminal:
            sys.stdout.write('\b' * self.stylelen)
        output = self.style.output(endstring=output, final=True)
        self.sysout(output)
        self.sysnl()

    def sysout(self, output):
        """
        print output
        """
        sys.stdout.write(output)
        sys.stdout.flush()
        self.outlen = len(output)

    def sysnl(self):
        """
        output new line
        """
        sys.stdout.write("\n")
        sys.stdout.flush()

def main(argv):
    from time import sleep

    """
    Simple spinner
    """
    p = propeller()
    for i in xrange(1, randint(10, 100)):
         p.update("Spinning classic %i " % i)
         sleep(0.1)
    p.end("done")

    """
    Simple spinner with brackets, limit output frequency
    """
    p = propeller(style="styles.spinner.Classic", brackets=True, spinner=1, updateinterval=50)
    for i in xrange(1, randint(10, 100)):
        p.update("fast spinning classic with brackets %i " % i)
        sleep(0.1)
    p.end("ok")

    """
    Phenox
    """
    for s in range(0, 7):
        p = propeller(style="styles.spinner.Phenox", spinner=s, updateinterval=50)
        for i in xrange(1, randint(10, 200)):
            p.update("pnx %i " % i)
            sleep(0.1)
        p.end("ok")

    """
    Simple progess bar
    """
    p = propeller(style="styles.progress.ClassicProgress", width=50)
    maximum = 10
    for i in xrange(1, maximum + 1):
        p.update("Classic progress brackets %i " % i, current=i, maximum=maximum)
        if i > maximum - 5:
            break
        sleep(0.1)
    p.end("failed")

    """
    Simple progess bar with percentage shown
    """
    p = propeller(style="styles.progress.ClassicProgress", width=50, showpercentage=True)
    maximum = 10
    for i in xrange(1, maximum + 1):
        p.update("Classic progress brackets and % ", current=i, maximum=maximum)
        sleep(0.1)
    p.end("done")

    """
    Simple spinners UTF8
    """
    for s in range(0, 1):
        p = propeller(style="styles.spinner.ClassicUTF8", updateinterval=50)
        for i in xrange(1, 100):
            p.update("Spinning UTF8 %i " % i)
            sleep(0.1)
        p.end("done")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
