#Coding Task Description

======================================


update: i made a simple frontend to verify the backend  
to run the full stack 

`docker-compose up `

the frontend is located at 

`<serveraddress>:5110`

the backend is located at 

`<serveraddress>:5111`

on the frontend, i didnt wait for the response from the backend before i update the text ont the UI , but the request is actually made . but you can press the button several times to update the UI. 

input the url address you can to add into the scan and press "input"

"watchdog" is for watching the current status of the scan service running and show all the latest result of the scan. 

"kill" will kill the watchdog on the backend to stop all the on going tasks. noticed that the request already made in the queue will not stop , so there will be at most one more request to be finished on the backend. 


=============================================

Implement a program that monitors web sites and reports their availability. This tool is intended as a monitoring tool for web site administrators for detecting problems on their sites.

##Main functions:

1.	Reads a list of web pages (HTTP URLs) and corresponding page content requirements from extenal configuration.

====visit <serveraddress>:5111/input/<websiteaddress> to send a request (you can send multiple requests to monitor several websites. the reason to design like this is to have connection with the front end , the front end can send request to monitor the websites.
====visit <serveraddress>:5111/watch to watch the result. the result is provided in json format so easy to connect to the front end

2.	Periodically makes an HTTP request to each page.

====access <serveraddress>:5111/input/<websiteaddress>/<checkfrequency> to define the check frequency, default frequency is 5 seconds, the minimum frequency is 0.2 sec

3.	Verifies that the response result received from the server matches the requirements in the configuration.

====the result can be found at <serveraddress>:5111/watch , there is a key called "result" is telling if the requirement matches or not , and also other information can be found in there

4.	Measures the time it took for the web server to complete the whole request.

====the result can be found at <serveraddress>:5111/watch , there is a key called "responcetime" is telling the time it took to reach the server

5.	Writes a log that contains the progress of the periodic checks.

====the log can be found at <serveraddress>:5111/log , including all the request result in a json file format

6.	(OPTIONAL) Implement a single-page HTTP server interface that shows (HTML) each monitored web site and their current (last check) status.

==== the current status can be found at <serveraddress>:5111/watch
====it is showing all the current on going scan and the latest result.


##Details:

•	The “content requirement” can for example be just a simple string that must be included in the response received from the server, e.g. one rule might be that the page at the URL “http://www.foobar.com/login” must contain the text “Please login:”.

====access <serveraddress>:5111/input/<websiteaddress>&&<keyword> to define a content requirement keyword

•	The checking period must be configurable via a command-line option or by a setting in the configuration.
====access <serveraddress>:5111/input/<websiteaddress>/<checkfrequency> to define the checking period , default frequency is 5 seconds , the minimum frequency is 0.2 sec

•	The log must contain the checked URLs, their status and the response times.
====this is a sample log
{"google.com&&soemthings": {"checkfreq": 5.0, "keyword": "soemthings", "responcetime": "0.113223", "result": "website up and keyword NOT found", "time": "2020-09-25 18:45:31.866942", "url": "google.com"}}
====so it contains the check period, content keyword, response time , results of checking , checked time , checked url
•	The program must distinguish between connection level problems (e.g. the web site is down) and content problems (e.g. the content requirements were not fulfilled).
==== connection level problems includes timeout, too many redirection, website not reachable . content problem includes content found , content not found , no content defined .

There is a lot of freedom to choose software technologies, tools and file formats to achieve the goal.

==== this solution is based on python backend and angular frontend (the frontend is not yet including when I am writing this document , the app also has docker configs setup , can be easily deployed using docker compose .

Note that the task is meant for evaluating both software development and software architecture design skills. Pay attention to the design of applications you create. Be ready to defend your architectural decisions in a discussion.

It is necessary to personally write the source code, but it does not have to be complete.

##Deliverables:

The software is delivered with the full source code included. All used source code must be freely distributable.

If necessary, include readme.txt to describe the software and how it meets the requirements.

====to run the application . download the package and run docker-compose up . it will setup the environment and server.
====also it is fine to run on the host machine by running python server.py . the real time result is available from the console.

##Design question

Assuming we wanted to simultaneously monitor the connectivity (and latencies) from multiple geographically distributed locations and collect all the data to a single report that always reflects the current status across all locations. Describe how the design would be different. How would you transfer the data? Security considerations?

====the app that I made is a backend service , it can be distributed to servers where we need to send the request from . the client in this case , will send a request to all the nodes , to tell them to monitor the target from different place . when the nodes are done with monitoring , they can send back the client the result . in that case , we will have the connection information from different geo locations .

==== to do it in a more secure way . since the connection from the client is always considered unsafe and unstable , we could setup a backend management node to talk to all the service nodes (which is the one actually making the requests). client make a request to the management node to request scanning .the management node will send request to service nodes over the globe. when the management node collect the data , it will feed back to the client

====as for the security . the request sent from client can be going through TLS, also it can be from an native app , which has lower risk of seeing the source code and got reverse engineering, management node can be behind cloud front and load balancer. the management node will make requests to the service nodes , it can be a request sent from a customised protocol on a customised port . tunnelling the communication between the server nodes can be quite an effective way to avoid noise and security problems . but the "last one mile " will be still normal http request to get the accurate result.

