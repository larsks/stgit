__copyright__ = """
Copyright (C) 2007, Catalin Marinas <catalin.marinas@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

import sys, os
from stgit.argparse import opt
from stgit.commands.common import *
from stgit.utils import *
from stgit.out import *
from stgit import stack, git

help = 'Unhide a hidden patch'
kind = 'stack'
usage = ['[options] <patch-range>']
description = """
Unhide a hidden range of patches so that they are shown in the plain
'stg series' command output."""

options = [
    opt('-b', '--branch',
        short = 'Use BRANCH instead of the default branch')]

directory = DirectoryHasRepository()

def func(parser, options, args):
    """Unhide a range of patches in the series
    """
    if args:
        # parsing all the patches for a more meaningful error reporting
        all_patches = crt_series.get_applied() + crt_series.get_unapplied() \
                      + crt_series.get_hidden()
        patches = parse_patches(args, all_patches)
    else:
        parser.error('No patches specified')

    for patch in patches:
        crt_series.unhide_patch(patch)
        out.info('Patch "%s" unhidden' % patch)
