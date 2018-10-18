# most of the packages herein are maintained via the Anaconda environment 
# however packages like tufte and those direct from github are not implemented 
# useful function from https://stackoverflow.com/questions/9341635/check-for-installed-packages-before-running-install-packages
# adapted by PM to allow GitHub install
pkgTest <- function(x, UseGitHubInstead=FALSE)
{
  if (!require(x,character.only = TRUE))
  {
    if (UseGitHubInstead)
      {
        library(devtools)
        install_github(x)
      }
    else
      {
        install.packages(x,dep=TRUE)
      }
    if(!require(x,character.only = TRUE)) stop("Package not found")
  }
}

#get Tufte if not already there
pkgTest("tufte")
# get mpiccirilli's LinkedIn package from GitHub
# it is here: https://github.com/mpiccirilli/Rlinkedin
# NB depends on XML package which, here, was installed via anaconda
pkgTest("mpiccirilli/Rlinkedin", UseGitHubInstead = TRUE)

#ancillary packages: MacTex, installed by hand

# tufte theme for viz
pkgTest("ggthemes")

# direct labels for viz
pkgTest("directlabels")