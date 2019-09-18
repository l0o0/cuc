import re
from datetime import datetime



class TaskLine(object):
    def __init__(self):
        # completion mark
        self.re_mask = re.compile("^x")
        # priority indicats by an uppercase character from A to Z
        self.re_priority = re.compile('^x?(\([A-Z]\))\s')
        # completion date and creation date
        # completion date appears first if completion date exists
        self.re_dates = re.compile("\s([1-9][0-9]{3}-[0-9]{2}-[0-9]{2})(?=\s|$)")
        # non-whitespace characters starts with +
        self.re_projects = re.compile("\s(\+\S+)")
        # non-whitespace characters starts with @
        self.re_contexts = re.compile("\s(@\S+)")
        # non-wihtespace characters separated by :
        self.re_keyvalues = re.compile("\s(\S*?:\S*)")
        # default style 
        self.default_style = {'priority':{
                                '(A)' : '#FFD700',
                                '(B)' : '#FF7F50',
                                '(C)' : '#3CB371',
                                '(D)' : '#1E90FF'
                            },
                            'completion_date':'#B22222',
                            'creation_date':'green',
                            'content':'black',
                            'project':'#e74c3c',
                            'context':'#3498db',
                            'keyvalue':{
                                'k':'#800080',
                                'v':'#800080'
                            }}
    

    def parser(self, plain_text):
        break_len = 0
        self.plain_text = plain_text.strip()  

        # handle mask 
        self.mask = self.re_mask.search(self.plain_text)
        if self.mask:
            self.mask = self.mask.group()
            self.status = 'done'
        else:
            self.mask = None 

        # handle priority 
        self.priority = self.re_priority.search(self.plain_text)
        if self.priority:
            self.priority = self.priority.groups()[0] 
        else:
            self.priority = None 

        # handle dates
        self.dates = self.re_dates.findall(self.plain_text)
        if len(self.dates) == 2:
            self.completion_date = datetime.strptime(self.dates[0], '%Y-%m-%d')
            self.creation_date = datetime.strptime(self.dates[1], '%Y-%m-%d')
        elif len(self.dates) == 1:
            self.completion_date = None
            self.creation_date = datetime.strptime(self.dates[0], '%Y-%m-%d')
        else:
            self.completion_date = None 
            self.creation_date = None

        # handle projects 
        self.projects = self.re_projects.findall(self.plain_text)
        if not self.projects:
            self.projects = None 

        # handle contexts 
        self.contexts = self.re_contexts.findall(self.plain_text)
        if not self.contexts:
            self.contexts = None  

        # handle key:value pairs
        self.keyvalues = self.re_keyvalues.findall(self.plain_text)
        if not self.keyvalues:
            self.keyvalues = None
        # retrive content by remove another elements parts
        tmp = self.re_mask.sub('', self.plain_text)
        tmp = self.re_dates.sub('', tmp)
        tmp = self.re_priority.sub('', tmp)       
        tmp = self.re_projects.sub('', tmp)
        tmp = self.re_contexts.sub('', tmp)
        tmp = self.re_keyvalues.sub('', tmp)
        self.content = tmp 
        

    def enrich_text(self, style=None):
        if style == None:
            style = self.default_style
        rich_text = ""
        if self.priority:
            rich_text = "<b><font color=%s>%s</font></b> " % (
                style['priority'][self.priority], self.priority
                )
        if self.completion_date:
            if self.completion_date.year == datetime.now().year:
                rich_text = rich_text + "<font color=%s>%s</font> " % (
                    style['completion_date'], datetime.strftime(self.completion_date, '%Y-%m-%d')[5:]
                )
            else:
                rich_text = rich_text + "<font color=%s>%s</font> " % (
                    style['completion_date'], datetime.strftime(self.completion_date, '%Y-%m-%d')
                )

        if self.creation_date:
            if self.creation_date.year == datetime.now().year:
                rich_text = rich_text + "<font color=%s>%s</font> " % (
                    style['creation_date'], datetime.strftime(self.creation_date, '%Y-%m-%d')[5:]
                )
            else:
                rich_text = rich_text + "<font color=%s>%s</font> " % (
                    style['creation_date'], datetime.strftime(self.creation_date, '%Y-%m-%d')
                )

        # break line if content is too long
        rich_text = rich_text + self.content + ' '

        if self.projects:
            for i in range(len(self.projects)):
                p = self.projects[i]
                rich_text = rich_text + "<font color=%s>%s</font> " % (
                    style['project'], p
                )

        if self.contexts:
            for i in range(len(self.contexts)):
                p = self.contexts[i]
                rich_text = rich_text + "<font color=%s>%s</font> " % (
                    style['context'], p
                )
        
        if self.keyvalues:
            for i in range(len(self.keyvalues)):
                k, v = self.keyvalues[i].split(':')
                rich_text = rich_text + "<font color=%s>%s</font>:<font color=%s>%s</font> " % (
                    style['keyvalue']['k'], k, style['keyvalue']['v'], v
                )
        return rich_text


    def format_text(self):
        text = "%s%s %s %s %s" % (
            self.mask if self.mask else "", 
            self.priority if self.priority else "", 
            datetime.strftime(self.completion_date, '%Y-%m-%d') if self.completion_date else "", 
            datetime.strftime(self.creation_date, '%Y-%m-%d') if self.creation_date else "", 
            self.content
            )

        text = re.sub('\s{2,}', ' ', text.strip())
        
        if self.projects:
            for i in range(len(self.projects)):
                p = self.projects[i]
                text = text + " " + p

        if self.contexts:
            for i in range(len(self.contexts)):
                p = self.contexts[i]
                text = text + " " + p
        
        if self.keyvalues:
            for i in range(len(self.keyvalues)):
                k, v = self.keyvalues[i].split(':')
                text = text + " " + k + ':' + v
        return text



class Tasks(object):
    def __init__(self, todotxt, donetxt):
        self.todotxt = todotxt
        self.donetxt = donetxt

    
    def readFromFile(self):
        self.tasklines = []
        with open(self.todotxt, encoding='utf-8') as handle:
            for line in handle.readlines():
                t = TaskLine()
                t.parser(line)
                self.tasklines.append(t)
            
        
    def saveToFile(self):
        writelines = [t.format_text() + '\n' for t in self.tasklines]
        print('all lines to write', writelines)       
        with open(self.todotxt, 'w', encoding='utf-8') as handle:          
            handle.writelines(writelines)
        print('save todo.txt')


    def saveDoneTask(self, taskline):
        text = taskline.format_text()
        text += '\n'
        with open(self.donetxt, 'a', encoding='utf-8') as handle:
            handle.write(text)

    
    def taskSort(self, bypart):
        pass




if __name__ == '__main__':
    s = '(A) 2019-09-01 2019-08-31 call kitty @phone +project1 +project2 due:test'
    s1 = 'x(A) 2019-09-01 2019-08-31 call kitty @phone +pro1 +pro1 due:test @try'

    t1 = TaskLine()
    t1.parser(s)
    t2 = TaskLine()
    t2.parser(s1)

    print(s)
    print(t1.mask)
    print(t1.priority)
    print(t1.completion_date)
    print(t1.creation_date)
    print(t1.content)
    print(t1.projects)
    print(t1.contexts)
    print(t1.keyvalues)

    print(s1)
    print(t2.mask)
    print(t2.priority)
    print(t2.completion_date)
    print(t2.creation_date)
    print(t2.content)
    print(t2.projects)
    print(t2.contexts)
    print(t2.keyvalues)