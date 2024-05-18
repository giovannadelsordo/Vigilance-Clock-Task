This task is a modified version of the Mackworth Clock Task (Mackworth, 1948). In this task, a clock hand moves circularly and regularly every second. On some trials, the clock makes a double jump (instead of moving 4°, it moves 8°). The participants are instructed to press the spacebar whenever a double jump occurs. In this version of the task, feedback is provided throughout the trials. A green light flashes at the center of the screen for 0.1 second when a double jump happens and the spacebar is pressed. A red light flashes when a double jump happens but the spacebar was not pressed, or when a single jump happens but the spacebar was pressed. 

The trial durations (in seconds) can be modified (lines 115 and 117) and are chosen randomly. The number of trial and the number of practice trials can be changed lines 114 and 116, respectively. The probability of a double jump happening within a trial is set at 10%, but can be changed line 118. 

The output is a CSV file containing the age and gender of participants, the trial's number, the trials' duration, the number of double jumps within a trial, the number of times the spacebar was pressed when a double jump happened (correct), the number of times the spacebar was NOT pressed when a double jump happened (incorrect), the number of times a single jump happened and the spacebar was not pressed (correct), and the number of times the spacebar was pressed when a single jump occured (incorrect). 

This code was made in PsychoPy. The script as well as the images of the clock hands should all be stored in the same folder. 

References:
Mackworth, N. H. (1948). The breakdown of vigilance during prolonged visual search. Quarterly Journal of Experimental Psychology, 1(1), 6-21.
