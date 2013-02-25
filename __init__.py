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


class Style(object):

    spinner_pos = 0
    progress_width = 0
    current = 0
    maximum = 0

    def update_spinner(self):
        """
        update spinner position
        """
        spinner_pos = self.spinner_pos + 1
        if spinner_pos >= len(self.spinner):
            spinner_pos = 0
        self.spinner_pos = spinner_pos

    def update_progress(self, current, maximum):
        """
        calculate progress bar position based on current, maximum value and progress bar maxwidth
        """
        if not maximum > 0:
            maximum = self.maximum
        if current > self.current:
            self.current = current

        if maximum > 0:
            percent = self.current * 100.0 / maximum
            self.percent = percent
            self.progress_width = int(percent / 100.0 * self.progress_maxwidth)
            self.maximum = maximum

    def output(self, current=0, maximum=0, *args, **kw):
        """
        update positions and get styled output
        """
        if hasattr(self, 'spinner_width'):
            self.update_spinner()
        if hasattr(self, 'progress_maxwidth'):
            self.update_progress(current, maximum)
        output = self._output(*args, **kw)
        return output


class Classic(Style):
    spinner_prefix = '['
    spinner_suffix = ']'
    spinner_width = 1

    spinners = ['-\|/', '.o0O0o']

    def __init__(self, brackets=False, spinner=0):
        self.brackets = brackets
        self.spinner = self.spinners[spinner]
        super(Classic, self).__init__()

    def _output(self, final=False, endstring=None, *args, **kw):
        if final:
            output = endstring
        else:
            output = self.spinner[self.spinner_pos]

        if self.brackets:
            output = self.spinner_prefix + output + self.spinner_suffix

        return output

class ClassicUTF8(Style):
    spinner_prefix = '['
    spinner_suffix = ']'
    spinner_width = 1

    spinners = [u"□▣", u"◐◓◑◒", u"◜◝◞◟", u"◢◣◤◥", u"◴◷◶◵", u"☠ "]

    def __init__(self, brackets=False, spinner=0):
        self.brackets = brackets
        if spinner == 0:
            spinner = randint(0, len(self.spinners)-1)
        self.spinner = self.spinners[spinner]
        super(ClassicUTF8, self).__init__()

    def _output(self, final=False, endstring=None, *args, **kw):
        if final:
            output = endstring
        else:
            output = self.spinner[self.spinner_pos]

        if (self.brackets):
            output = self.spinner_prefix + output + self.spinner_suffix

        return output

class ClassicProgress(Style):

    progress_maxwidth = 0
    progress_prefix = '['
    progress_suffix = '] '
    progress_empty = '~'
    progress_check = '#'
    showpcnt = False
    lastoutput = 0

    def __init__(self, width=10, showpercentage=False, *args, **kw):
        self.progress_maxwidth = width
        self.showpcnt = showpercentage
        super(ClassicProgress, self).__init__(*args, **kw)

    def _output(self, final=False, endstring=None, *args, **kw):
        empty = "%s" % (self.progress_empty * self.progress_maxwidth)
        filler = empty[self.progress_width:self.progress_maxwidth]
        output = self.progress_prefix + "%s" % (self.progress_check * self.progress_width) + filler + self.progress_suffix

        if self.showpcnt:
            output = output + str(self.percent) + "% "

        if final and endstring is not None:
            output = output + endstring

        return output


class propeller:

    style = None
    outlen = 0
    stylelen = 0
    outputts = 0
    interval = 0
    terminal = True
    encoding = ""
    finished = False

    def __init__(self, style=None, updateinterval=300):
        """
        init style if none set
        """
        if style is None:
            style = Classic()

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
    classic_style = Classic(brackets=True, spinner=1)
    p = propeller(style=classic_style, updateinterval=50)
    for i in xrange(1, randint(10, 200)):
        p.update("fast spinning classic with brackets %i " % i)
        sleep(0.1)
    p.end("ok")

    """
    Simple progess bar
    """
    progress_style = ClassicProgress(width=50)
    p = propeller(style=progress_style)
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
    progress_style = ClassicProgress(width=50, showpercentage=True)
    p = propeller(style=progress_style)
    maximum = 10
    for i in xrange(1, maximum + 1):
        p.update("Classic progress brackets and % ", current=i, maximum=maximum)
        sleep(0.1)
    p.end("done")

    """
    Simple spinners UTF8
    """
    for s in range(0, 1):
        classic_style = ClassicUTF8()
        p = propeller(style=classic_style, updateinterval=50)
        for i in xrange(1, 100):
            p.update("Spinning UTF8 %i " % i)
            sleep(0.1)
        p.end("done")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
