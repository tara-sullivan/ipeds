import pandas as pd
import matplotlib.pyplot as plt
# Add items from ipeds folder
from data.ipeds.c.clean_data.make_df import ReadData, MakeDict
from data.ipeds.c.save_ipeds_plots import save_rateplot, save_areaplot, save_comboplot

# %%

from img_tools.figsize import ArticleSize
size = ArticleSize()

from img_tools import plot_line_labels
plot_df = plot_line_labels.plot_df

from img_tools import tikzplotlib_functions as tplf

import os
dirname = os.path.dirname(__file__)
tex_img_path = os.path.join(dirname, 'fig_tex_code')

# from data.ipeds.c import plot_by_cip
# PlotCIP = plot_by_cip.PlotCIP
# %%

ipeds_df = ReadData()
df, df2, df4 = ipeds_df.df, ipeds_df.df2, ipeds_df.df4

ipeds_dict = MakeDict()
cip2labels_short = ipeds_dict.cip2labels_short
cip2labels = cip2labels_short

# %%

stem_dict = {
    '01': 'STEM',  # 'Agriculture and related sciences',
    '03': 'STEM',  # 'Natural resources and conservation',
    '04': 'Non-STEM',  # 'Architecture and related services',
    '05': 'Non-STEM',  # 'Group studies',
    '09': 'Non-STEM',  # 'Communcation',
    '10': 'Non-STEM',  # 'Communications tech.',
    '11': 'STEM',  # 'Computer services',
    '12': 'Non-STEM',  # 'Personal and culinary services',
    '13': 'Non-STEM',  # 'Education',
    '14': 'STEM',  # 'Engineering',
    '15': 'STEM',  # 'Engineering technologies',
    '16': 'Non-STEM',  # 'Foreign languages',
    '19': 'Non-STEM',  # 'Family and consumer sciences',
    '22': 'Non-STEM',  # 'Legal professions and studies',
    '23': 'Non-STEM',  # 'English language and literature/letters',
    '24': 'Non-STEM',  # 'Liberal arts',
    '25': 'Non-STEM',  # 'Library science',
    '26': 'STEM',  # 'Biological sciences',
    '27': 'STEM',  # 'Math and stats',
    '28': 'Non-STEM',  # 'Military science, leadership and operational art',
    '29': 'Non-STEM',  # 'Military technologies and applied sciences',
    '30': 'Non-STEM',  # 'Interdisciplinary',
    '31': 'Non-STEM',  # 'Parks, recreation, leisure, and fitness studies',
    '32': 'Non-STEM',  # 'Basic skills and developmental/remedial education',
    '33': 'Non-STEM',  # 'Citizenship activities',
    '34': 'Non-STEM',  # 'Health-related knowledge and skills',
    '35': 'Non-STEM',  # 'Interpersonal and social skills',
    '36': 'Non-STEM',  # 'Leisure and recreational activities',
    '37': 'Non-STEM',  # 'Personal awareness and self-improvement',
    '38': 'Non-STEM',  # 'Philosophy and religious studies',
    '39': 'Non-STEM',  # 'Theology and religious vocations',
    '40': 'STEM',  # 'Physical sciences',
    '41': 'STEM',  # 'Science technologies/technicians',
    '42': 'Non-STEM',  # 'Psychology',
    '43': 'Non-STEM',  # 'Law enforcement',
    '44': 'Non-STEM',  # 'Public administration and social service professions',
    '45': 'Non-STEM',  # 'Social sciences',
    '46': 'Non-STEM',  # 'Construction trades',
    '47': 'Non-STEM',  # 'Mechanic and repair technologies/technicians',
    '48': 'Non-STEM',  # 'Precision production',
    '49': 'Non-STEM',  # 'Transportation and materials moving',
    '50': 'Non-STEM',  # 'Arts',
    '51': 'Non-STEM',  # 'Health',
    '52': 'Non-STEM',  # 'Business',
    '53': 'Non-STEM',  # 'High school/secondary diplomas and certificates',
    '54': 'Non-STEM',  # 'History',
    '60': 'Non-STEM',  # 'Residency programs'
}
# %%

df['stem'] = df['cip2'].map(stem_dict)
assert df['stem'].notna().all()

stem_df = df.groupby(['year', 'stem'])[['ctotalm', 'ctotalw']].sum()
stem_df['ratio'] = stem_df['ctotalw'] / stem_df['ctotalm']

stem_df.drop(columns=['ctotalm', 'ctotalw'], inplace=True)
stem_df = stem_df.unstack()

stem_df.columns = stem_df.columns.droplevel(0)

# %% all DF

all_df = df.groupby('year')[['ctotalm', 'ctotalw']].sum()
all_df['All fields'] = all_df['ctotalw'] / all_df['ctotalm']

all_df['All fields'] = all_df['ctotalw'] / all_df['ctotalm']
all_df.drop(columns=['ctotalm', 'ctotalw'], inplace=True)

# %%

agg_df = pd.merge(stem_df, all_df, left_index=True, right_index=True)

# %%

# Create standalone version of graph
# cip_cls = PlotCIP(plot_df, rategraph=True, areagraph=False, x_lim=2030,
#                   # label_edit=label_edit, cip_dict=cip_dict, rate_total=True
#                   )
# save_rateplot('male_dom')
fig, ax = plt.subplots()
plot_df(
    agg_df, ax=ax,
    title='Ratio of women to men',
    x_lim=2030
    # xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020]
)

ax.set_ylim(bottom=0)
# plt.show()
tplf.save_subplots(
    tex_img_path + '/ratio_stem.tex',
    height=size.h(1.25), width=size.w(1.1),
    extra_tikzpicture_parameters={
        'every node/.style={font=\\footnotesize}',
        'align=left'
    },
    caption='STEM fields include: '
            'agriculture and related sciences; '
            'natural resources and conservation; '
            'computer services; '
            'engineering; '
            'engineering technologies; '
            'biological sciences; '
            'mathematics and statistics; '
            'physical sciences; '
            ' and science technologies. '
            'Source: IPEDS.'
)