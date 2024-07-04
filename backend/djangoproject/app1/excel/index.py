import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', 1000, 'qw', 'qw', 123],
    ['Gas',   100, 'qw', 'qw', 123],
    ['Food',  300, 'qw', 'qw', 123],
    ['Gym',    50, 'qw', 'qw', 123],
)

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for item, cost, val1, val2, val3 in (expenses):
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, cost)
    worksheet.write(row, col + 2, val1)
    worksheet.write(row, col + 3, val2)
    worksheet.write(row, col + 4, val3)
    row += 1

# Write a total using a formula.
#worksheet.write(row, 0, 'Total')
# worksheet.write(row, 1, '=SUM(B1:B4)')

workbook.close()
