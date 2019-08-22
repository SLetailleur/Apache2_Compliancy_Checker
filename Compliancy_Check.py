#/usr/bin/python3

from Checker_output import checker
from terminaltables import AsciiTable

Output = []
def main():
	check = checker.Checkers()
	Output.append(['Checked Item', 'Current Value', 'Comment', "Status"])
	Output.append(check.OsCheck())
	Output.append(check.VersionCheck())
	Output.append(check.SiteSimpleCheck())
	Output.append(check.ModsSimpleCheck())
	Output.append(check.SSLCheck())
	table = AsciiTable(Output)
	print (table.table)


if __name__== "__main__":
   main()



