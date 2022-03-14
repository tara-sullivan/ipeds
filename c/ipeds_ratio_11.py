
# Set image path
import os

dirname = os.path.dirname(__file__)
tex_img_path = os.path.join(dirname, 'fig_tex_code')

from tabulate import tabulate

# %%
# Add items from ipeds folder
from data.ipeds.c.clean_data.make_df import ReadData, MakeDict
from data.ipeds.c.save_ipeds_plots import save_rateplot, save_areaplot, save_comboplot

# Keep 2010-2011 data

ipeds_df = ReadData()
df, df2, df4 = ipeds_df.df, ipeds_df.df2, ipeds_df.df4

ipeds_dict = MakeDict()
cip2labels_short = ipeds_dict.cip2labels_short
cip2labels = cip2labels_short

# # %%
#
# # NCES dictionaries
#
# major_map = {
#     0.0: 0.0,    # Undecided or undeclared
#     1.0: 1.0,    # Computer and information sciences
#     2.0: 2.0,    # Engineering and engineering technology
#     3.0: 3.0,    # Biological and physical science, science tech
#     4.0: 4.0,    # Mathematics
#     5.0: 5.0,    # Agriculture and natural resources
#     6.0: 6.0,    # General studies and other
#     7.0: 7.0,    # Social Sciences
#     8.0: 8.0,    # Psychology
#     9.0: 9.0,    # Humanities
#     10.0: 9.0,   # History > Humanities
#     11.0: 24.0,  # Personal and consumer services > Other Applied
#     12.0: 24.0,  # Manufacturing, construction, repair, transportation > Oth.A
#     13.0: 24.0,  # Military technology and protective services > Other Applied
#     14.0: 14.0,  # Health care fields
#     15.0: 15.0,  # Business
#     16.0: 16.0,  # Education
#     17.0: 24.0,  # Architecture > Other Applied
#     18.0: 18.0,  # Communications
#     19.0: 24.0,  # Public administration and human services > Other Applied
#     20.0: 24.0,  # Design and applied arts > Other Applied
#     21.0: 24.0,  # Law and legal studies > Other Applied
#     22.0: 24.0,  # Library Science > Other Applied
#     23.0: 24.0   # Theology and religious vocations > Other Applied
# }
#
# major_dict = {
#     0.0: 'Undecided or undeclared',
#     1.0: 'Computer and information sciences',
#     2.0: 'Engineering and engineering technology',
#     3.0: 'Biological and physical science, science tech',
#     4.0: 'Mathematics',
#     5.0: 'Agriculture and natural resources',
#     6.0: 'General studies and other',
#     7.0: 'Social Sciences',
#     8.0: 'Psychology',
#     9.0: 'Humanities',
#     14.0: 'Health care fields',
#     15.0: 'Business',
#     16.0: 'Education',
#     18.0: 'Communications',
#     24.0: 'Other Applied'
# }

# %%

# NCES dictionaries

major_map = {
    0.0: 0.0,    # Undecided or undeclared
    1.0: 1.0,    # Computer and information sciences
    2.0: 2.0,    # Engineering and engineering technology
    3.0: 3.0,    # Biological and physical science, science tech
    4.0: 4.0,    # Mathematics
    5.0: 5.0,    # Agriculture and natural resources
    6.0: 6.0,    # General studies and other
    7.0: 7.0,    # Social Sciences
    8.0: 8.0,    # Psychology
    9.0: 9.0,    # Humanities
    10.0: 9.0,   # History > Humanities
    11.0: 24.0,  # Personal and consumer services > Oth. Applied
    12.0: 12.0,  # Manufacturing, construction, repair, transportation > Oth.A
    13.0: 13.0,  # Military technology and protective services
    14.0: 14.0,  # Health care fields
    15.0: 15.0,  # Business
    16.0: 16.0,  # Education
    17.0: 17.0,  # Architecture
    18.0: 18.0,  # Communications
    19.0: 24.0,  # Public administration and human services > Other App.
    20.0: 24.0,  # Design and applied arts > Other Applied
    21.0: 21.0,  # Law and legal studies
    22.0: 6.0,   # Library Science > General studies and other
    23.0: 24.0   # Theology and religious vocations > Other Applied
}

major_dict = {
    0.0: 'Undecided or undeclared',
    1.0: 'Computer and information sciences',
    2.0: 'Engineering and engineering technology',
    3.0: 'Biological and physical science, science tech',
    4.0: 'Mathematics',
    5.0: 'Agriculture and natural resources',
    6.0: 'General studies and other',
    7.0: 'Social Sciences',
    8.0: 'Psychology',
    9.0: 'Humanities',
    12.0: 'Manufacturing',
    13.0: 'Military and protective services',
    14.0: 'Health care fields',
    15.0: 'Business',
    16.0: 'Education',
    17.0: 'Architecture',
    18.0: 'Communications',
    21.0: 'Law and legal studies',
    24.0: 'Other Applied'
}
# %%

