import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Add items from ipeds folder
from data.ipeds.c.clean_data.make_df import ReadData, MakeDict
from data.ipeds.c.save_ipeds_plots import save_rateplot, save_areaplot, save_comboplot

# from data.ipeds.c import plot_by_cip
# PlotCIP = plot_by_cip.PlotCIP
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

stem_cip = [k for k, v in stem_dict.items() if v == 'STEM']
non_stem_cip = [k for k, v in stem_dict.items() if v == 'Non-STEM']

# %% Create dataframe with gender ratio for STEM and non-STEM fields

df['stem'] = df['cip2'].map(stem_dict)
assert df['stem'].notna().all()

stem_df = df.groupby(['year', 'stem'])[['ctotalm', 'ctotalw']].sum()
stem_df['ratio'] = stem_df['ctotalw'] / stem_df['ctotalm']

stem_df.drop(columns=['ctotalm', 'ctotalw'], inplace=True)
stem_df = stem_df.unstack()

stem_df.columns = stem_df.columns.droplevel(0)

# %% Create a dataframe with gender ratio for all fields

all_df = df.groupby('year')[['ctotalm', 'ctotalw']].sum()
all_df['All fields'] = all_df['ctotalw'] / all_df['ctotalm']

all_df['All fields'] = all_df['ctotalw'] / all_df['ctotalm']
all_df.drop(columns=['ctotalm', 'ctotalw'], inplace=True)

# %% Merge dataframes together; this will be plotted in figure A

agg_df = pd.merge(stem_df, all_df, left_index=True, right_index=True)

# %% Create a dataframe with gender ratios in STEM subfields

stem_fields_dict = {
    'Agriculture and natural resources': ['01', '03'],
    'Computer services': ['11'],
    'Engineering and engineering technologies': ['14', '15'],
    'Biological sciences': ['26'],
    'Math and statistics': ['27'],
    'Physical sciences and science technologies': ['40', '41']
}

# keeping the max number
stem_field_df = df.loc[df['stem'] == 'STEM'].copy()
stem_field_df['stem_field'] = stem_field_df['cip2'].map(
    # New column has value labels
    # {v: k for k, v_list in stem_fields_dict.items() for v in v_list}
    # New value has max key
    {v: max(v_list) for k, v_list in stem_fields_dict.items() for v in v_list}
)

stem_df = (stem_field_df
           .groupby(['year', 'stem_field'])[['ctotalm', 'ctotalw']]
           .sum())
stem_df['ratio'] = stem_df['ctotalw'] / stem_df['ctotalm']

stem_df.drop(columns=['ctotalm', 'ctotalw'], inplace=True)
stem_df = stem_df.unstack()
stem_df.columns = stem_df.columns.droplevel(0)

# %% First subplot: ratio of women to men in all STEM fields

fig, ax = plt.subplots(1, 2, sharey=False)
ref_name = 'fig:ipeds_stem'
subplot_titles = ''
group_caption = 'Ratio of women to men completing bachelor\'s degrees' \
    + ' in U.S. 4-year colleges from 1990 - 2019.'
# Subplot specific data
ax_loc = 0
subtitle_id = 'a'

plot_df(
    agg_df, ax=ax[ax_loc],
    xticks=[1990, 1995, 2000, 2005, 2010, 2015, 2020],
    x_lim=2030,
)
ax[ax_loc].set_ylim(bottom=0)
# remove title of subplot
ax[ax_loc].set_title('')
# Name of subplot; will be added in label below
plt_title = 'Ratio of women to men'
# Add to the subplot string
subplot_titles += tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name,
    subtitle_id=subtitle_id, plt_title=plt_title)
# Add to the group caption
group_caption += f' Figure ({subtitle_id}) plots the ratio in' \
    + ' STEM and non-STEM fields.'

# Second subplot: ratio of women to men in STEM sub-fields
# fig, ax = plt.subplots()
ax_loc = 1
subtitle_id = 'b'

label_dict = {max(v_list): k for k, v_list in stem_fields_dict.items()}
label_dict['03'] = 'Agriculture\\\\\\& natural\\\\resources'
label_dict['11'] = 'Computer\\\\services'
label_dict['27'] = 'Math \\&\\\\stats'
label_dict['26'] = 'Biological\\\\sciences'
label_dict['15'] = 'Engineering'
label_dict['41'] = 'Physical\\\\sciences'

label_edit = {
    '11': -.22,  # Computer services
    '15': .04,  # Engineering
    '41': -.22,  # Physical sciences
    '27': .02,
    '26': -.2,  # Biological sciences
    '03': -.2,  # Ag and nat resources
}

plot_df(
    stem_df, ax=ax[ax_loc],
    # stem_df, ax=ax,
    xticks=[1990, 1995, 2000, 2005, 2010, 2015, 2020],
    x_lim=2031,
    col_labels=label_dict, label_edit=label_edit
    # yticks=np.linspace(0, 2, 10, endpoint=False)
)
# plt.show()

ax[ax_loc].set_ylim(bottom=0)
# remove title of subplot
ax[ax_loc].set_title('')
# Name of subplot; will be added in label below
plt_title = 'Ratio of women to men in STEM fields'
# Add to the subplot string
subplot_titles += tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, col=False,
    subtitle_id=subtitle_id, plt_title=plt_title)
# Add to the group caption
group_caption += f' Figure ({subtitle_id}) plots the ratio in' \
    + ' in various STEM sub-fields.'

# Save combined figure
group_caption += ' Source: IPEDS.'
tplf.save_subplots(
    tex_img_path + '/ratio_stem_subfields.tex',
    figure=fig,
    node_code=subplot_titles, caption=group_caption,
    height=size.h(1.25), width=size.w(1.05),
    clean_figure=True,
    extra_tikzpicture_parameters={
        'every node/.style={font=\\footnotesize}',
        'align=left'
    },
)