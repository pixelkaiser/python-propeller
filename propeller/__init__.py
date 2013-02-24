__author__ = 'te'
"""
"""

import sys

class style(object):

    spinner_pos = 0

    def __init__(self):
        self.width = len(self.spinner_prefix + self.spinner_suffix) + self.spinner_width

    def update_spinner(self):
        spinner_pos = self.spinner_pos + 1
        if (spinner_pos >= len(self.spinner)):
            spinner_pos = 0
        self.spinner_pos = spinner_pos

    def update_progress(self, percent = 0):
        self.progress_width = int(percent / 100.0 * self.progress_width)

    def output(self, *args, **kw):
        self.update_spinner()
        return self._output(*args, **kw)

class classic(style):
    spinner_prefix = '['
    spinner_suffix = ']'
    spinner = '-\|/'
    spinner_width = 1

    def __init__(self, brackets = False):
        self.brackets = brackets
        super(classic, self).__init__()

    def _output(self, *args, **kw):
        output = self.spinner[self.spinner_pos]

        if (self.brackets):
            output = self.spinner_prefix + output + self.spinner_suffix
        return output

class classicprogress(style):

    progress_maxwidth = 0
    progress_prefix = '['
    progress_suffix = ']'
    progress_empty = '~'
    progress_check = '#'

    def __init__(self, width = 10):
        self.progress_width = width
        super(classic, self).__init__()

    def _output(self, *args, **kw):
        return ""

class propeller:

    style = None
    outlen = 0

    def __init__(self, updateIntervall = 100, style = None):
        if (style is None):
            style = classic()

        self.style = style

    def update(self, userstring = "", percent = 0):
        sysout('\b' * self.outlen)

        output = userstring + self.style.output(userstring = userstring, percent = percent)
        sysout(output)

        self.outlen = len(output)

    def end(self):
        sysout("\n")

def sysout(output):
    sys.stdout.write (output)
    sys.stdout.flush()

def percentize(steps):
    """Generate percental values."""
    for i in range(steps + 1):
        yield i * 100.0 / steps

if __name__ == "__main__":
    from time import sleep

    """
    Simple spinner
    """
    p = propeller()
    for i in xrange(1,20):
        p.update("Classic %i " % i)
        sleep(0.1)
    p.end()

    """
    Simple spinner with brackets
    """
    classic_style = classic(brackets=True)
    p = propeller(style = classic_style)
    for i in xrange(1,20):
        p.update("Classic with brackets %i " % i)
        sleep(0.1)
    p.end()