# map to cip labels - 23 categories
ipeds_to_nces23_dict = {
    '01': 5.0,   # 'Agriculture and related sciences'
                 # > 'Agriculture and natural resources'
    '03': 5.0,   # 'Natural resources and conservation'
                 # > 'Agriculture and natural resources'
    '04': 17.0,  # 'Architecture and related services'
                 # > Architecture
    '05': 9.0,   # 'Group studies',
                 # > Humanities [CHECK]
    '09': 18.0,  # 'Communcation'
                 # > Communications
    '10': 18.0,  # 'Communications tech.'
                 # > Communication
    '11': 1.0,   # Computer services
                 # > Computer and information sciences
    '12': 11.0,  # 'Personal and culinary services'
                 # > Personal and consumer services
    '13': 16.0,  # 'Education',
                 # > Education
    '14': 2.0,   # 'Engineering'
                 # > 'Engineering and engineering technology'
    '15': 2.0,   # 'Engineering technologies'
                 # > Engineering and engineering technology
    '16': 9.0,   # 'Foreign languages',
                 # > Humanities
    '19': 19.0,  # 'Family and consumer sciences',
                 # >  Public administration and human services [CHECK]
    '22': 21.0,  # 'Legal professions and studies',
                 # > Law and legal studies
    '23': 9.0,   # 'English language and literature/letters',
                 # > Humanities
    '24': 6.0,   # 'Liberal arts',
                 # > 6, # General studies and other
    '25': 22.0,  # 'Library science',
                 # > 22.0, Library Science
    '26': 3.0,   # 'Biological sciences'
                 # > Biological and physical science, science tech
    '27': 4.0,   # 'Math and stats'
                 # > Mathematics
    '28': 13.0,  # 'Military science, leadership and operational art',
                 # > 13, Military technology and protective services
    '29': 13.0,  # 'Military technologies and applied sciences',
                 # > 13.0, Military technology and protective services
    '30': 6.0,   # 'Interdisciplinary',
                 # > 6.0, General studies and other [CHECK]
    '31': 11.0,  # 'Parks, recreation, leisure, and fitness studies',
                 # 11.0 Personal and consumer services
    '32': 99.0,  # 'Basic skills and developmental/remedial education',
                 # 99.0 to drop
    '33': 99.0,  # 'Citizenship activities',
                 # 99.0 to drop
    '34': 99.0,  # 'Health-related knowledge and skills',
                 # 99.0 to drop
    '35': 99.0,  # 'Interpersonal and social skills',
                 # 99.0 to drop
    '36': 99.0,  # 'Leisure and recreational activities',
                 # 99.0 to drop
    '37': 99.0,  # 'Personal awareness and self-improvement',
                 # 99.0 to drop
    '38': 9.0,   # 'Philosophy and religious studies',
                 # > 9.0 Humanities
    '39': 23.0,  # 'Theology and religious vocations',
                 # > 23.0 Theology and religious vocations
    '40': 3.0,   # 'Physical sciences'
                 # Biological and physical science, science tech
    '41': 3.0,   # 'Science technologies/technicians',
                 # Biological and physical science, science tech
    '42': 8.0,   # 'Psychology',
                 # > Psychology
    '43': 13.0,  # 'Law enforcement',
                 # 13.0: Military technology and protective services
    '44': 19.0,  # 'Public administration and social service professions',
                 # > 19.0 Public administration and human services [CHE
    '45': 7.0,   # Social sciences
                 # > 7.0 Social siences
    '46': 12.0,  # 'Construction trades',
                 # 12 Manufacturing, construction, repair, transportation
                 # [CHECK]
    '47': 12.0,  # 'Mechanic and repair technologies/technicians',
                 # 12 Manufacturing, construction, repair, transportation
                 # [CHECK]
    '48': 12.0,  # 'Precision production',
                 # 12.0 Manufacturing, construction, repair, transportation
                 # [CHECK]
    '49': 12.0,  # 'Transportation and materials moving',
                 # 12.0 Manufacturing, construction, repair, transportation
                 # [CHECK]
    '50': 9.0,   # 'Arts',
                 # > 9.0 Humanities [CHECK]
    '51': 14.0,  # 'Health',
                 # 14.0 Health care fields
    '52': 15.0,  # 'Business',
                 # 15.0 Business
    '53': 99.0,  # 'High school/secondary diplomas and certificates',
                 # 99.0 TO DROP
    '54': 10.0,  # 'History',
                 # > 10.0 History
    '60': 60.0,  # 'Residency programs'
                 # CHECK - not in data
}

# %%
year1 = 2011
year2 = 2019

df = df2.loc[df2['year'].isin([2011, 2019])].copy()

# First map the values to the majors23 values in the NCES data
df['majors23'] = df['cip2'].map(ipeds_to_nces23_dict)
assert df['majors23'].notna().all()

# next create a mapping to my majors 15 categorization
df['majors15_idx'] = df['majors23'].map(major_map)
assert df['majors15_idx'].notna().all()

df['majors15'] = df['majors15_idx'].map(major_dict)
# %%

# generate the gender ratio for each of these fields
agg_df = df.groupby(['majors15', 'year'])[['ctotalm', 'ctotalw']].sum()
agg_df['ratio'] = agg_df['ctotalw'] / agg_df['ctotalm']
#
agg_df.drop(columns=['ctotalm', 'ctotalw'], inplace=True)
agg_df = agg_df.unstack()
agg_df.sort_values(ascending=True, by=('ratio', 2011), inplace=True)

mytab = tabulate(
    agg_df,
    ['Major', '2011', '2019'],
    tablefmt='latex',
    floatfmt='.2f'
)

# %%
with open(tex_img_path + '/rat_11.tex', 'w') as file:
    file.write(mytab)

# %%
# I also save a version of this table to save onto my USB and make a
# scatterplot with NCES data.
if __name__ == '__main__':
    nces_notes_path = (
        '/Users/tarasullivan/Documents/dissertation/nces_notes/tables/'
    )
    file = nces_notes_path + 'tab_rat_2011.csv'
    agg_df.droplevel(level=0, axis=1).to_csv(file)
