# cheatingScanner
Finds cheaters in a set of student scantron data

This program accepts a CSV file in Eduphoria format, and displays
an interactive scatterplot. Each point on the plot represents the 
number of shared incorrect and correct answers on a multiple choice
scantron exam. 

An exam administration without any cheating will, presumably, have 
many students who share the same correct answers. One would hope 
after all that most of the students pass the exam. Comparing a
suspected cheater's exam to another students by looking at how 
how many questions they have in common does not tell us much information.

However, if every students exam is compared against every other exam,
cheating becomes easier to identify. A student who has copied another 
students answers will share their incorrect answers as well as their
correct ones at a rate much higher than the general testing population.

This program includes a sample eduphoria CSV file to use for testing.
Pipe the file into CheatScanner.py through std.in to see the graph.
After the graph is closed, the program will print the results to std.out
for further analysis.

The data here is from an actual exam, although false alliterative names
and random ID numbers have been swapped out for the students real 
identification. The student pair "Laronda Labarbera" and "Kathline Keehn"
shared a remarkable 15 incorrect answers (upper right)! They also happened
to sit next to each other at the back of the class in the same period. 

Student pair "Deetta Delpiore" and "Man Mcdevitt" were also caught cheating
during the exam, although their scores were entered anyways for the sake of
this analysis.

