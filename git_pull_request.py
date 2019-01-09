'''
script to fetch all contents in the remote repo and update the local
by D. Bailey
'''


def pull_from_github(remote_repo):

    import os
    import git

    # May need to change this to another directory on Ubuntu
    #os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = '/usr/local/bin/git'

    # define the git repo
    git_dir = "{}".format(remote_repo)
    # intialize git repo
    repo = git.Repo.init(git_dir)
    g = git.cmd.Git(repo)
    # make pull request
    g.pull()

    print "Success!"


pull_from_github("") #"https://dbailey_89:@bitbucket.org/dbailey_89/wildlife_app.git"

