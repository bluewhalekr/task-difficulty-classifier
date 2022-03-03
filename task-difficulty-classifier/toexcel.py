import datetime

import xlsxwriter
import pandas as pd

from tools.summary import get_instance_count
from tools.summary import get_folder_analysis
from tools.summary import get_agg_table
from tools.summary import get_piechart_imgdata
from tools.summary import get_countplot_imgdata
from tools.summary import get_histogram_imgdata


def cvt_df_to_excel(df, dst_path, prj_title):
    writer = pd.ExcelWriter(dst_path, engine='xlsxwriter')
    
    # Extract aggregated table and attach to worksheet 'Summary'
    df_instance = get_instance_count(df, 'labels')
    df_instance.to_excel(
        writer, sheet_name='Summary', startrow=31, startcol=2
        )
    get_agg_table(df, 'n_instance').to_excel(
        writer, sheet_name='Summary', startrow=31, startcol=8
        )
    get_agg_table(df, 'avg_size_ratio').to_excel(
        writer, sheet_name='Summary', startrow=31, startcol=13
        )
    get_agg_table(df, 'avg_n_occlusion').to_excel(
        writer, sheet_name='Summary', startrow=31, startcol=18
        )
    get_agg_table(df, 'n_instance', groupby='difficulty').to_excel(
        writer, sheet_name='Summary', startrow=63, startcol=7
        )
    get_agg_table(df, 'avg_size_ratio', groupby='difficulty').to_excel(
        writer, sheet_name='Summary', startrow=63, startcol=12
        )
    get_agg_table(df, 'avg_n_occlusion', groupby='difficulty').to_excel(
        writer, sheet_name='Summary', startrow=63, startcol=17
        )
    
    # Extract Folder analysis and attach to worksheet 'Folder Analysis'
    get_folder_analysis(df).to_excel(writer, sheet_name='Folder Analysis')

    # Attach raw dataframe to worksheet 'Task Difficulty Raw Data'
    df.to_excel(writer, sheet_name='Task Difficulty Raw Data')
    
    # Define worksheets
    workbook = writer.book
    w_summary = writer.sheets['Summary']
    w_folder = writer.sheets['Folder Analysis']
    w_raw = writer.sheets['Task Difficulty Raw Data']
    
    # Set Column Width
    w_summary.set_column(1, 100, 14)
    w_summary.set_column(6, 6, 8)
    w_summary.set_column(11, 11, 8)
    w_summary.set_column(16, 16, 8)
    w_folder.set_column(1, 1, 25)
    w_folder.set_column(2, 5, 15)
    w_raw.set_column(1, 1, 25)
    w_raw.set_column(2, 2, 70)
    w_raw.set_column(3, 100, 15)
    
    # Attach charts to worksheet 'Summary'
    img_inst_cnt = get_piechart_imgdata(df_instance)
    w_summary.insert_image(11, 1, '', {'image_data': img_inst_cnt})
    
    img_inst = get_countplot_imgdata(df, 'n_instance')
    w_summary.insert_image(11, 6, '', {'image_data': img_inst})
    
    img_size = get_histogram_imgdata(df, 'avg_size_ratio')
    w_summary.insert_image(11, 11, '', {'image_data': img_size})

    img_occlusion = get_histogram_imgdata(df, 'avg_n_occlusion')
    w_summary.insert_image(11, 16, '', {'image_data': img_occlusion})
    
    img_inst_groupby = get_countplot_imgdata(df, 'n_instance', 'difficulty')
    w_summary.insert_image(43, 6, '', {'image_data': img_inst_groupby})
    
    img_size_groupby = get_histogram_imgdata(df, 'avg_size_ratio', 'difficulty')
    w_summary.insert_image(43, 11, '', {'image_data': img_size_groupby})
    
    img_occlusion_groupby = get_histogram_imgdata(df, 'avg_n_occlusion', 'difficulty')
    w_summary.insert_image(43, 16, '', {'image_data': img_occlusion_groupby})

    # Set proejct title format
    prj_title_format = workbook.add_format({
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Malgun Gothic (본문)',
        'font_size': 20,
        'bold': True,
        'bg_color': '#4C0099', #'#0080FF'
        'font_color': 'white'
    })
    w_summary.merge_range('B4:U6', prj_title, prj_title_format)
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    w_summary.write('B3', date_time)

    # Set title format
    title_format = workbook.add_format({
        'top': 6,
        'bottom': 6,
        'align': 'center',
        'valign': 'vcenter', 
        'font_name': 'Malgun Gothic (본문)',
        'font_size': 16,
        'bold': True,
    })
    w_summary.merge_range('B8:U9', 'Overview', title_format)
    w_summary.merge_range('H40:U41', '작업 난이도별 비교', title_format)    

    # Set subtitle format
    subtitle_format = workbook.add_format({
        'font_name': 'Malgun Gothic (본문)',
        'font_size': 12,
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#8A2BE2',
        'font_color': 'white'
    })
    w_summary.merge_range('B11:F11', '클래스별 인스턴스 분포', subtitle_format)
    w_summary.merge_range('H11:K11', '인스턴스 수 분포 (단위: Task)', subtitle_format)
    w_summary.merge_range('M11:P11', '평균 인스턴스 사이즈 비율 분포 (단위: Task)', subtitle_format)
    w_summary.merge_range('R11:U11', '평균 폐색 인스턴스 수 분포 (단위: Task)', subtitle_format)
    w_summary.merge_range('H43:K43', '인스턴스 수 분포 (단위: Task)', subtitle_format)
    w_summary.merge_range('M43:P43', '평균 인스턴스 사이즈 비율 분포 (단위: Task)', subtitle_format)
    w_summary.merge_range('R43:U43', '평균 폐색 인스턴스 수 분포 (단위: Task)', subtitle_format)
    
    writer.save()

    print('STEP 3: EXPORTING TO EXCEL IS COMPLETED')