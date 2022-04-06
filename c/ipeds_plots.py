import matplotlib.pyplot as plt

# import pdb
# from importlib import reload

# %%
# Set image path
import os

dirname = os.path.dirname(__file__)
tex_img_path = os.path.join(dirname, 'fig_tex_code')

# %%
# Add items from ipeds folder
from data.ipeds.c.clean_data.make_df import ReadData, MakeDict
from data.ipeds.c.save_ipeds_plots import save_rateplot, save_areaplot, save_comboplot

if __name__ == '__main__':
    readata = True

    if readata:
        # Add items from ipeds folder
        from data.ipeds.c import plot_by_n
        plot_n_degrees = plot_by_n.plot_n_degrees

        from data.ipeds.c import plot_by_cip
        PlotCIP = plot_by_cip.PlotCIP

        ipeds_dict = MakeDict()
        cip2labels_short = ipeds_dict.cip2labels_short
        cip2labels = cip2labels_short
        cip4labels_df = ipeds_dict.cip4labels_df

# %%
# Add items from img_tools
# from img_tools.tikzplotlib_functions import save_rateplot
from img_tools.figsize import ArticleSize
size = ArticleSize()
#
# from img_tools import plot_line_labels
# plot_df = plot_line_labels.plot_df

from img_tools import tikzplotlib_functions as tplf

# %%
# Old

# from data.ipeds.c.clean_data.make_df import cip4labels_df
# # get figure heigth and width
# from img.code import tikzplotlib_functions as tplf
# from img.code.figsize import ArticleSize
# size = ArticleSize()
#
# from data.ipeds.c import plot_by_n
# plot_n_degrees = plot_by_n.plot_n_degrees
#
# from data.ipeds.c import plot_by_cip
# PlotCIP = plot_by_cip.PlotCIP
# from data.ipeds.c import save_ipeds_plots
# save_rateplot = save_ipeds_plots.save_rateplot
# save_areaplot = save_ipeds_plots.save_areaplot
# save_comboplot = save_ipeds_plots.save_comboplot

plt.close('all')

# %%
##############################################################################
# 1. Number degrees completed by men and women

plot_n_degrees()
title_str = ('Number of Bachelor\'s Degrees awarded'
             ' in US 4-year colleges')
save_rateplot('n_degrees', source='Snyder (2013)', plot_title=title_str)

plt.close('all')

# %%
plt.close('all')
##############################################################################
# 2. Ration men to women in historically male dominated fields

male_dom_cip = ['14', '11', '40', '45', '27', '52', '26', '42']

# Initialize first sub-plot

fig, ax = plt.subplots(1, 2)
ref_name = 'fig:ipeds'
subplot_titles = ''
group_caption = ''
# Subplot specific data
ax_loc = 0
subtitle_id = 'a'

cip_dict = {
    'Social Sciences': ['45', '42'],
    'All Fields': ['98']
}

label_edit = {
    '11': -.1,  # Computer services
    '14': .02,  # Engineering
    '40': -.09,  # Physical sciences
    '52': .02,  # Business
    '26': -.03,  # Biological sciences
    '98': -.05  # All fields
}

# Create standalone version of graph
cip_cls = PlotCIP(male_dom_cip, rategraph=True, x_lim=2030,
                  label_edit=label_edit, cip_dict=cip_dict, rate_total=True)
save_rateplot('male_dom')

# %%

# Create version for sub-plot version
# edit cip dictionary
cip_cls.cip_dict['42'] = 'Social \\\\ Sciences'
cip_cls.cip_dict['11'] = 'Computer \\\\ Services'
cip_cls.cip_dict['26'] = 'Biological \\\\ Sciences'
cip_cls.cip_dict['27'] = 'Math'
cip_cls.cip_dict['40'] = 'Physical \\\\ Sciences'

# cip_dict = {'Computer \\\\ Services': ['11'],
#             'Biological \\\\ Sciences': ['26'],
#             'Math': ['27'],
#             'Physical \\\\ Sciences': ['40'],
#             'Social \\\\ Sciences': ['45', '42'],
#             'All Fields': ['98']
#             }

