"""
some inteaction functions for analyzing data by proper operations
on the tables in the database
"""

import os
import sqlite3
from zython.db_util.conf import *
from zython.db_util.basic import *
from zython.db_util.util import *
from zython.logf.printf import *
from time import strftime
from numpy import *
import zython.logf.filef as filef

import pdb

def db_control_dim(meta_table, data_table, *var_attr, comm_key=TIME_ATTR,
    db_path=DB_DIR_PARENT, db_name=DB_NAME, db_temp="temp.db", temp_table="analysis#{}|null"):
    """
    TODO: filter on populate_time & bp-version
    aggregate the meta_table with data_table, filter out some runs by controlling variable,
    write the final table to new table, new file --> ready for visualization.

    ARGUMENTS:
        meta_table      table storing the mata info, usually configurations of a run
        data_table      table storing the data produced by the run --> join with meta to form a complete run
        var_attr        configuration variabes to analyze. will keep all other attr in conf the same
                        e.g.: if you want to analyze effect of momentum in ANN training.
                            then: var_attr='momentum', this will create multiple sub-tables,
                            with configurations such as learning rate, batch, etc., the same.
        comm_key            list or string: join meta_table and data_table by comm_key
        db_path, db_name    tell me where to find the meta_table & data_table
        db_temp, temp_table tell me where to write the processed new tables
                            table_temp should specify reflex rule for indexing.
                            e.g.:
                                temp_table = 'whoa-{}|ann', then whoa-0|ann, whoa-1|ann, ..., will be produced

    NOTE:
        the db_temp is always open with 'w' (overwrite), as it is not raw data.
        For security of db containing your raw data, always enforce read-only policy to it.
        (default setting for function in db_util.basic)
    """
    db_fullpath = '{}/{}'.format(db_path, db_name)
    # not my duty to check file existence
    conn = sqlite3.connect(db_fullpath)
    c = conn.cursor()
    meta_table, data_table, temp_table = surround_by_brackets([meta_table, data_table, temp_table])
    if len(array(comm_key).shape) == 0:
        comm_key = [comm_key]
    comm_key = surround_by_brackets(comm_key)
    comm_key = list(map(lambda x: '{}.{}={}.{}'.format(meta_table, x, data_table, x), comm_key))
    var_attr = surround_by_brackets(var_attr)
    # get list of attributes
    # attr in the meta table
    l_attr_meta = list(get_attr_info(meta_table, db_fullpath=db_fullpath).keys())
    l_attr_meta_flt = [item for item in l_attr_meta if item not in var_attr]
    l_attr_meta_flt = [item for item in l_attr_meta_flt if item not in ['[{}]'.format(TIME_ATTR)]]
    # attr in the data table
    l_attr_data = list(get_attr_info(data_table, db_fullpath=db_fullpath).keys())
    l_attr_type = get_attr_info(meta_table, db_fullpath=db_fullpath)
    # store the index of attr if it is of TEXT type --> append quote later
    text_idx = [l_attr_meta_flt.index(itm) for itm in l_attr_meta_flt if l_attr_type[itm]=='TEXT']
    # attr list in the joined table
    l_attr = set(var_attr + l_attr_data)
    l_attr = {(itm in var_attr) and '{}.{}'.format(meta_table, itm) \
                or '{}.{}'.format(data_table, itm) for itm in l_attr}
    #
    control_var = list(c.execute('SELECT DISTINCT {} FROM {}'.format(','.join(l_attr_meta_flt), meta_table)))
    temp_fullpath = '{}/{}'.format(db_path, db_temp)
    open(temp_fullpath, 'w').close()    # always overwrite
    db_temp = surround_by_brackets(db_temp)
    c.execute('ATTACH DATABASE \'{}\' AS {}'.format(temp_fullpath, db_temp))
    for flt in control_var:
        flt = [(flt.index(itm) in text_idx) and '\'{}\''.format(itm) or itm for itm in flt]
        flt_cond = ['{}.{}={}'.format(meta_table, l_attr_meta_flt[i], flt[i]) for i in range(len(flt))]
        flt_cond_neat = ['{}={}'.format(l_attr_meta_flt[i], flt[i]) for i in range(len(flt))]
        temp_table_i = temp_table.format(','.join(flt_cond_neat).replace('[','').replace(']',''))
        c.execute('CREATE TABLE {}.{} AS SELECT {} FROM {} JOIN {} ON {} WHERE {}'\
            .format(db_temp, temp_table_i, ','.join(l_attr),
                    meta_table, data_table, ' and '.join(comm_key),
                    ' and '.join(flt_cond))) 
    conn.commit()
    conn.close()



