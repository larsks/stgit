
__copyright__ = """
Copyright (C) 2005, Catalin Marinas <catalin.marinas@gmail.com>

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
from pydoc import pager
from stgit.argparse import opt
from stgit.commands.common import *
from stgit.utils import *
from stgit.out import *
from stgit import argparse, stack, git

help = 'Show the tree diff'
kind = 'wc'
usage = ['[options] [<files or dirs>]']
description = """
Show the diff (default) or diffstat between the current working copy
or a tree-ish object and another tree-ish object (defaulting to HEAD).
File names can also be given to restrict the diff output. The
tree-ish object can be an StGIT patch, a standard git commit, tag or
tree. In addition to these, the command also supports '{base}',
representing the bottom of the current stack.

rev = '[branch:](<patch>|{base}) | <tree-ish>'"""

options = [
    opt('-r', '--range', metavar = 'rev1[..[rev2]]', dest = 'revs',
        short = 'Show the diff between revisions'),
    opt('-s', '--stat', action = 'store_true',
        short = 'Show the stat instead of the diff'),
    ] + argparse.diff_opts_option()

directory = DirectoryHasRepository()

def func(parser, options, args):
    """Show the tree diff
    """
    args = git.ls_files(args)
    directory.cd_to_topdir()

    if options.revs:
        rev_list = options.revs.split('..')
        rev_list_len = len(rev_list)
        if rev_list_len == 1:
            rev1 = rev_list[0]
            rev2 = None
        elif rev_list_len == 2:
            rev1 = rev_list[0]
            rev2 = rev_list[1]
        else:
            parser.error('incorrect parameters to -r')
    else:
        rev1 = 'HEAD'
        rev2 = None

    diff_str = git.diff(args, git_id(crt_series, rev1),
                        rev2 and git_id(crt_series, rev2),
                        diff_flags = options.diff_flags)
    if options.stat:
        out.stdout_raw(git.diffstat(diff_str) + '\n')
    else:
        if diff_str:
            pager(diff_str)
