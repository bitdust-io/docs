# Software releases

* [Intro](#intro)
* [Prepare environment](#prepare-environment)
* [Runbook](#runbook)
* [Update Documentation](#update-documentation)


## Intro

The BitDust project development flow is based on two independent GIT repositories:

* [Development repository](https://github.com/bitdust-io/devel)
* [Stable repository](https://github.com/bitdust-io/public)


When changes in the development repo are considered to be "good enough" files are manually copied by one of the developers to the stable repo and the new Pull Request is started.
This process can be considered as a new "Release" - we do not have any versioning of the releases.
After the Pull Request gets merged -  the release is done.

Every BitDust node periodically "check & fetch" fresh commits from the GIT repository where it was cloned from.
This way the BitDust software automatically "updates itself" and stays in sync with the "Stable" repository.

As a user of BitDust software you can disabled automatic updates at any moment in the program settings.

You can also fork BitDust "stable" repo and clone locally your fork to quickly check and run main python code. Just like any other github project you forked, your fork will be fully independent from the main repo. This will work for developers and for those who wish to stay in sync with main network manually.

Most BitDust users are starting from main web site and download installer from [BitDust desktop](https://github.com/bitdust-io/desktop/releases) release files - they automatically stay in sync with "Stable" repository.

Below is a step-by-step guide to deliver changes from the "Development" repository into the "Stable" repository.



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

Change to `devops/` folder inside development repository and run `release_prepare` script:

    cd bitdust.devel/devops/
    ./release_prepare


This will prepare all files to be commited into "Stable" repository. All modified/added/removed files will be displayed in your terminal output. That script is doing a bunch of things:

* copy files from "devel" to "stable" repo
* disable DEBUG mode in all Python files
* compare all files in both repositories
* updates `HISTORY.txt` file in "devel" repo


Now edit `bitdust.devel/CHANGELOG.txt` file manually - you need to provide some info about your changes. After running `release_prepare` you should see in your terminal console output a list of most recent commits. Just copy those lines and paste on top of `CHANGELOG.txt` file:

    # copy text block from `HISTORY.TXT` file into `CHANGELOG.txt` and make it look nice
    cd ..
    nano CHANGELOG.txt


Now you need to change to the "stable" repository and run `git add ...` / `git rm ...` commands to confirm changes.

First mark all modified files in git to be commited in the new release:

    cd ../bitdust
    git add -u .


Add all other new files to git manually - this is important here to not miss any files created recently in "devel" repo:

    git add <some new file>


If some files or folders were removed from "devel" repo - do not forget to also remove them from the "stable" repo and mark those changes to be commited:

    git rm <some old file>


We are almost done!
Change back to `devops/` folder inside development repository and run `release_start` script:

    cd ../bitdust.devel/devops/
    ./release_start


That script will push all prepared changes to your forked repositories.

All you need to do now is to create new [Pull Request](https://github.com/bitdust-io/public/pulls) to the "stable" repository ...

Make sure Travis build is green ...

Review changes ...

Click Merge button ... 

Congratulations, YOU ARE LIVE NOW!!!

Update your fork to stay in sync:

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
