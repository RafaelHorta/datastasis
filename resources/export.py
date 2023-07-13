import xlsxwriter

class ExportList:

    def __init__(self, filename):
        self._workbook = xlsxwriter.Workbook(filename)
        self._format_heading = self._workbook.add_format({
            'bold': True,
            'font_size': 16,
            'font_color': "#F1DADA",
            'align': "center",
            'valign': "center",
            'bg_color': "#622423",
            'border': 1
        })
        self._format_content = self._workbook.add_format({
            'font_size': 12,
            'border': 1,
            'align': "center",
        })

    def add_worksheet(self, heading : list, content : list, sheetname = None):
        row = 0
        worksheet = self._workbook.add_worksheet(sheetname)

        for i, item in enumerate(heading):
            worksheet.write(0, i, item, self._format_heading)

        for row, item in enumerate(content):
                row += 1

                for col, data in enumerate(item):
                    worksheet.write(row, col, data, self._format_content)

        self._workbook.close()
