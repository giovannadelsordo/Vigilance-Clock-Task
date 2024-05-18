from psychopy import visual, core, event, gui
from random import uniform, shuffle, choice
import time
import csv

# To exit task while experiment is running
def exitIfEscPressed():
    if event.getKeys(keyList=["escape"]):
        core.quit()

# To show clock hand pictures
def showImage(image, pos, size, angle):
    imageClock.image = image
    imageClock.pos = pos
    imageClock.size = size
    imageClock.setOri(angle)
    imageClock.autoDraw = True
    win.flip()
    imageClock.autoDraw = False

# For instructions (display instructions and wait a spacebar press to continue)
def showTextAndWaitSpace(text):
    textBox.autoDraw = True
    textBox.text = text
    win.flip()
    textBox.autoDraw = False
    event.waitKeys(keyList=["space"])

# Code to run the experiment
def runClockTest(durationTrial):
    # Have participants press the spacebar to start a new trial (only display after the first trial)
    if i > 0:
        showTextAndWaitSpace("Press the spacebar to start a new trial.") 
    
    # Show vertical clock hand and reset variables
    clockAngle = 0 # Reset clock hand to vertical position
    doubleJumpCorrect = 0 # Reset the number of correct answer per trial
    doubleJumpIncorrect = 0 # Reset the number of double jumps that should have been pressed but were not
    singleJumpCorrect = 0 # Reset the number of single jumps that were correctly not pressed
    singleJumpIncorrect = 0 # Reset the number of single jumps that incorrectly pressed
    doubleJumpNumber = 0 # Reset the number of double jumps
    previousIsDoubleJump = False # To check if last trial was a double jump
    
    # Show clock hand and wait for two seconds before movement starts
    showImage(clockHandImage, (defaultImagePosX, defaultImagePosY), defaultImageSize, clockAngle)
    core.wait(2)
    
    # Start a new trial
    for j in range(durationTrial):
        # Ensure the next trial doesn't have double jump if the previous one did (no two consecutive double jumps)
        if previousIsDoubleJump:
            isDoubleJump = False
        else:
            # Choose if normal jump or double jump
            isDoubleJump = uniform(0,1) <= probabilityDoubleJump
        # Preparation for next movement
        if isDoubleJump:
            clockAngle += stepAngle*2 # Double the angle to get a double jump
            doubleJumpNumber += 1 # Record a double jump happened
        else:
            clockAngle += stepAngle # Update clock hand angle every frame
        clockAngle %= 360 # Ensure the angle stays within 0-360 degrees
        previousIsDoubleJump = isDoubleJump # Update previousIsDoubleJump for the next trial
        # Show next movement
        showImage(clockHandImage, (defaultImagePosX, defaultImagePosY), defaultImageSize, clockAngle)
        # Record spacebar presses 
        event.getKeys(['space'])
        # Pause before next movement
        # Start timer
        startTime = time.perf_counter()
        while time.perf_counter() - startTime < 1:
            # Check if spacebar was pressed within one second of previous movement
            keys = event.getKeys(['space'])
            isSpaceBarPressed = len(keys) > 0
            if isSpaceBarPressed: 
                break
        # Record behavioral data and give feedback (through colors)
        if isDoubleJump:
            if isSpaceBarPressed: # If double jump happened and spacebar is pressed = correct = feedback show green color
                doubleJumpCorrect += 1
                showImage(clockHandImageGreen, (defaultImagePosX, defaultImagePosY), defaultImageSize, clockAngle)
            else: # If double jump did not happen but spacebar was pressed = incorrect = feedback show red color
                doubleJumpIncorrect +=1
                showImage(clockHandImageRed, (defaultImagePosX, defaultImagePosY), defaultImageSize, clockAngle)
        else:
            if isSpaceBarPressed: # If only a single jump happen and the spacebar was pressed = incorrect = feedback show red color
                singleJumpIncorrect +=1
                showImage(clockHandImageRed, (defaultImagePosX, defaultImagePosY), defaultImageSize, clockAngle)
            else: # If a single jump happened and the spacebar was not pressed = correct = nothing happens
                singleJumpCorrect +=1
        core.wait(1-(time.perf_counter()-startTime)+flashTime) # Each clock hand movement is 1s
        showImage(clockHandImage, (defaultImagePosX, defaultImagePosY), defaultImageSize, clockAngle) # Reset color after feedback
        exitIfEscPressed() # Press escape to get out of task
    # This def returns the following variables in a spreadsheet:
    return doubleJumpNumber, doubleJumpCorrect, doubleJumpIncorrect, singleJumpCorrect, singleJumpIncorrect

studyName = "VigilanceTask"

# USER INFORMATION
userInfoDlg = gui.Dlg(title="Participant information")
userInfoDlg.addField("Number")
userInfoDlg.addField("Age")
userInfoDlg.addField("Gender", choices=["Male", "Female", "Other"])
userInfoDlg.show()
if userInfoDlg.OK == False:
    core.quit()
