# get sql
FROM microsoft/mssql-server-linux:2017-latest
 
# create directory within SQL container for database files
# Set the working directory to /SQLServer
WORKDIR /SQLServer

# Copy the current directory contents into the container at /SQLServer
ADD . /SQLServer
 
# set environment variables
ENV SA_PASSWORD=h00rayforCVs
 
ENV ACCEPT_EULA=Y

ENV MSSQL_PID=Developer

ENV NAME sqlSmartCV

EXPOSE 1433

#install bet tools so that can run and ifconfig later on (ignore debconf warning)
RUN apt-get update
RUN apt-get install -y net-tools

#start sql agent on start up
RUN /opt/mssql/bin/mssql-conf set sqlagent.enabled true 

# Run SQL Server process.
CMD [ "/opt/mssql/bin/sqlservr" ]

#now run this from docker: 
#docker tag [image] lookatyourdata/sqlrepo:smartcvnaked
#docker push lookatyourdata/sqlrepo:smartcvnaked
#docker run --name=[yourcont] --restart=always -d -v [localdrivefromwhichtomountdatabase]:/var/opt/mssql -p 5173:1433 smartcv 



