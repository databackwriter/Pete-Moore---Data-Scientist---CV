# take CV from Word, paste into excel, label and split strings accordingly
# the below script then uses the sqlalchemy to build into an SQL Server
# DockerFile for SQL Server build is contained in /SQL folder
library(readxl)
xl.path<-"Excel/Initial data model.xlsx"
xl.sheet<-"Flat CV"
xl.list<-read_excel(xl.path, sheet=xl.sheet, n_max=1000)



for (xl.row in xl.list){
  print(xl.row[100])
}