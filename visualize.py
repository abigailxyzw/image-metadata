import pandas as pd
import seaborn as sns
import seaborn as sns

def describe_columns(merged_df):
    folder=os.path.join(os.getenv("HOME"), 'qanon/analysis/pngs')
    for col in merged_df.columns.tolist():
        print(col)
        counts_df=merged_df[col].value_counts()
        #pdb.set_trace()
        if counts_df.shape[0] < 20:
            print("making bar graph")
            try:
                sns.catplot(y=col, data = merged_df, kind="count", ci=None, aspect=2)
                if counts_df.shape[0] < 5:
                    plt.xticks(rotation = 360)
                else:
                    plt.xticks(rotation=90)
                plt.tight_layout()
                plt.savefig('%s/%s.png' % (folder, col))
                plt.close()
            except:
                continue

