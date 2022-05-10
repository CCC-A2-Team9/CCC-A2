# Team9 - Frontend

## 1. How to run
    cd frontend/ docker-compose up

## 2. End user usage
### frontend:
 http://172.26.132.76:3000/
 
 
## 3. Role
Dynamically display data visualization for our cloud-based system.

## 4. Main Components
- The login page
- The homepage
- The team profile page
- Data visualization pages for each scenario

## 5. How to fetch data from Back-end
When we open and refresh the page, the data displayed in histograms, pie charts, and the estimated coefficients of the linear regression model will be retrieved via the ajax() method in Flask. With the ajax() method, an approach used to perform an AJAX (asynchronous HTTP) request, we can request only a portion of the page information we need each time, instead of requesting a completely new page. The process is that, first, when the page is loaded, JavaScript will create an XMLHttpRequest object. Then a request will be sent by this XMLHttpRequest object to the back-end server. Afterward, the back-end server will send a request to the CouchDB database, and it will send back a response to our back-end server. Finally, the data will be performed on our webpage after obtaining the response from the back-end server. 
