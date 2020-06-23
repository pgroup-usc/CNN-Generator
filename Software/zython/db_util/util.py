"""
utility functions often used by db operation
"""
import sqlite3
import numpy as np
import timeit
from zython.logf.printf import *
from zython.db_util.conf import *
import re

import pdb

def surround_by_brackets(name):
    """
    NOTE: name can be a string or a list of string
    ensure that every element in name is surrounded by bracket.
    return a list or a string: cast to other structures on return, if needed
    """
    if type(name) == type(''):
        return (name[0]=='[' and name[-1]==']') and name or '[{}]'.format(name)
    else:
        return [(n[0]=='[' and n[-1]==']') and n or '[{}]'.format(n) for n in name]

def desurround_by_brackets(name):
    """
    NOTE: name can be either a string or a list of string
    ensure that every element in name is not surrounded by bracker.
    return a list or a string
    """
    if type(name) == type(''):
        return (name[0]=='[' and name[-1]==']') and name[1:-1] or name
    else:
        return [(n[0]=='[' and n[-1]==']') and n[1:-1] or n for n in name]




def is_table_exist(db_fullpath, table, c=None):
    """
    check if table exists in db_fullpath
    table may or may not be surrounded by '[' and ']'
    if c is not None, don't need to connect to db again
    """
    conn = None
    if not c:
        conn = sqlite3.connect(db_fullpath)
        c = conn.cursor()
    table = desurround_by_brackets(table)
    tbl_list = list(c.execute('SELECT name FROM sqlite_master WHERE type=\'table\''))
    if conn:
        conn.close()
    tbl_list = list(map(lambda x: x[0], tbl_list))
    return table in tbl_list


def get_table(table_regex, db_fullpath=None, c=None):
    """
    return a list of tables in db that matches the table_regex
    won't surround table by brackets
    """
    conn = None
    if not c:
        assert db_fullpath
        conn = sqlite3.connect(db_fullpath)
        c = conn.cursor()
    table_all = list(c.execute('SELECT name FROM sqlite_master WHERE type=\'table\''))
    table_all = list(map(lambda x: x[0], table_all))
    if conn:
        conn.close()
    treg = re.compile(table_regex)
    return [tbl for tbl in table_all if treg.match(tbl)]


def count_entry(db_fullpath, table, c=None):
    """
    return total num of entries in table
    table may or may not be surrounded by '[' and ']'
    """
    table = surround_by_brackets(table)
    conn = None
    if not c:
        conn = sqlite3.connect(db_fullpath)
        c = conn.cursor()
    ret = c.execute('SELECT Count(*) FROM {}'.format(table)).fetchone()[0]
    if conn:
        conn.close()
    return ret


def get_attr_info(table, enclosing=True, db_fullpath=None, c=None, db_attached=None):
    """
    return a dict for attr and the corresponding type
    with enclosing, the attr will be enclosed by '[' and ']'
    """
    table = surround_by_brackets(table)
    conn = None
    if not c:
        assert db_fullpath
        conn = sqlite3.connect(db_fullpath)
        c = conn.cursor()
    ret_dict = {}
    if db_attached:
        l = c.execute('pragma {}.table_info({})'.format(db_attached, table))
    else:
        l = c.execute('pragma table_info({})'.format(table))
    for t in list(l):
        f = enclosing and '[{}]' or '{}'
        ret_dict[f.format(t[1])] = t[2]
    if conn:
        conn.close()
    return ret_dict


def load_as_array(db_fullpath, table, attr_list, size=-1, c=None):
    """
    load data from db as numpy array
    attr name in attr_list may or may not be surrounded by '[' and ']'
    """
    conn = None
    if not c:
        conn = sqlite3.connect(db_fullpath)
        c = conn.cursor()
    attr_list = surround_by_brackets(attr_list)
    table = surround_by_brackets(table)
    tot_num = count_entry(db_fullpath, table, c=c)
    size = (size==-1) and tot_num or size
    if tot_num < size:
        printf('db don\'t have enough entries to load!', type='ERROR')
    c.execute('SELECT {} FROM {} LIMIT {}'.format(','.join(attr_list), table, size))
    ret = np.array(list(c.fetchall()))
    if conn:
        conn.close()
    return ret

