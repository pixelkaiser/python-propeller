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

class Style(object):

    spinner_pos = 0
    progress_width = 0
    current = 0
    maximum = 0
    percent = 0

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
