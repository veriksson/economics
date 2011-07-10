from __future__ import division
import Image,ImageDraw
import cStringIO
import cgi
import csv
from datetime import datetime

X,Y = 500, 200 #image width and height

from collections import namedtuple

Month = namedtuple("Month", ["date", "income","expenses", "net"])

def parse_file(name):
    months = []
    reader = csv.reader(open(name, "rb"), delimiter=",")
    for row in reader:
        date, income, expense, net = row
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        months.append(Month(date, float(income), float(expense), float(net)))
    return months

def highest(months):
    return max(months, key= lambda x: x.income)

def lowest(months):
    return min(months, key = lambda x: x.expenses)

def mfactor(midpoint, highest):
    midpoint -= 5 # just so the "roof" is lowered
    return midpoint / highest

def draw_legend(draw):
     # draw legend
    draw.rectangle((0,Y-85, 80, Y-30), fill="white", outline="#aaa")
    draw.text((25, Y-85), "Legend", fill="black")
    # income legend
    draw.rectangle((5, Y-75, 10, Y-65), fill="green")
    draw.text((15, Y-75), "Income", fill="green")
    # expense legend
    draw.rectangle((5,Y-60, 10, Y-50), fill="red")
    draw.text((15, Y-60), "Expenses", fill="red")
    # net legend
    draw.rectangle((5,Y-45, 10, Y-35), fill="orange")
    draw.text((15, Y-45), "Net", fill="orange")

   
def graph(legend=False):
    img = Image.new("RGB", (X,Y), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    midpoint = Y / 2
    months = parse_file("a:/out.csv")

    # highest income
    h = highest(months)

    # highest expense
    l = lowest(months)

    #spacing
    skip = int(X / len(months))
    
    # multiplication factor
    # We need to check whichever is highest, income or expense. 
    # invert expense so it's positive
    hf = mfactor(midpoint, max(h.income, (l.expenses*-1)))

    #  width of bars, -1 so theres some spacing between months
    width = int(skip/3)-1

    # draw back-lines
    for i in xrange(0, X, int(skip)):
        draw.line((i, 0, i, Y), fill="#ccc")

    # current step
    curr = 0
    for i,m in enumerate(months):
        
        # print month numbers
        draw.text((curr, Y-10), m.date.strftime("%m"), fill="black")
        # draw income
        income_top = m.income*hf

        draw.rectangle((curr+1, 
                        midpoint, 
                        curr+width, 
                        midpoint-income_top), fill="green")

        # draw expenses
        expenses_low = (m.expenses) * hf

        draw.rectangle((curr+width+1, 
                        midpoint, 
                        curr+width*2, 
                        midpoint-expenses_low), fill="red")
        
        net_f = m.net * hf
        draw.rectangle((curr+(width*2)+2, 
                        midpoint, 
                        curr+width*3+1, 
                        midpoint-net_f), fill="orange")

        curr += skip


    draw.line((0,midpoint, X, midpoint), fill="#aaa")
    

    if legend:
        draw_legend(draw)

    f = cStringIO.StringIO()
    img.save(f, "PNG")
    f.seek(0)

    #output to browser
    print "Content-type: image/png\n"
    print f.read()

if __name__ == "__main__":
    try:
        form = cgi.FieldStorage()
        if "legend" in form:
            graph(True)
        else:
            graph()
    except Exception, e:
        print "Content-type: text/html\n"
        print """<html><body>%s</body></html>""" % e