def sanity_last_n_commit(*table, num_run=1, db_name=DB_NAME, db_path=DB_DIR_PARENT, time_attr=TIME_ATTR):
    """
    delete the entries with the latest populate_time, for all tables with the time attr

    ARGUMENTS:
        table       if table=(), then delete entries for all tables, otherwise only delete for that in *table
        num_run     delete entries with the last (num_run) populate time
        time_attr   the name of the time attribute
    """
    db_fullpath = '{}/{}'.format(db_path, db_name)
    conn = sqlite3.connect(db_fullpath)
    c = conn.cursor()
    if len(table) == 0:
        table = list(c.execute('SELECT name FROM sqlite_master WHERE type=\'table\''))
        table = list(map(lambda x: '[{}]'.format(x[0]), table))
    else:
        table = list(map(lambda x: '[{}]'.format(x), table))
    # fliter table list to those actually contains the time_attr
    table_flt = []
    for tbl in table:
        tbl_attr = list(get_attr_info(tbl, enclosing=False, db_fullpath=db_fullpath).keys())
        if time_attr in tbl_attr:
            table_flt += [tbl]
    time_attr = surround_by_brackets(time_attr)
    time_set = set()
    for tbl in table_flt:
        cur_time_set = set(c.execute('SELECT DISTINCT {} FROM {}'.format(time_attr, tbl)))
        time_set |= set(map(lambda x: x[0], cur_time_set))
    conn.close()
    time_len = len(time_set)
    num_run = (num_run>time_len) and time_len or num_run
    time_list = sorted(list(time_set))[time_len-num_run:]
    for tbl in table_flt:
        for t in time_list:
            sanity_db(time_attr[1:-1], t, tbl[1:-1], db_name=db_name, db_path=db_path)
    
    printf('Done: cleared last {} commits for {}'.format(num_run, table_flt))
    bad_table = set(table) - set(table_flt)
    if bad_table:
        printf('tables {} don\'t have attr {}', bad_table, time_attr, type='WARN')


def drop_col(table, *col_drop, db_name=DB_NAME, db_path=DB_DIR_PARENT):
    """
    very basic function for dropping a column in a sqlite db table.
    --> reason for this: sqlite does not support drop operation
    """
    from functools import reduce
    db_fullpath = '{}/{}'.format(db_path, db_name)
    perm = os.stat(db_fullpath).st_mode
    filef.set_f_perm(db_fullpath, '0666')
    conn = sqlite3.connect(db_fullpath)
    c = conn.cursor()
    table = surround_by_brackets(table)
    col_dict = get_attr_info(table, c=c)
    # import pdb; pdb.set_trace()
    remain_keys = set(col_dict.keys()) - set(surround_by_brackets(col_drop))
    remain_keys_str = reduce(lambda _1,_2: '{}, {}'.format(_1,_2), remain_keys)
    remain_attr_str = reduce(lambda _1,_2: '{}, {} {}'.format(_1, _2, col_dict[_2]), remain_keys)
    cmd = \
       ('CREATE TABLE _bk ({remain_attr_str});\n'
        'INSERT INTO _bk SELECT {remain_keys_str} from {table};\n'
        'DROP TABLE {table};\n'
        'ALTER TABLE _bk RENAME TO {table};')\
                .format(table=table, remain_attr_str=remain_attr_str, remain_keys_str=remain_keys_str)
    for cmd_ in cmd.split('\n'):
        printf(cmd_)
        c.execute(cmd_)
    conn.commit()
    conn.close()
    filef.set_f_perm(db_fullpath, perm)
    printf('successfully drop column(s): {}', col_drop)


