from sys import argv
import re

def wrap(text,tag,html_attributes={}):
	attr_text = ' '.join(['{}="{}"'.format(k,v) for k,v in html_attributes.items()])

	return "<{} {}>{}</{}>".format(tag,attr_text,text,tag)

def time_24_to_12(timestring):
	h24,m = timestring.split(":")

	h12 = 12 if h24 in ['12','0','00'] else int(h24) % 12
	return "{}:{}{}".format(h12,m,'am' if int(h24) < 12 else 'pm')

def re_clean_time(txt):
	# handle time ranges
	range_match = r'\d+:\d+-\d+:\d+'

	txt = re.sub(range_match,lambda m: wrap(m[0],"span",{"class":"time"}) + "<br>",txt)

	# handle individual times not in ranges AFTER ranges are handled
	indiv_match = r'\d+:\d\d(?:[^<-])'
	txt = re.sub(indiv_match,lambda m: wrap(m[0],"span",{"class":"time"}) + "<br>",txt)

	# convert 24h to 12h
	generic_match = r'\d+:\d+'
	txt = re.sub(generic_match,lambda m: time_24_to_12(m[0]),txt)

	return txt


# replace "||" with a line break
def re_force_breaks(txt):
	return re.sub(r'\|\|','<br>',txt)

def full_clean(htmlText):
	txt = re_clean_time(htmlText)
	txt = re_force_breaks(txt)

	return txt


def main():
	with open(argv[1],'r+') as fp:
		htmlText = fp.read()

		cleaned_text = full_clean(htmlText)

	with open(argv[1],'w') as outfp:
		outfp.write(cleaned_text)



if __name__=='__main__':
	main()