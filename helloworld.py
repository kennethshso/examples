#This is a test 123456
import csv
import re
import os

accounts = ["ccb-joint","ccb-fandy","hsbc-joint","hsbc-ken","hsbc-fandy"]

inpath = "h:/working/python/data/indata/"
outpath = "h:/working/python/data/outdata/"

def loadchequelist(in_filename):
   print(in_filename)
   chequelist = readfile(in_filename)
   return chequelist;
   
def readfile(in_filename):
   "read an input file"
   with open(in_filename) as f:
      reader = csv.reader(f, delimiter="\t")
      mylist = list(reader)
   return mylist;

def isDetail(myLine,template):
   ###
   ### Check if the line is a detail line
   ###
   if template == "ccb":
      print("*****"+myLine[0])
      if myLine[0] == "Total":
         return False
      if myLine[0] == "Date":
         return False
   elif template == "hsbc":
      if myLine[0] == "Date":
         return False
      myLine[1] = myLine[1].strip()
      print("***" + myLine[1] + "***")
      if myLine[1] == "Opening Balance":
         return False
      if myLine[1] == "Closing Balance":
         return False
   return True;

def convertlist(sourcelist,template):
   newlist = []
   for l in sourcelist:
      if isDetail(l,template):
         newline = convertline(l,template)
         newlist.append(newline)
   return newlist;

def convertline(sourceline,template):
   newline = []
   if template == "ccb":
      date = sourceline[0]
      txndesc = sourceline[1]
      credit = sourceline[2]
      debit = sourceline[3]
   elif template == "hsbc":
      date = sourceline[0]
      txndesc = sourceline[1]
      credit = sourceline[2]
      debit = sourceline[3]
   else:
      print("Unknown template: " + template)
      return
   txntype = getTxnType(sourceline[1])
   credit = credit.replace(',','')
   debit = debit.replace(',','')
   newline.append(date) #date
   newline.append(txndesc) #desc
   newline.append(credit) #credit
   newline.append(debit) #debit
   newline.append(txntype)
   return newline;

def getTxnType(txndesc):
   if txndesc == "INTEREST PAYMENT":
      return "Income"
   if txndesc == "CREDIT INTEREST":
      return "Income"
   if txndesc == "DEPOSIT - SO SHIU HUNG":
      return "Trasnfer-in"
   if txndesc == "DEPOSIT - MR SO SHIU HUNG":
      return "Trasnfer-in"
   if txndesc == "DEPOSIT - MR SO SHIU HUNG AND":
      return "Trasnfer-in"
   if txndesc == "LOAN PAYMENT DEBIT - PMT LOAN 000000806455 1":
      return "Trasnfer-out"
   if re.match(r"DEPOSIT - #[0-9]",txndesc):
      return "Income"
   if re.match(r"CORP EVT PAYMENT SEC     400326930380",txndesc):
      return "Income"
   if re.match(r"ATM WITHDRAWAL",txndesc):
      return "Expense"
   if re.match(r"PPS",txndesc):
      return "Expense"
   if re.match(r"EPS",txndesc):
      return "Expense"
   type = "Unknown"
   return type;

def writefile(a, d):
   ###
   ### Write file
   ###
   outfile = open(out_filename,"a") 
   for wn in d: 
      str = ','.join(wn)
      outfile.write(a + "," + str + '\n')

   outfile.close() 

###
### Main
###
chequelist = loadchequelist(inpath + "cheque.txt")
for a in accounts:
   temp = a.split("-")
   template = temp[0]
   print(template)
   in_filename = inpath + a + "-201808.txt"
   out_filename = outpath + "201808.csv"

   #os.remove(out_filename)
   sourcelist = readfile(in_filename)
   newlist = convertlist(sourcelist,template)
   writefile(a, newlist)
   print(a+"...Done")