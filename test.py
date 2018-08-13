import re

question_body = "ناززنیننننن"
alphabet = ['ض','ص','ث','ق','ف','غ','ع','ه','خ','ح','ج','چ','ش','س','ی','ب','ل','ا'
        ,'ت','ن','م','ک','گ','ظ','ط','ز','ر','ذ','د','پ','و']
for char in alphabet:
    reg = char+char+char+'('+char+'*'+')'
    question_body = re.sub(reg,char, question_body)

print(question_body)