# Search Aalysis Application (Description)
### There are two folders in the repository.
##### First, is for the Flask application i.e., the RESTful Backend
##### Second, is for the React application i.e., the Frontend

#### First and foremost, clone or download the entire repository. Then, perform the following steps to get the system up and running.

### For the Flask App:
First, please ensure that 'pip' is installed in your machine.
Open a Terminal, and move into the 'Flask API for app' folder. It is a good practice to create a virtual environment before installing the packages.
Refer to ['VENV'](https://docs.python.org/3/library/venv.html) for this. Once, you have created a virtual environment, and are in it, install the requirements.txt file.

```
  pip install -r requirements.txt
```
This command installs all the required dependencies for the Flask application directly.

After this, to start the server, run the following command in the Terminal.
```
  python3 ./main.py
```
 
 Once you run this command, you have started a server on the Port:5000. This will fetch all the scraped data from Google and Bing, and also compute the sentiment from IBM Watson.
 
 ### For the React App:
Please ensure that Node is installed in your environment before moving forward. You need to be able to run 'npm' in the next step.
Change the working directory into the 'client' folder. This holds the React app.
Then, install all the packages that are needed for the application. This is stored in 'package.json'. It can be installed using the command:
```
  npm install
```
Afterr this, start the app.
```
  npm start
```
Once this step is complete, it shold automatically take you to the link of the React app. If not, by default, the app runs in Port:3000. So, go to:
'localhost:3000' in your web browser. This info is also visible in the Terminal where you entered the command.

### Note: Please ensure both the Flask backend and React frontend are running. Don't close the terminals. And, if the port number for Flask is different, you can change it in the 'package.json' file.

> In case of any errors, ensure that Python version is 3.0+ and Node.js is installed on the stable version 16.14.2.

## Testing the App
When you go to the `localhost:3000`, you should see the 'Fetch' Dashboard that looks something like this:

![image](https://raw.githubusercontent.com/BatsalG/search-engine-app/main/SearchFullStack/screenshots/Fetch_Dashboard.jpg)

From the dashboard, you can add in the keywords, number of results and intervals and start the fetching process.

![image](https://github.com/BatsalG/search-engine-app/blob/main/SearchFullStack/screenshots/fetch.jpg?raw=true)

You can also persist the list of keywords to the database with a unique identifier, which makes searching for jobs easier.

![image](https://github.com/BatsalG/search-engine-app/blob/main/SearchFullStack/screenshots/keyword_persis.jpg?raw=true)

There is also a tab named "Active" which shows all the active jobs running. Based on this, you can stop the job and search for jobs using the unique identifier.

![image](https://github.com/BatsalG/search-engine-app/blob/main/SearchFullStack/screenshots/Running-jobs.jpg?raw=true)

Finally, there is a tab named "Search"

![image](https://user-images.githubusercontent.com/90344616/145472587-5f126ce0-c94e-4b17-b0e3-62dc49933d68.png)

Here, you can enter a keyword of you choosing and select whether you want to search with Google or Bing, or Both.

![image](https://user-images.githubusercontent.com/90344616/145472928-2a0324e5-6f47-40af-b27b-0c20c41a01b7.png)

Once you submit the query, you will be redirected to a page comparing the results between Google and Bing.

![image](https://user-images.githubusercontent.com/90344616/145473532-5d8bf5e2-4aae-40c7-a95d-f094de2e151d.png)

As you hover over each of the article boxes, you can either look at its analysis or go to the site of its publisher. When you click on 'Analysis', it will take you to a dashboard with all the information about the article's sentiment and emotion.

![image](https://user-images.githubusercontent.com/90344616/145473786-6e4819f8-9916-420c-bc76-c7a939db0717.png)

![image](https://user-images.githubusercontent.com/90344616/145473869-22c402f4-3d02-43cd-9d85-45c3941a1d54.png)

To view further analysis of the search engines, visit [this](https://github.com/BatsalG/SearchAnalysis) repository.