cip_cls.label_edit = {
    '14': .02, '11': -.25,
    '40': -.23, '27': 0.08, '52': .08,
    '26': -.25, '42': -.1, '98': -.1}

# plot sub-pot graph
cip_cls.plot_rate(ax=ax[ax_loc], xticks=[1990, 1995, 2000, 2005, 2010, 2015, 2020])

# edit variable for save_subplots
plt_title = ax[ax_loc].get_title()
# remove y-axis label
ax[ax_loc].set_title('')
subplot_titles += tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, col=False,
    subtitle_id=subtitle_id, plt_title=plt_title
)
group_caption += 'Ratio of women to men completing bachelor\'s degrees' \
    + ' in U.S. 4-year colleges from 1990 - 2019. Source: IPEDS.'

# %%
##############################################################################
# 3. Social sciences - rate and area graphs

# Subplot variables
ax_loc = 1
subtitle_id = 'b'

# Social science degrees
cip_list = ['42', '45.10', '45.11', '45.02', '45.06',
            # '45.07',
            '45.09',
            # '45.04',
            '45.01', '45.05', '45.14', '45.03', '45.12', '45.13', '45.99'
            ]
cip_dict_arg = {
    'Political science': ['45.10'],
    'Int\'l relations': ['45.09'],
    # 'Geography': ['45.07'],
    'Other': ['45.01', '45.04', '45.05', '45.05', '45.14', '45.03',
              '45.12', '45.13', '45.99']
}

# cip_list = ['42', '45.10', '45.11', '45.02', '45.06',
#             '45.09',
#             '45.01', '45.05', '45.14', '45.03', '45.12', '45.13', '45.99'
#             ]
# cip_dict_arg = {
#     'Political \\\\ science': ['45.10'],
#     'Int\'l relations': ['45.09'],
#     # 'Geography': ['45.07'],
#     'Other': ['45.01', '45.04', '45.05', '45.05', '45.14', '45.03',
#               '45.12', '45.13', '45.99']
# }

# Rate graph
cip_cls = PlotCIP(cip_list, cip_dict=cip_dict_arg,
                  cip_inlabel=False, drop_other=True, x_lim=2030)
cip_cls.plot_rate()
save_rateplot('social_science_rat')

# %%

# plot sub-pot graph
cip_cls = PlotCIP(cip_list, cip_dict=cip_dict_arg,
                  cip_inlabel=False, drop_other=False, x_lim=2032,)
cip_cls.label_edit = {
    '45.11': .1,  # Sociology
    '45.02': -.15,  # Anthropology
    '45.09': -.2,  # Int'l relations
    '45.10': -.3,  # Poli sci
    '45.06': -.2,
    '45.99': .1  # Other
}
# save version of subplot
cip_cls.cip_dict['45.10'] = 'Political \\\\ science'
cip_cls.cip_dict['45.09'] = 'Int\'l \\\\ relations'

cip_cls.plot_rate(ax=ax[ax_loc],
                  xticks=[1990, 1995, 2000, 2005, 2010, 2015, 2020])
# edit variable for save_subplots
plt_title = ax[ax_loc].get_title() + ' - Social Sciences'
# remove y-axis label
ax[ax_loc].set_title('')
subplot_titles += tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, col=False,
    subtitle_id=subtitle_id, plt_title=plt_title
)

tplf.save_subplots(os.path.join(tex_img_path, 'intro_ipeds.tex'),
                   figure=fig,
                   node_code=subplot_titles, caption=group_caption,
                   height=size.h(1.25), width=size.w(1.1),
                   extra_tikzpicture_parameters={
                       'every node/.style={font=\\footnotesize}',
                       'align=left'
                   })

# %%
# Area graph
PlotCIP(cip_list, cip_dict=cip_dict_arg, areagraph=True, shareyflag=False)
save_areaplot('social_science_area', 'Social Science')

# Add plot to subplot
plt.close('all')

# %%
##############################################################################
# Social Sciences cip
plt.close('all')

