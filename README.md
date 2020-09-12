# dots-and-boxes
dots and boxes game/AI oponent for CMPUT 355 at UofA

how to git 101:
easiest way will be to download github desktop app but if you are using linux then command line will work just fine.

# getting started
first thing you need to do is clone the repo. When on the website, click the green code button and you should see a URL you can copy.
if you have the desktop app, then there is an option to open the repo in the app.
if not, run 'git clone URL' where URL is whatever you can copy from the website.

# checking your current branch
we will use branches when working on different features. generally a branch is named something like 'feature/game' or 'bug/line-colours'
the first part of it is what you are working on (i.e. feature, bug, organinizing) and the second is more specific to what you are building/fixing

in the desktop app there is a drop down option to take care of branches.
in git, you can see what branch you're on and all other branches in the repo using 'git branch'
to make a new branch, use 'git checkout -b new-branch-name'. Don't forget to push it to github using 'git push origin new-branch-name'
keep in mind 'new-branch-name' is whatever you want to call the branch

to switch between branches, use 'git checkout branch-name' where the branch name is the name of the branch you want to switch to

# pulling
simply use 'git pull' to get everything up to date. i would reccomend doing this whenever you start working to get new changes that have been pushed

# what to do when you want to upload your code
when working on code, there are 3 steps to getting it online.
first, you need to prepare things for staging. To do this, use 'git add .'
next, use 'git commit -m "upload message"' where upload message is whatever info you have for the current commit. 
finally, use 'git push origin' to send the changes up! 

# what happens when you finish all the work needed on a branch
you just make a pull request on the github website!
