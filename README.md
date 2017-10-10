# RapidScreenshots
A script that takes screenshots for a given period of time

This python script is used to take rapidly take screenshots using pyscreenshot while the user
uses their computer for other purposes. No guarantee is given for the number of
screenshots taken during a time frame. Images are stored as .png files in the folder
that the program is run in with names of 1.png, 2.png, ... n.png (where n is an integer).

# Usage
The script has three optional parameters:

1. --time_limit
This is the amount of time the program will run. A floating point number denoting
the amount of seconds to run should be given. If a number less than or equal to zero is
given then the program will not terminate. Instead, use CTRL+BREAK to end the program.
The default value is ten seconds.

2. --loop_time_limit
This is the amount of time the program will run before it begins overwriting old images.
To conserve memory, it can be specified to only keep images until a time limit is reached.
The value is a floating point number denoting the amount of seconds each loop should be.
If this is set to zero or less then the program will ignore time with regard to whether to
overwrite old images. The default is zero seconds.

3. --maximum_screenshots
This is an integer amount that denotes how many images to keep. After this many images are created
then old images will be overwritten. If it is set to zero or less then the program will ignore
the number of images with regard to whether or not to overwrite old images. The default is zero.


The cleanup.py script can be used to delete all of the .png files in the directory from which
it is executed (Use caution when executing it!).