cip_list = ['45.01', '45.02', '45.03', '45.04', '45.05', '45.06', '45.07',
            '45.09', '45.10', '45.11', '45.12', '45.13', '45.14', '45.99']
cip42dict = {
    'Political science': ['45.10'],
    'Int\'l relations': ['45.09'],
    'Geography': ['45.07'],
    'Other': ['45.01', '45.05', '45.14', '45.03', '45.12', '45.13', '45.99']
}

label_edit = {'45.06': -.04}
ss = PlotCIP(cip_list, cip_dict=cip42dict,
             rategraph=True, areagraph=True, x_lim=2031)

save_comboplot(ss, 'cip45')

# %%
##############################################################################
# Engineering

cip_list = list(cip4labels_df.loc['14'].index)

cip_dict = {'Biomedical': ['14.05'],
            'Chemical': ['14.07'],
            'Industrial': ['14.35'],
            'Civil': ['14.08'],
            'Mechanical': ['14.19'],
            'Electrical': ['14.10'],
            'Computer': ['14.09'],
            'Other': ['14.01', '14.02', '14.03', '14.04', '14.06', '14.11',
                      '14.12', '14.13', '14.14', '14.18', '14.20',
                      '14.21', '14.22', '14.23', '14.24', '14.25',
                      '14.27', '14.28', '14.32', '14.33', '14.34',
                      '14.36', '14.37', '14.38', '14.39', '14.40',
                      '14.41', '14.42', '14.43', '14.44', '14.45',
                      '14.99']}

label_edit = {'14.07': .05, '14.35': .02,
              '14.19': .04, '14.09': -.12, '14.10': -.04,
              '14.99': -.04, '14.08': .04}

cip_cls = PlotCIP(cip_list=cip_list, cip_dict=cip_dict,
                  rategraph=True, areagraph=True,
                  label_edit=label_edit,
                  rate_title='Engineering',
                  x_lim=2031, shareyflag=False)
save_comboplot(cip_cls, 'cip14', slide=False)

# %%
# For paper
plt.close('all')
cip_cls = PlotCIP(cip_list=cip_list, cip_dict=cip_dict,
                  rategraph=True, areagraph=False,
                  label_edit=label_edit,
                  x_lim=2031, shareyflag=False)
save_rateplot('cip14_rat',
              extra_tikzpicture_parameters={
                  'every node/.style={font=\\footnotesize}',
                  'align=left'
              }
              )

# %%
##############################################################################
# Business and related services

cip_list = list(cip4labels_df.loc['52'].index)

cip_dict = {'General': ['52.01'],
            'Business admin.': ['52.02'],
            'Accounting': ['52.03'],
            'Finance': ['52.08'],
            'Hospitality': ['52.09'],
            'Human Resources': ['52.10'],
            'Management services': ['52.12'],
            'Other': ['52.04', '52.05', '52.06', '52.07', '52.11',
                      '52.12', '52.13', '52.15', '52.16', '52.17',
                      '52.18', '52.19', '52.20', '52.21', '52.99']}

label_edit = {'52.01': .03, '52.02': -.12, '52.03': .05,
              '52.08': -.15, '52.11': .06,
              '52.14': .15, '52.99': -.19}

cip_cls = PlotCIP(cip_list=cip_list, cip_dict=cip_dict,
                  rategraph=True, areagraph=True,
                  label_edit=label_edit,
                  x_lim=2031)

save_comboplot(cip_cls, 'cip52')

# %%
##############################################################################
# CS
plt.close('all')

cip_list = list(cip4labels_df.loc['11'].index)

cip_dict = {'General': ['11.01'],
            'Information science': ['11.04'],
            'Media applications': ['11.08'],
            'Systems network': ['11.09'],
            'IT': ['11.10'],
            'Other': ['11.02', '11.05', '11.99', '11.03', '11.06']}

label_edit = {'11.01': .06, '11.04': .08,
              '11.09': -.14, '11.10': -.1,
              '11.99': -.05,
              }

cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  x_lim=2031, shareyflag=False,
                  )

save_comboplot(cip_cls, 'cip11')

