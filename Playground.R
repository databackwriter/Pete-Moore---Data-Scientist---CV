options(warn=-1)
rm(list=ls()) #clear variables
cat("\014")  #clear console

library(DBI) # for SQL database calls
library(odbc) # for R datab abase calls
con.d <- yaml::yaml.load_file("~/connections.yaml")$sqlconn$DSN
con.u <- yaml::yaml.load_file("~/connections.yaml")$sqlconn$user
con.p <- yaml::yaml.load_file("~/connections.yaml")$sqlconn$password
con <- DBI::dbConnect(odbc::odbc(),
                      DSN = con.d,
                      uid = con.u,
                      pwd = con.p)


section.sql <- "SELECT s.sectionid, s.section FROM Section s"
section.query <- dbSendQuery(con, section.sql)
section.list <- dbFetch(section.query)
section.df <- data.frame(section.list)


for (row in 1:nrow(section.df)){
  section.id <- section.df[row,"sectionid"]
  section.name <- section.df[row,"section"]
  print(paste(section.id,section.name))
}



# section.name <- filter(section.list, sectionid==i)$section
# print(i)
# print(section.name)
names(section.list)

section.list$section[section.list$sectionid=1]

for(id in section.list) {
  print(i)
  # cat("  \n###",  i, " is the section name  \n")
  # cat("summat")
  # cat("  \n")
}


header.n <- function(n){return (rep("#", n))}
lr.buffer <- paste0(rep(" ",2), "\n")
for(i in section.list$section) {
  cat(lr.buffer, "#",  i, lr.buffer) #<--note to self: two spaces here
  cat("summat")
  cat("  \n")
}

# library("dplyr")
# my_data<-section.list
# my_data[1:6, ]
# slice(my_data, 1:6)
# i<-3
# filter(my_data, sectionid==i)$section

# attach(airquality)
# 
# for(i in unique(airquality$Month)) {
#   cat("  \n###",  month.name[i], "Air Quaility  \n")
#   plot(airquality[airquality$Month == i,])
#   cat("  \n")
# }

seq_len(4)
seq_along(4)

n = c(2, 3, 5) 
s = c("aa", "bb", "cc") 
b = c(TRUE, FALSE, TRUE) 
typeof(s)
df = data.frame(n, s, b) 

typeof(df)

for (i in df){
  print(i[3])
}

