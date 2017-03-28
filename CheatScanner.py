"""
CheatScanner 
By: Scott Grimes

This program reads in an Eduphoria csv file from std.in, and displays
an interactive graph via matplotlib. 

"""
import sys
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show

students = []
studentPair = []

class Student:
    #each Student object contains a name, ID number, and array of answers
    
    def __init__(self, name,id,answers):
        
        self.name = name[1].strip('/"')+' '+name[0].strip('/"')
        self.id = id
        self.answers = answers
        pass
    
    def __repr__(self):
        #a student object is printed as:
        #First Last | ID#
        return '{} {} | {} '.format(
            self.first_name,
            self.last_name,
            self.id)

class SharedAnswers:
    #a SharedAnswers object contains the number of shared
    #correct and incorrect answers between two students
    
    def __init__(self, student1, student2):
        
        self.student1 = student1
        self.student2 = student2
        
        self.shared_correct = 0
        self.shared_incorrect = 0
        
        #determines the number of shared correct and incorrect answers
        #between our two students
        for i, ans_1 in enumerate(student1.answers):
            ans_2 = student2.answers[i]
            
            #ignore blank answers
            if(ans_2 == ans_1 and
               ans_2 != '' and ans_1 != ''):
                
                if(ans_1[0] == '+'):
                    self.shared_correct+=1
                    
                else:
                    self.shared_incorrect+=1
        
        #self.label is used for printing our student pair on the graph
        self.label = '{},{} : {}\n{}'.format(
            self.shared_correct,
            self.shared_incorrect,
            self.student1.name,
            self.student2.name)
        
        #self.export is used to export our data point to a csv file
        #for further analysis
        self.export = '{},{},{},{}'.format(
            self.student1.name,
            self.student2.name,
            self.shared_correct,
            self.shared_incorrect)
    
def readInputFile():
    #reads in each row of our file from std.in
    #every row has the following format
    #LastName,FirstName,ID,Q1,Q2...Qn
    #Qn is a string with the students answer for question n
    #if the correct answer for a question was A:
    #Qn would be stored as '+A'
    #if the students answer was incorrect, their choice is saved but the + 
    #is ommitted: ie. answer was A, student response is 'B' 'C' or 'D'
    
    for line in sys.stdin:
        parsed = line.strip('/n').split(',')
        name = parsed[0:2] 
        id = parsed[2]
        answers = parsed[3:]
        students.append(Student(name,id,answers))
    
def compareAnswers():
    #compare all possible student combinations, append the shared answers object
    #between them to our list studentPair
    for (i, s1) in enumerate(students):
        for (j, s2) in enumerate(students[i:]):
            sys.stdout.write('Processing: '+str(round(i/len(students)*100,0))+'%\r')
            sys.stdout.flush()
            if s1 is not s2:
                studentPair.append(SharedAnswers(s1,s2))
    
    sys.stdout.write('Processing Complete!\r')
    sys.stdout.flush()

class graphResults():  
    #creates a matlibplot graph with two sections
    #the left section is a scatterplot of the correct
    #and inccorrect shared answers between every student
    
    #the right section displays the students names when a point on 
    #the scatterplot is clicked on
    
    def __init__(self,studentPair): 
        #arrays of correct and incorrect answers to be plotted
        self.corr = [i.shared_correct for i in studentPair]
        self.incorr = [i.shared_incorrect for i in studentPair] 
        
        #label for each coordinate pair
        self.annotes = [s.label for s in studentPair]
        
        #text to be displayed on the right hand side
        self.ann_text = 'Click on a data point'
    
        #setting up our window for plotting
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(122)
        self.ax2 = self.fig.add_subplot(121)
        self.visible = False
        
        #plots each half of our window
        self.plotSecond()
        self.plotFirst()
        
        #when a mousedown even happens on a point, update the text
        #which is displayed on the right hand subplot
        self.fig.canvas.mpl_connect('pick_event',self.pickMe)
        plt.show()
        
    
    def pickMe(self,event):
        #updates the text which is displayed on our right subplot
        #to display the students names which were selected
        
        #id number of our coordinate point (multiple possible if they overlap)
        ind = event.ind 
        
        #get student labels, store into ann_text
        ann_text = [self.annotes[i] for i in ind]
        
        #temp coords to plot a red dot to show our selected point
        px = [self.corr[i] for i in ind]
        py = [self.incorr[i] for i in ind]
        pointcolor = 'red'
        
        #determine if we have selected a dot or not
        if self.visible is False:
            self.visible = True
            self.ann_text = '\n'.join(ann_text)
        else:
            self.ann_text = 'Click on a data point'
            self.visible = False
            pointcolor = 'blue'
        
        #update our screen
        self.plotSecond()
        self.plotFirst()
        self.ax2.scatter(px,py, color = pointcolor)
        event.canvas.draw()
    
    
    def plotSecond(self):
        #displays the text in the right subplot
        self.ax1.cla()
        self.ax1.title.set_text('Selected Pair(s)')
        self.ax1.text(0.5, 0.5, self.ann_text, size=10, ha='center', va='center')
        self.ax1.axis('off')
        
    
    def plotFirst(self):
        #displays the scatterplot of student pairs
        self.ax2.cla()
        self.ax2.scatter(self.corr,self.incorr, color = 'blue',picker = True)
        self.ax2.title.set_text('Shared Answers')
        self.ax2.set_xlabel('Correct')
        self.ax2.set_ylabel('Incorrect') 
        
    

readInputFile()
compareAnswers()
graphResults(studentPair)

#optional section, prints results to std.out for further analysis
#can be saved as a csv
for i in studentPair:
    print(i.export)

    
