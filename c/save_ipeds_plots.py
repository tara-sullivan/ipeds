# Male dominated fields in IPEDS
import matplotlib.pyplot as plt
import tikzplotlib as tpl

import codecs

# %%
# Set image path
import os

dirname = os.path.dirname(__file__)
tex_img_path = os.path.join(dirname, 'fig_tex_code')
# %%
# Add items from img_tools
from img_tools.figsize import ArticleSize
size = ArticleSize()

from img_tools import plot_line_labels
plot_df = plot_line_labels.plot_df

from img_tools import tikzplotlib_functions as tplf
# import img.code.tikzplotlib_functions as tplf
add_begin_content = tplf.add_begin_content

# %%
# Add items from ipeds folder
from data.ipeds.c.clean_data.make_df import ReadData, MakeDict
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
# add_begin_content: moved to tplf


def add_end_content(filepath, plot_title=None, group_title=None,
                    title_space="1cm", source=None):
    '''
    Add end content, including:
       * plot title (better to use \\caption to define title) than pgfplots
       * a title for subplots, if a group plot
       * end the tikzpicture
       * add the caption
    '''
    with open(filepath, 'a+') as file_handle:
        # Edit strings that will be included
        caption = 'Source: IPEDS'
        if source is not None:
            caption = caption + '; ' + source

        content = file_handle.read()
        file_handle.seek(0, 0)

        if group_title is None:
            line = '\n\\end{tikzpicture}'
        else:
            line = '\\draw' \
                   + ' ($(my plots c1r1.north)!0.5!(my plots c2r1.north)' \
                   + ' + (0, ' + title_space + ')$)' \
                   + ' node {' + group_title + '};' \
                   + '\n\\end{tikzpicture}'

        if plot_title is not None:
            line = line + '\n\\caption{' + plot_title + '. ' + caption + '.}'
        # line = line + '\n\\caption*{' + caption + '}'
        file_handle.write('\n' + line.rstrip('\r\n') + '\n' + content)


def save_rateplot(filename, source=None, plot_title=None,
                  width=size.w(1.25), height=size.h(1.25),
                  extra_tikzpicture_parameters=None):
    tpl.clean_figure()
    filepath = os.path.join(tex_img_path, filename + '.tex')
    tpl.save(filepath, wrap=False, axis_height=height,
             axis_width=width,
             )
    add_begin_content(filepath,
                      extra_tikzpicture_parameters=extra_tikzpicture_parameters)
    add_end_content(filepath, source=source, plot_title=plot_title)


def save_areaplot(filename, title):
    tpl.clean_figure()
    filepath = os.path.join(tex_img_path, filename + '.tex')
    tpl.save(filepath, wrap=False,
             extra_axis_parameters={"height=180pt, width=150pt",
                                    "reverse legend",
                                    "legend style={"
                                    + "at={(2.02, 0.5)},"
                                    + "anchor=west,"
                                    + "}"},
             extra_groupstyle_parameters={"horizontal sep=0.8cm",
                                          "group name=my plots"},
             )
    add_begin_content(filepath)
    title_str = title + " - number Bachelor's degrees awarded (thousands)"
    add_end_content(filepath, title_str)


# def save_comboplot(cip_cls, filename, slide=True):
#     filepath = os.path.join(tex_img_path, filename + '.tex')
#     file_handle = codecs.open(filepath, 'w')
#
#     # Rate graph
#     cip_cls.plot_rate()
#     # To do: figure out why computer science ('11') raises error here
#     try:
#         tpl.clean_figure()
#     except ValueError:
#         pass
#
#     code = tpl.get_tikz_code(axis_height='140pt',
#                              axis_width='300pt',
#                              extra_tikzpicture_parameters=extra_tikzpicture_parameters,
#                              # axis_width='150pt',
#                              # extra_axis_parameters={'x post scale=2',
#                              #                        'y post scale=1'}
#                              )
#     file_handle.write(code)
#     file_handle.write('\n\\vspace{0.1cm}\n\\begin{tikzpicture}')
#     file_handle.close()
#
#     add_begin_content(filename, extra_tikzpicture_parameters=extra_tikzpicture_parameters)
#
#     # area graph
#     cip_cls.plot_area()
#     tpl.clean_figure()
#     code = tpl.get_tikz_code(
#         wrap=False,
#         extra_axis_parameters={"height=90pt, width=160pt",
#                                "reverse legend",
#                                "legend style={"
#                                + "at={(2.02, 0.5)},"
#                                + "anchor=west,"
#                                + "}"},
#         extra_groupstyle_parameters={"horizontal sep=0.8cm",
#                                      "group name=my plots"},
#     )
#     with open(filepath, 'a+') as file_handle:
#         content = file_handle.read()
#         file_handle.seek(0, 0)
#         file_handle.write('\n' + code + '\n' + content)
#     group_title = 'Number Bachelor\'s degrees awarded (thousands)'
#     add_end_content(filepath, group_title, title_space="0.25cm")