participantNumber, age, gender = userInfoDlg.data

# INITALIZATION
# Create the main window
win = visual.Window(fullscr=False, units="height")

# Trials (all of these variables can be changed to fit the needs of each experiment)
nbrTrials = 10 # number of trials for the entire experiment
trialDurations = [7,10,12,15,20,30,45,60] # trial duration in seconds (to be picked randomly for each trial)
nbrTrialsPractice = 2 # number of practice trials
trialDurationsPractice = [7,10,12,15,20,30,45,60] # duration for practice trials
probabilityDoubleJump = 0.1 # probability that the clock hand makes a double jump
flashTime = 0.1 # feedback color timing

# Images (images must be located in the same folder as this script)
clockHandImage = 'clock_hand.png' 
clockHandImageRed = 'clock_hand_red.png' 
clockHandImageGreen = 'clock_hand_green.png' 
defaultImageSize = (0.7*0.149,0.7) 
defaultImagePosX = 0
defaultImagePosY = 0

imageClock = visual.ImageStim(win, image = clockHandImage, size = defaultImageSize) # Inititalize image
imageClockRed = visual.ImageStim(win, image = clockHandImageRed, size = defaultImageSize) # Initialize clock hand with red feedback (incorrect)
imageClockGreen = visual.ImageStim(win, image = clockHandImageGreen, size = defaultImageSize) # Initialize clock hand with green feedback (correct)
clockAngle = 0 # Initial angle, to be updated through the trial
stepAngle = 4 # Adjust the simple jump angle

# Text boxes for instructions
textBox = visual.TextBox2(win, text="", letterHeight=0.03,  alignment="center", autoDraw=False, size=[1.25, None])

# Create CSV file
fileName = "{}_{}.csv".format(studyName, participantNumber)
csvFile = open(fileName,"w")
csvFile.write("{},{},{},{},{},{},{},{},{}\n".format("Age", "Gender", "Trial Number", "Trial duration", "Double jumps number", "Correctly pressed double jumps",
                                            "Not pressed double jumps", "Single jump correctly not pressed", "Single jump incorrectly pressed")) # set up columns for file output
csvFile.flush()

# WELCOME
showTextAndWaitSpace("Welcome to this experiment.\n" +
                     "Press the space bar to continue")

# INSTRUCTIONS
showTextAndWaitSpace("In the task you are going to perform, your vigilance is going to be tested.\n" +
                    "This task is very simple. You are going to see a clock hand.\n" +
                    "The clock hand is going to move circularly at a regular path.\n" +
                    "However, sometimes the clock hand is going to jump more than normally.\n" +
                    "Your job is to press the space bar as soon as you detect the irregular jumps.\n\n\n" +
                    "Press the space bar to continue.")

showTextAndWaitSpace("A bit more information before you start:\n" +
                    "You will only have one second from the moment the long jump happen to press the space bar.\n" +
                    "Each trial can last anywhere from a few seconds to a few minutes.\n"
                    "You need to stay very vigilant throughout the task to perform well!\n" +
                    "You will receive feedback through red or green flashes throughout the trials.\n" +
                    "The center of the screen will flash green if you correctly detect a long jump. \n" +
                    "However, the center of the screen will flash red when you press the space bar when there was no unusual clock hand jumping or when you failed to detect it.\n\n" +
                    "Press the space bar to continue.")

showTextAndWaitSpace("Let's start with some practice trials.\n\n Press the space bar to start.")

#PRACTICE TRIALS
for i in range(nbrTrialsPractice): # Practice trials number
    durationTrialsPractice = choice(trialDurationsPractice) # randomly choose trial duration
    # Run practice trials by inputing in parenthesis the trials duration
    doubleJumpNumber, doubleJumpCorrect, doubleJumpIncorrect, singleJumpCorrect, singleJumpIncorrect = runClockTest(durationTrialsPractice)

# Instructions to start experimental trials
showTextAndWaitSpace("The real experiment is going to start.\n If you have a question, please raise your hand and ask the resercher.\n\n" +
                    "Press the space bar when you are ready.")

# REAL TRIALS
for i in range(nbrTrials):
    durationTrial = choice(trialDurations) #randomly choose trial duration
    doubleJumpNumber, doubleJumpCorrect, doubleJumpIncorrect, singleJumpCorrect, singleJumpIncorrect = runClockTest(durationTrial)
    # Write data into CVS file 
    csvFile.write("{},{},{},{},{},{},{},{},{}\n".format(age, gender.lower(), 1+i, durationTrial, doubleJumpNumber, doubleJumpCorrect, doubleJumpIncorrect,
                                                singleJumpCorrect, singleJumpIncorrect))
    csvFile.flush()

# DEBRIEF
showTextAndWaitSpace("Thank you for participating!\n Let the researcher know that you are done.\n\n Researcher: Press the space bar to end the task.")

# Terminate task and close CSV
csvFile.close()
core.quit()