def add_col(table, col_add_name, col_add_type, f_lambda, *dependencies, db_name=DB_NAME, db_path=DB_DIR_PARENT):
    """
    dependencies        col in the original table
                        should pass dependencies to f_lambda
    """
    db_fullpath = '{}/{}'.format(db_path, db_name)
    perm = os.stat(db_fullpath).st_mode
    filef.set_f_perm(db_fullpath, '0666')
    conn = sqlite3.connect(db_fullpath)
    c = conn.cursor()
    table = surround_by_brackets(table)
    col_add_name = surround_by_brackets(col_add_name)
    dependencies = surround_by_brackets(dependencies)
    dp_str = reduce(lambda _1,_2:'{}, {}'.format(_1,_2), dependencies)
    col_dict = get_attr_info(table, c=c)
    assert set(dependencies).issubset(set(col_dict.keys()))
    c.execute('ALTER TABLE {table} ADD COLUMN {col} {type}'.format(table=table, col=col_add_name, type=col_add_type))
    dp_list = list(c.execute('SELECT {dp} FROM {table}'.format(dp=dp_str, table=table)) )
    for dp in dp_list:
        up_cond = zip(dependencies, dp)
        up_cond_str = map(lambda _: '{}={}'.format(_[0],_[1]), up_cond)
        up_cond_str = reduce(lambda _1,_2: '{} and {}'.format(_1,_2), up_cond_str)
        c.execute('UPDATE {table} SET {col} = {ret} WHERE {cond}'\
            .format(table=table, col=col_add_name, 
                    ret=f_lambda(*dp), cond=up_cond_str))
    conn.commit()
    conn.close()
    filef.set_f_perm(db_fullpath, perm)
    printf('successfully add column: {}', col_add_name)


def normalize_col(table, col, group_by_key, db_name=DB_NAME, db_path=DB_DIR_PARENT):
    db_fullpath = '{}/{}'.format(db_path, db_name)
    perm = os.stat(db_fullpath).st_mode
    filef.set_f_perm(db_fullpath, '0666')
    conn = sqlite3.connect(db_fullpath)
    c = conn.cursor()
    table = surround_by_brackets(table)
    group_by_key = surround_by_brackets(group_by_key)
    col_norm = '{}_norm'.format(col)
    col_norm = surround_by_brackets(col_norm)
    col = surround_by_brackets(col)
    c.execute('ALTER TABLE {table} ADD COLUMN {col_norm} REAL'.format(table=table, col_norm=col_norm))
    k_list = list(c.execute('SELECT DISTINCT {filt} FROM {table}'.format(filt=group_by_key, table=table)) )
    k_list = [i[0] for i in k_list]
    for k in k_list:
        m = list(c.execute('SELECT max({col}) FROM {table} WHERE {filt}={k}'.format(col=col, table=table, filt=group_by_key, k=k)))[0]
        m = float(m[0])
        d_list = list(c.execute('SELECT {col} FROM {table} WHERE {filt}={k}'.format(col=col, table=table, filt=group_by_key, k=k)))
        d_list = [i[0] for i in d_list]
        for d in d_list:
            c.execute('UPDATE {table} SET {col_norm} = {ret} WHERE {filt}={k1} AND {col}={k2}'\
                .format(table=table, col_norm=col_norm, ret=d/m, 
                    filt=group_by_key, k1=k, col=col, k2=d))
    
    conn.commit()
    conn.close()
    filef.set_f_perm(db_fullpath, perm)
    printf('successfully normalize column: {}', col)
