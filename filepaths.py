posts_fp=os.path.join(os.getenv("HOME"), 'qanon/data/all_drops/posts.json')
    exif_fp=os.path.join(os.getenv("HOME"), 'qanon/data/all_drops/Q_exif.csv')
    extras_fp=os.path.join(os.getenv("HOME"), 'qanon/data/all_drops/Q_drops_Q_extra_fields.csv')
    counts_fp=os.path.join(os.getenv("HOME"), 'qanon/analysis/png_counts.tsv')
    blacklisted_fp=os.path.join(os.getenv("HOME"), 'qanon/data/blacklisted.tsv')
    merged_fp=os.path.join(os.getenv("HOME"), 'qanon/data/all_drops/enriched_Q_exif.csv')
    all_time_info_fp=os.path.join(os.getenv("HOME"), 'qanon/analysis/all_time_info.csv')
    all_2017_profile_fp=os.path.join(os.getenv("HOME"), 'qanon/analysis/all_2017_info.csv')

#get_q_png_duplicates(post_dict)

    exif_df=read_exif_info(exif_fp)
    extras_df=read_extras_info(extras_fp)
    counts_df=read_counts(counts_fp)
    blacklist_df=read_blacklist(blacklisted_fp)
    merged_df=merge_exif_extra(extras_df, exif_df, counts_df, blacklist_df)
    #profiledt_df.to_csv(all_2017_profile_fp, index=False, header=True)
    #exit() 
    
    #datetime_cols=get_datetimecols(exif_df)
    #with_datestamps=datestamp_info_only(merged_df, datetime_cols) 
    #with_date_created_df=clean_date_info(with_datestamps)
    #with_date_created_df.to_csv(all_time_info_fp, index=False, header=True)

    #screenshots_fp=os.path.join(os.getenv("HOME"), 'qanon/analysis/screenshots.csv')
    #screenshots_df=merged_df[merged_df.UserComment=="Screenshot"]
    #screenshots_df=analyze_screenshots(screenshots_df)
    #pdb.set_trace()
    #screenshots_df.to_csv(screenshots_fp, index=False, header=True)
    #describe_columns(merged_df) 
    #pdb.set_trace()
    #merged_df.to_csv(merged_fp, index=False, header=True)
    #original pngs manipulations
    with open(posts_fp, 'r') as fh:
        post_dict=json.load(fh)
    q_pngs=get_q_pngs(post_dict)
    png_drop_dict=get_q_png_duplicates(post_dict)
    move_pngs_over_by_hundreds(q_pngs, png_drop_dict)

    #get_q_png_duplicates(post_dict)
    #get_q_pngs_with_extra_fields(post_dict)
    #pdb.set_trace()
    #move_pngs_over(q_pngs)
    #exif_df=read_exif_info(exif_fp)
