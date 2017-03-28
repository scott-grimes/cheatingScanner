import sys
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
students = []
studentPair = []

class Student:
    
    def __init__(self, name,id,answers):
        self.name = name[1].strip('/"')+' '+name[0].strip('/"')
        self.id = id
        self.answers = answers
        pass
    def __repr__(self):
        return '{} {} | {} '.format(
            self.first_name,
            self.last_name,
            self.id)

class SharedAnswers:
    
    def __init__(self, student1, student2):
        self.student1 = student1
        self.student2 = student2
        self.shared_correct = 0
        self.shared_incorrect = 0
        for i, ans_1 in enumerate(student1.answers):
            ans_2 = student2.answers[i]
            if(ans_2 == ans_1 and
               ans_2 != '' and ans_1 != ''):
                try:
                    if(ans_1[0] == '+'):
                        self.shared_correct+=1
                    else:
                        self.shared_incorrect+=1
                except Exception as e:
                    print('\''+ans_1+'\'')
                    print('\''+ans_2+'\'')
                    print(e)
        self.label = '{}/{} incorrect/correct : {} and {}'.format(
            self.shared_incorrect,
            self.shared_correct,
            self.student1.name,
            self.student2.name)
    
def readInputFile():
    
    for line in sys.stdin:
        parsed = line.strip('/n').split(',')
        name = parsed[0:2] #first two slots are lastname, firstname
        id = parsed[2]#third slot is ID number
        answers = parsed[3:]#remaining slots are answers
        students.append(Student(name,id,answers))
    
def compareAnswers():
    for (i, s1) in enumerate(students):
        for (j, s2) in enumerate(students[i:]):
            sys.stdout.write('Processing: '+str(round(i/len(students)*100,0))+'%\r')
            sys.stdout.flush()
            if s1 is not s2:
                studentPair.append(SharedAnswers(s1,s2))
    
    sys.stdout.write('Processing Complete!\r')
    sys.stdout.flush()

def graphResults():
    corr = [i.shared_correct for i in studentPair]
    incorr = [i.shared_incorrect for i in studentPair]    
    global annotes
    annotes = [s.label for s in studentPair]
    
    fig = plt.figure()
    ax2 = fig.add_subplot(121)
    ax1 = fig.add_subplot(122)
    coll = ax2.scatter(corr,incorr, color = 'blue',picker = True)
    
    
    class DataCursor(object):
        #modified from https://github.com/joferkington/mpldatacursor
        x, y = 0.0, 0.0
        xoffset, yoffset = -5, 5
        text_template = ''
    
        def __init__(self, ax):
            self.ax = ax
            self.annotation = ax.annotate(self.text_template, 
                    xy=(self.x, self.y), xytext=(self.xoffset, self.yoffset), 
                    textcoords='offset points', ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', fc='white')
                    )
            self.annotation.set_visible(False)
            self.visible = False
    
        def __call__(self, event):
            
            if self.visible is False:
                self.visible = True
                ind = event.ind 
                global annotes
                annotation_text = [annotes[i] for i in ind]
                annotation_text = '\n'.join(annotation_text)
                self.x, self.y = event.mouseevent.xdata, event.mouseevent.ydata
                if self.x is not None:
                    self.annotation.xy = self.x, self.y
                    self.annotation.set_text(annotation_text)
                    self.annotation.set_visible(True)
                    event.canvas.draw()
            else:
                self.visible = False
                self.annotation.set_visible(False)
                event.canvas.draw()
               
    
    ax1.title.set_text('Selected Pair(s)')
    ax2.title.set_text('Shared Incorrect/Correct Answers')
    fig.canvas.mpl_connect('pick_event',DataCursor(ax2))
    
    plt.show()

readInputFile()
compareAnswers()
graphResults()

    
