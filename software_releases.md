# Software releases

* [Intro](#intro)
* [Prepare environment](#prepare-environment)
* [Runbook](#runbook)
* [Update Documentation](#update-documentation)


## Intro

The BitDust project development flow is based on two independent GIT repositories:

* [Development repository](https://github.com/bitdust-io/devel)
* [Stable repository](https://github.com/bitdust-io/public)


When changes in the development repo are considered to be "good enough" files are manually copied by one of the developers to the stable repo fork on his local machine and new commit must be created to start a new Pull Request.

This process can be considered as a new "Release" - BitDust do not have any versioning of the releases because it is not required. After Pull Request is merged - release is done.

Every BitDust node periodically "check & fetch" fresh commits from the GIT repository where it was cloned from.
This way BitDust software on your local machine automatically "updates itself" and stays in sync with the "Stable" repository. Every BitDust contributor is responsible to deliver high-standard, super reliable and well-tested source code changes every time Pull Request is merged.

You can also fork BitDust "stable" repo and clone locally your fork to quickly check and run main Python code. Just like any other github project you forked, your fork will be fully independent from the main repo - you will have to sync manually with main repo if you wish to stay on same version. This will work the best for all of the developers and also for those who wish to learn BitDust or particiapte in testing.

If you stay out of sync with other users your data is at risk! Remember to always check & pull your BitDust software sources and stay in sync with the main network by updating your code from [Stable repository](https://github.com/bitdust-io/public).

For non-developers and all other people willing to join BitDust network in a common way we maintain [BitDust Desktop](https://github.com/bitdust-io/desktop/releases) Application installer.

You go directly to [bitdust.io web site](https://bitdust.io) and download installer file - we provide link directly from [GitHub repo]([BitDust desktop](https://github.com/bitdust-io/desktop/). Application uses Electron Framework for GUI and will automatically clone from BitDust Stable repo for the first time you run application and keep your local sources in sync with the master branch.

As a user of BitDust software you can disabled automatic updates at any moment in the program settings and always run only the code you cloned first time when you get into BitDust network.

Below is a step-by-step guide for developers to deliver changes from the "Development" repository into the "Stable" repository.



## Prepare environment

To be able to run a new BitDust release you must fork and clone both repositories already.
Basically those actions you need to do only one time and just keep your repositories up-to-date with the main branches.

Here we assume your fork will be "origin" and main repository will be added as "upstream":

    # fork and clone development repo
    git clone git@github.com:<your GitHub username here>/devel.git bitdust.devel
    cd bitdust.devel
    git remote add upstream https://github.com/bitdust-io/devel.git
    cd ..

    # fork and clone stable repo
    git clone git@github.com:<your GitHub username here>/public.git bitdust
    cd bitdust
    git remote add upstream https://github.com/bitdust-io/public.git
    cd ..



## Runbook

Change to `bitdust.devops/` repository and run First script:

    git clone https://github.com/bitdust-io/devops.git bitdust.devops
    cd bitdust.devops/
    ./cicd/release_prepare


This will prepare all files to be commited into "Stable" repository.
All modified/added/removed files will be displayed in your terminal output. That script is doing a bunch of things:

* copy files from "devel" to "stable" repo
* disable DEBUG mode in all Python files
* compare all files in both repositories
* updates `HISTORY.txt` file in "devel" repo


Now edit `bitdust.devel/CHANGELOG.txt` file manually - you need to provide some info about your changes.
After running `release_prepare` you should see in your terminal console output a list of most recent commits.
Just copy those lines and paste on top of `CHANGELOG.txt` file:

    # copy text block from `HISTORY.TXT` file into `CHANGELOG.txt` and make it look nice
    nano ../bitdust.devel/CHANGELOG.txt


Now you need to change to the "stable" repository and run `git add ...` / `git rm ...` commands to confirm changes.

First mark all modified files in git to be commited in the new release:

    cd ../bitdust
    git add -u .


Add all other new files to git manually - this is important here to not miss any files created recently in "devel" repo:

    git add <some new file>


If some files or folders were removed from "devel" repo - do not forget to also remove them from the "stable" repo and mark those changes to be commited:

    git rm <some old file>


We are almost done!

Change back to `bitdust.devops` repository Second script:

    cd ../bitdust.devops/
    ./cicd/release_start


That script will push all prepared changes to your forked repositories.

All you need now to do start the release is to create new [Pull Request](https://github.com/bitdust-io/public/pulls) towards "stable" repository via GitHub web site.

Make sure Travis build is green and people review your changes and everyone agree with your code.

One of the core developers must click Merge button, and ...  Congratulations, your changes are LIVE!

Do not forget to update your fork right away to stay in sync and avoid merge conflicts later:

    git pull upstream master
    git push origin master



## Update Documentation

The BitDust project Documentation is fully open-sourced and everyone is welcome to contribute and improve it the [Documentation repository](https://github.com/bitdust-io/docs).
Those steps are required to keep documentation in sync with the code.

Update "docs" repo first, you must already have it forked and cloned in the`./bitdust.docs/` folder in same parent folder as the "devel" and the "stable" repos:

    cd ../bitdust.docs/
    ./build_api
    ./build_settings
    # TODO: ./build_changelog


Push changes to your fork of the documentation repository and start a new [Pull Request](https://github.com/bitdust-io/docs/pulls) to the upstream:

    git push origin master
    # Open & Review & Merge Pull Request


Update your fork to stay in sync after a merge:

    git pull upstream master
    git push origin master


ALL DONE!