# %%
# CS - for paper
plt.close('all')
cip_list = list(cip4labels_df.loc['11'].index)

cip_dict = {'General': ['11.01'],
            'Information science': ['11.04'],
            'Media applications': ['11.08'],
            'Systems network': ['11.09'],
            'IT': ['11.10'],
            'Other': ['11.02', '11.05', '11.99', '11.03', '11.06']}

label_edit = {'11.01': .06, '11.04': .08,
              '11.09': -.14, '11.10': -.1,
              '11.99': -.05,
              }


# Create standalone version of graph
cip_cls = PlotCIP(
    cip_list=cip_list,
    cip_dict=cip_dict,
    label_edit=label_edit,
    rategraph=True, x_lim=2035)
# pdb.set_trace()
save_rateplot('cip11_rat',
               extra_tikzpicture_parameters = {
                   'every node/.style={font=\\footnotesize}',
                   'align=left'
               }
)
cip_dict = {'General': ['11.01'],
            'Information science': ['11.04'],
            'Media applications': ['11.08'],
            'Systems network': ['11.09'],
            'IT': ['11.10'],
            'Other': ['11.02', '11.05', '11.99', '11.03', '11.06']}

# Paper version
cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  rate_title=cip2labels['11'],
                  x_lim=2035, shareyflag=True,
                  )
save_comboplot(cip_cls, 'cip11_paper', slide=False)

  # %%
##############################################################################
# Education

cip_list = list(cip4labels_df.loc['13'].index)

cip_dict = {'Other': ['13.02', '13.03', '13.04', '13.05',
                      '13.06', '13.07', '13.09', '13.11',
                      '13.14', '13.15', '13.99'],
            'Specific subject area': ['13.13'],
            'Specific levels': ['13.12'],
            'Special Ed': ['13.10'],
            'General': ['13.01']}

label_edit = {'13.12': -1, '13.99': -.05
              # '11.09': -.14, '11.10': -.1,
              # '11.99': -.05,
              }

cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  x_lim=2031, shareyflag=False,
                  )

save_comboplot(cip_cls, 'cip13')

# %%
##############################################################################
# Biological sciences

plt.close('all')

cip_list = ['26']
label_edit = {}
cip_dict = {'Biology': ['26']}
# Paper version
cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=False,
                  rate_title='Biological sciences',
                  x_lim=2025, shareyflag=False,
                  )
save_rateplot('biology_rate_paper',
              extra_tikzpicture_parameters = {
                   'every node/.style={font=\\footnotesize}',
                   'align=left'
               })
# save_comboplot(cip_cls, 'biology_paper')


# %%
##############################################################################
# Biological and Physical Sciences and math
plt.close('all')

cip_list = ['26', '27'] + list(cip4labels_df.loc['40'].index)

cip_dict = {'Biology': ['26'], 'Math': ['27'],
            'Geosciences': ['40.06'],
            'Other': ['40.01', '40.02', '40.04', '40.99']}

label_edit = {'40.99': -.1, '27': .1}

# Slide version
cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  x_lim=2031, shareyflag=False,
                  )
save_comboplot(cip_cls, 'science_math')

# Paper version
cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  rate_title='Biological and physical sciences and Math',
                  x_lim=2031, shareyflag=False,
                  )
save_comboplot(cip_cls, 'science_math_paper')

# %%
##############################################################################
# Physical Sciences and math
plt.close('all')

cip_list = ['27'] + list(cip4labels_df.loc['40'].index)

cip_dict = {'Biology': ['26'], 'Math': ['27'],
            'Geosciences': ['40.06'],
            'Other': ['40.01', '40.02', '40.04', '40.99']}

label_edit = {'40.99': -.1, '27': .05, '40.06': -.03}

# Slide version
cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  x_lim=2031, shareyflag=False,
                  )
save_comboplot(cip_cls, 'physical_science_math')

# Paper version
cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  rate_title='Physical Sciences and Math',
                  x_lim=2031, shareyflag=True,
                  )
save_comboplot(cip_cls, 'physical_science_math_paper', slide=False)

# subplot_titles += tplf.subplot_title(