def save_comboplot(cip_cls, filename, slide=True):
    filepath = os.path.join(tex_img_path, filename + '.tex')
    file_handle = codecs.open(filepath, 'w')

    if slide:
        extra_tikzpicture_parameters = {}
        param_wrap=True
    else:
        extra_tikzpicture_parameters = {
            'every node/.style={font=\\footnotesize}',
            'align=left'
        }
        param_wrap=False

    # need to make the extratikzpicture params a list for group plot
    extra_tikzpicture_parameters_list = list(extra_tikzpicture_parameters)
    extra_tikzpicture_parameters_str = ''
    for i in extra_tikzpicture_parameters_list:
        extra_tikzpicture_parameters_str = (
                extra_tikzpicture_parameters_str
                + ' ' + str(i) + ',')

    # Rate graph
    cip_cls.plot_rate()
    # To do: figure out why computer science ('11') raises error here
    try:
        tpl.clean_figure()
    except ValueError:
        pass
    code = tpl.get_tikz_code(axis_height='140pt',
                             axis_width='300pt',
                             wrap=param_wrap,
                             # axis_width='150pt',
                             # extra_axis_parameters={'x post scale=2',
                             #                        'y post scale=1'}
                             )
    file_handle.write(code)
    file_handle.write('\n\n\\end{tikzpicture}')
    # Start tikzpicutre for the next graphs
    file_handle.write('\n\n\\vspace{0.1cm}\n\\begin{tikzpicture}')
    file_handle.write(f'[{extra_tikzpicture_parameters_str}]')
    file_handle.close()

    add_begin_content(filepath, extra_tikzpicture_parameters=extra_tikzpicture_parameters)
    # tplf.add_end_content(filepath)

    # file_handle = codecs.open(filepath, 'w')

    # area graph
    cip_cls.plot_area(ylabel='Num (1000s)')
    tpl.clean_figure()
    code = tpl.get_tikz_code(
        wrap=False,
        extra_tikzpicture_parameters=extra_tikzpicture_parameters,
        extra_axis_parameters={"height=90pt, width=160pt",
                               "reverse legend",
                               "legend style={"
                               + "at={(2.02, 0.5)},"
                               + "anchor=west,"
                               + "}"},
        extra_groupstyle_parameters={"horizontal sep=0.8cm",
                                     "group name=my plots"},
    )
    with open(filepath, 'a+') as file_handle:
        content = file_handle.read()
        file_handle.seek(0, 0)
        file_handle.write('\n' + code + '\n' + content)
    if slide:
        group_title = 'Number Bachelor\'s degrees awarded (thousands)'
    else:
        group_title = (
            'The top figure contains the ratio of women to men'
            ' completing bachelor\'s degree in the specified field.'
            ' The bottom figures contain the total number of bachelor\'s'
            ' degrees awarded in thousands for men and for women'
        )
    add_end_content(filepath, group_title, title_space="0.25cm")

# %%
if __name__ == '__main__':
    plt.close('all')

    # Test 1: n degrees
    plot_n_degrees()
    title_str = ('Number of Bachelor\'s Degrees awarded'
                 ' in US 4-year colleges')
    save_rateplot('n_degrees', source='NCES', plot_title=title_str)

    plt.show()

# %%

if __name__ == '__main__':
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
                      x_lim=2031, shareyflag=False,
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
