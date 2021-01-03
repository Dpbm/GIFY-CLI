import xlsxwriter
import os


async def create_xlsx(titles, visualizations, dates, likes, dislikes, comments, links, directory, OUTPUT_FILE_NAME):
    output = xlsxwriter.Workbook(f'{os.path.join(directory, OUTPUT_FILE_NAME)}.xlsx')
    worksheet = output.add_worksheet()
            
            
    header = {
        "A" : "Title",
        "B" : "Visualizations",
        "C" : "Date",
        "D" : "Likes in video",
        "E" : "Deslikes in Video",
        "F" : "Amount of comments",
        "G" : "Link"
    }
            
    for i in header.keys():
        worksheet.write(f'{i}1', header[i])
            

    for i in range(len(links)):
        worksheet.write(f'A{i+2}', titles[i])
        worksheet.write(f'B{i+2}', visualizations[i])
        worksheet.write(f'C{i+2}', dates[i])
        worksheet.write(f'D{i+2}', likes[i])
        worksheet.write(f'E{i+2}', dislikes[i])
        worksheet.write(f'F{i+2}', comments[i])
        worksheet.write(f'G{i+2}', links[i])

    worksheet.write_formula(f'B{len(links)+2}', '{=SUM(B2:B%i)}'%(len(links)+1))
    worksheet.write_formula(f'D{len(likes)+2}', '{=SUM(D2:D%i)}'%(len(likes)+1))
    worksheet.write_formula(f'E{len(dislikes)+2}', '{=SUM(E2:E%i)}'%(len(dislikes)+1))
    worksheet.write_formula(f'F{len(comments)+2}', '{=SUM(F2:F%i)}'%(len(comments)+1))



    output.close()