import urllib
import re

url = 'http://library.columbia.edu/locations.html'
html = urllib.urlopen(url).read()

# Find strings in the html with email addresses in them
emailList = list()
emails = re.findall('[a-zA-Z0-9]\S*@\S*[a-zA-Z]', html)
for item in emails:
    emailList.append(str(item))
 
count = 0  
for item in emailList:
    # Remove html header data
    mPos = item.find('>')
    if mPos == -1:
        text = item
    else: 
        text = item[mPos+1:]
        
        
    # Remove html footer data
    mPos = text.find('<')
    if mPos == -1:
        text = text        
    else: 
        text = text[:mPos]
    
    # Replace the current list item with header and footer data stripped out
    emailList[count] = text
    
    # Increment the counter    
    count = count +1

# Look for library names based on their proximity to email addresses    
libName = list()
libNdx = list()
count = 0  
for item in emailList:
    emailPos = html.find(item)
    
    
    # Check for multiple libraries using the same email
    numEmails = len(re.findall(item, html))
    if count > 0 and numEmails > 2:
        if emailList[count] == emailList[count-1]:
            oneNdx = html.find(item, libNdx[count-1]+2, len(html))
            emailPos = html.find(item, oneNdx+2, len(html))
            
    rPos = html.rfind('</strong>', 0, emailPos)
    lPos = html.rfind('<strong>', 0, emailPos)
    libName.append(html[lPos+8:rPos])

    libNdx.append(emailPos)
    count += 1
 
# Remove ampersand formatting
count = 0
for item in libName:
    ampPos = item.find('&amp;')
    if ampPos == -1:
        newText = item
    else:
        newText = item[0:ampPos-1] + ' &' + item[ampPos+5:len(item)]
    
    libName[count] = newText
    count += 1

# Remove new line formatting
count = 0
for item in libName:
    flag = 0
    while flag !=  1:
        nlPos = item.find('\n')
        if nlPos == -1:
            newText = item
            flag = 1
        else:
            newText = item[0:nlPos] + item[nlPos+1:len(item)]
            item = newText
    
        libName[count] = newText
        
    count += 1
    
 # Remove carriage formatting
count = 0
for item in libName:
    flag = 0
    while flag !=  1:
        nlPos = item.find('<br />')
        if nlPos == -1:
            newText = item
            flag = 1
        else:
            newText = item[0:nlPos] + item[nlPos+6:len(item)]
            item = newText
    
        libName[count] = newText
    
    count += 1
 
# Print library names and email addresses
count = 0
print '\n'
for item in libName:
    print item + ': ' + emailList[count]
    count += 1
