# hookup to linked in profile
# I followed the below link to do this:
# http://thinktostart.com/analyze-linkedin-with-r/

# ultimately this function led to frustration, it requires a key press and 
# the standard developer edition of the linked in licence only provides most recent
# position
# I am waiting to see if I can get full profile access (I am doubtful at this point)
getlinkedinprofile <- function(x){
  require(devtools)
  require(Rlinkedin)
  
  con.a <- yaml::yaml.load_file("~/connections.yaml")$linkedinconn$app_name
  con.k <- yaml::yaml.load_file("~/connections.yaml")$linkedinconn$consumer_key
  con.s <- yaml::yaml.load_file("~/connections.yaml")$linkedinconn$consumer_secret
  
  
  in.auth <- inOAuth(application_name = con.a, consumer_key = con.k,
                     consumer_secret = con.s)
  my.profile <- getProfile(token=in.auth, partner=1)
  
  return(my.profile)
}

s<-getlinkedinprofile(1)
