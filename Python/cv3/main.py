import os

fileName = "temp.txt"
repoDest= "C:/Users/moravcik50/pvsa/git/2023-python/"
#repoDest = "C:/Users/David/OneDrive/Desktop/cloud/workspace/python/uniza/cv3/"

def addFileToGit(fname, destination):
	os.system("cd " + destination)
	os.system("git add " + fname)

def commitFileToGit(message, repo):
	os.chdir(repo)
	os.system("git commit -m \"" + message + "\"")

def gitPush(repo):
	os.chdir(repo)
	os.system("git push")

file = open(repoDest + "new.txt", "w")
file.write("PSA ROCKS!")
file.close()

addFileToGit(fileName, repoDest)
commitFileToGit("Commit cez skript", repoDest)
gitPush(repoDest)