#     ax_loc=ax_loc, ref_name=ref_name, col=False,
#     subtitle_id=subtitle_id, plt_title=plt_title
# )


# extra_tikzpicture_parameters = {
#     'every node/.style={font=\\footnotesize}',
#     'align=left'
# })

# %%
##############################################################################
# Physical science
plt.close('all')

cip_list = list(cip4labels_df.loc['40'].index)

cip_dict = {'Biology': ['26'],
            'Geosciences': ['40.06'],
            'Other': ['40.01', '40.02', '40.04', '40.99']}

label_edit = {'40.99': -.1, '27': .05, '40.06': -.03}

# Slide version
cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rate_title='Physical Sciences',
                  rategraph=True, areagraph=False,
                  x_lim=2031, shareyflag=False,
                  )
tplf.save_subplots(
    tex_img_path + '/physical_science_paper.tex',
    height=size.h(1.25), width=size.w(1.1),
    extra_tikzpicture_parameters={
        'every node/.style={font=\\footnotesize}',
        'align=left'
    },
    caption='Source: IPEDS.'
)

# save_comboplot(cip_cls, 'bio_physical_science')

# Paper version
cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  rate_title='Physical Sciences',
                  x_lim=2031, shareyflag=True,
                  )
save_comboplot(cip_cls, 'bio_physical_science_paper', slide=False)

##############################################################################
# plt.close('all')
print('done: ipeds_plots.py')

# %%

ipeds_df = ReadData()
df4 = ipeds_df.df4
df2 = ipeds_df.df2

# %%

# Physics ratios

# Sentences to copy
cip4 = '40.08'
startyr = 1990
endyr = 2019

def print_rat(cip4=None, cip2=None, startyr=1990, endyr=2019, return_df=False):
    if cip4 is not None:
        assert cip2 is None, "Only pass cip4 or cip2"
        ciplabel = cip4labels_df.loc[cip4[:2], cip4]['ciptitle2010']
        aggdf = (
            df4.loc[df4['cip4'] == cip4][['ctotalm', 'ctotalw', 'year']]
                .groupby('year').sum())
    if cip2 is not None:
        assert cip4 is None, "Only pass cip4 or cip2"
        ciplabel = cip2labels['11']
        aggdf = (
            df2.loc[df2['cip2'] == cip2][['ctotalm', 'ctotalw', 'year']]
                .groupby('year').sum()
        )

    aggdf['rat'] = aggdf['ctotalw'] / aggdf['ctotalm']
    aggdf.loc[startyr, 'rat']

    print(
        f"Ratio of women to men completing degrees in {ciplabel} in"
        f" {startyr} was {aggdf.loc[startyr, 'rat']:.2f}."
        f"\n"
        f"Ratio of women to men completing degrees in {ciplabel} in"
        f" {endyr} was {aggdf.loc[endyr, 'rat']:.2f}"
    )

    if return_df:
        return aggdf

print_rat(cip4='40.08')

# %%

aggdf = print_rat(cip2='11', return_df=True)
min_idx = aggdf[aggdf['rat'] == aggdf['rat'].min()].index[0]
print(
    f"The ratio of women to men completing degrees in {cip2labels['11']}"
    f" reaches its low of {aggdf['rat'].min():.2f} in {min_idx}"
)

# %%

# Total CS ratio
cip2 = '11'
startyr = 1990
endyr = 2019

cip2label = cip2labels['11']
aggdf = (
    df2.loc[df2['cip2'] == cip2][['ctotalm', 'ctotalw', 'year']]
    .groupby('year').sum()
)

startyr_rat = aggdf['ctotalw'].loc[startyr] / aggdf['ctotalm'].loc[startyr]
endyr_rat = aggdf['ctotalw'].loc[endyr] / aggdf['ctotalm'].loc[endyr]

print(
    f"Ratio of women to men completing degrees in {cip2label} in"
    f" {startyr} was {startyr_rat:.2f}."
    f"\n"
    f"Ratio of women to men completing degrees in {cip4label} in"
    f" {endyr} was {endyr_rat:.2f}"
)
