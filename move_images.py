def get_q_pngs(post_dict):
    q_pngs=[]
    for drop in post_dict:
        try:
            media=drop['media']
        except KeyError:
            continue
        if media is not None and len(media) > 0:
            for m in media:
                q_png_fp_long=m['url']
                q_png_fp=os.path.basename(q_png_fp_long)
                if q_png_fp not in q_pngs:
                    q_pngs.append(q_png_fp)
    q_pngs.reverse()
    return q_pngs

#move pngs over
def _move_pngs_over(q_pngs, full_folder_from, full_folder_to):
    for q_png in q_pngs:
        full_fp_from='%s/%s' % (full_folder_from, q_png)
        full_fp_to='%s/%s' % (full_folder_to, q_png)
        os.system('mv %s %s' % (full_fp_from, full_fp_to))  

def _move_pngs_over_by_hundreds(q_pngs, pngs_drop_dict):
    #q_pngs.sort()
    full_folder_from=os.path.join(os.getenv("HOME"), 'Desktop/Image-ExifTool-12.16/Qdrops_Q')
    full_folder_to=os.path.join(os.getenv("HOME"), 'Desktop/Image-ExifTool-12.16/Qdrops_Q_partitioned')
    total_images=len(q_pngs)
    first=np.arange(0, total_images, step=100)
    last=np.arange(100, total_images+100, step=100)
    for picture_range in list(zip(first, last)):
        subfolder_to='%s/%s_%s' % (full_folder_to, str(picture_range[0]+1), str(picture_range[1]))
        if not os.path.exists(subfolder_to):
            os.makedirs(subfolder_to)
        png_in_range=q_pngs[picture_range[0]:picture_range[1]]
        #pdb.set_trace()
        for q_png in png_in_range:
            drops=png_drop_dict[q_png]
            drops_string='_'.join(drops)
            full_fp_from='%s/%s' % (full_folder_from, q_png)
            full_fp_to='%s/%s_%s' % (subfolder_to, drops_string, q_png)
            #print(full_fp_to)
            os.system('cp %s %s' % (full_fp_from, full_fp_to))  

