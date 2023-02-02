from src.services.user_login1.serializer import CsvSerializer

class PdfHelper():

    @classmethod
    def html_create(cls,request:CsvSerializer):
        html_string = '''
        <!DOCTYPE html>
        <html>
        <style>
            table {
            font-size: 12px;
            border-collapse: collapse;
            border-style: hidden;
            }
            table td {
            border: 2.4px solid rgba(255, 255, 255, 0.807);
            }
            table th {
            border: 2.4px solid rgba(255, 255, 255, 0.807);
            }
        </style>
        <body>
        <table>
        '''
        cur_report_ary = request.cur_report_ary
        cur_report_header_ary = request.cur_report_header_ary

        print(len(cur_report_ary))
        print(len(cur_report_header_ary))


        for i in range(len(cur_report_ary)):
            report_header_ary = cur_report_header_ary[i]
            html_string = html_string + f'''
            <tr>
                <td colspan="4" style="width: 25%; text-align: left">
                <b>Mortgage Marketshare Module Report - {report_header_ary[0]} </b> <br />
                {report_header_ary[2]}
                </td>
                <th colspan="6">Prepared for:TWG</th>
                <th colspan="3" style="width: 25%; text-align: right">{report_header_ary[3]}</th>
            </tr>
            <tr>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td></td>
                <td></td>
            </tr>
            <tr style="background-color: rgba(63, 63, 70, 0.141)">
                <th colspan="4">Rank by {report_header_ary[4]}</th>
                <th colspan="2">All Mortgages</th>
                <th colspan="2">Purchase Mortgages</th>
                <th colspan="2">Non-purchase Mortgages</th>
                <th colspan="3">mkt shr by {report_header_ary[4]}(%)</th>
            </tr>

            <tr style="background-color: rgba(63, 63, 70, 0.141)">
                <td style="width: 25%; text-align: left"><b>Broker Name</b></td>
                <th style="width: 3%; text-align: center">All</th>
                <th style="width: 3%; text-align: center">P</th>
                <th style="width: 3%; text-align: center">N</th>
                <th style="width: 10%; text-align: center">Total $</th>
                <th style="width: 10%; text-align: center">Total Num</th>
                <th style="width: 10%; text-align: center">Total $</th>
                <th style="width: 10%; text-align: center">Total Num</th>
                <th style="width: 10%; text-align: center">Total $</th>
                <th style="width: 10%; text-align: center">Total Num</th>
                <th style="width: 10%; text-align: center">All</th>
                <th style="width: 3%; text-align: center">P</th>
                <th style="width: 3%; text-align: center">N</th>
            </tr>'''
            for j in range (len(cur_report_ary[i])):
                report_ary = cur_report_ary[i][j]
                print(report_ary)
                html_string = html_string + f'''
                        <tr>
                            <td style="text-align: left">{report_ary[0]}</td>
                            <td style="text-align: center">{report_ary[1]}</td>
                            <td style="text-align: center">{report_ary[2]}</td>
                            <td style="text-align: center">{report_ary[3]}</td>
                            <td style="text-align: right">{report_ary[4]}</td>
                            <td style="text-align: right">{report_ary[5]}</td>
                            <td style="text-align: right">{report_ary[6]}</td>
                            <td style="text-align: right">{report_ary[7]}</td>
                            <td style="text-align: right">{report_ary[8]}</td>
                            <td style="text-align: right">{report_ary[9]}</td>
                            <td style="text-align: right">{report_ary[10]}</td>
                            <td style="text-align: right">{report_ary[11]}</td>
                            <td style="text-align: right">{report_ary[12]}</td>
                        </tr>
                    '''                  
            html_string = html_string + '''</table> <hr/>
            <table style="margin-top: 50px">'''
        html_string = html_string +'''</table>
  </body>
</html>'''
        return html_string