def read_extras_info(fp):
    names=['drop_number', 'drop_id', 'timestamp', 'source', 'trip', 'SourceFileShort']
    dtype={'drop_number': int, 'drop_id': int, 'timestamp': int, 'source': str, 'trip': str, 'SourceFileShort':str}
    drops_extra=pd.read_csv(fp, names=names, dtype=dtype, index_col=False)
    drops_extra['timestamp'] = pd.to_datetime(drops_extra['timestamp'], unit='s', utc=True)
    return drops_extra
counts_df=pd.read_csv(fp, names=names, dtype=dtype, sep='\t', index_col=False)
    return counts_df

#drop undefined columns
def drop_undefined(posts_df, col):
    posts_df=posts_df[~posts_df[col].isna()]
    return posts_df

def get_datetimecols(exif_df):
    all_cols=exif_df.columns.tolist()
    cols_df=pd.DataFrame({'col_name': all_cols})
    mask=cols_df.col_name.apply(lambda x: ('Date' in x) or ('Time' in x) or ('date' in x) or ('time' in x))
    dt_cols=cols_df[mask]
    as_list= dt_cols.col_name.values.tolist()
    as_list.remove('FileAccessDate')
    as_list.remove('FileInodeChangeDate')
    as_list.remove('FileModifyDate')
    as_list.remove('ProfileDateTime')
    return as_list

def datestamp_info_only(merged_df, datetime_cols):
    keep_rows=set()
    for dt_col in datetime_cols:
        bool_result=~merged_df[dt_col].isna()
        new_keep_rows=set(list(merged_df[bool_result].index))
        keep_rows=keep_rows.union(new_keep_rows)
    keep_rows=list(keep_rows)
    just_df=merged_df[merged_df.index.isin(keep_rows)]
    keep_cols=['timestamp', 'drop_number', 'source', 'trip'] + datetime_cols
    #reorder
    #return just_df[keep_cols]
    return just_df


