# Flask Framework
## Running a Flask Application
In order to run a Flask application you need to create an instance of the Flask class and call the run()-method on the object, like so: 
<code>
import os
from flask import Flask
app = Flask(__name__)
app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
</code>
NOTE! In the example above the parameters: host, port are grabbing the IP and PORT environment variables from the Operating System. 
<code>
os.environ.get({desired IP},{default IP})
os.environ.get({desired PORT},{default PORT})
</code> 
Furthermore, the code also provides a second parameter for a **default value** for the **IP** and the **PORT**, as a fallback strategy if the variables are **not defined** in the **environment of the Operating System**.

## Basic Structure
### Folders
**static** - used for storing folders with **CSS, JS and Images**
**templates** - used for storing **HTML** files

### Files
**models.py** - Model Classes
**routes.py** - @app.route annotations for HttpRequests and HttpResponse routing with corresponding view functions

### Templating language cheat sheet
#### Define or Insert block into a template
<code>
{% block block_name %} 
// In base template leave this empty
// In the actual template insert the code for this block here ..
{% endblock %}
{}
</code>

#### Use variables that have been passed to the view via render_template()
Envelop the name of variable inside **double curly braces**
<code>{{ name of variable }}</code>

#### Linking a URL from the template
Envelop the call to the **url_for()** function, which must be sitting inside a set of **double curly braces**
<code>{{ url_for('url_name')}} </code>




## Apache2 Webserver Deployment
### Prepare App Folder
#### Prerequisites
A virtual environment tool for python3 must be installed
<code>
$ apt-get install -y python3-venv
</code>

##### Step by Step set up of the app folder
1. Create a **app folder** where you will copy your project to.
2. To create a **virtual environment folder**. From inside the **app folder** run <code>$ python -m venv venv</code>
3. **Activate the virtual environment** <code>$ source ./venv/bin/activate </code>
4. Now **install** all the **packages** that the project requires using<code>$ pip3 install -r requirements.txt</code>
5. **Deactivate the virtual environment** <code>$ deactivate</code>
6. Copy project files to the **app folder**

### Server Configuration
The weserver needs a configuration file with the extension **wsgi**. In this file you need to add paths to your application and its virtual environment.
In the sample code below I also enable logging, linking it to stderr, which will result in writing the print() messages that you might have placed inside the scripts or the messages that are printed when an **exception, error or warning** is printed by any of the scripts that live inside the included libraries.

Lastly, I need to import and run the Flask app. Which is simply done by **importing** the app from a file or folder as **application**. The name **application is key** , because **Apache2 server** will create an instance of it and then call the **run()** method on it with valid parameters. In there is no neccessaty for you to run the application, because the server takes care of that.

#### WSGI Config file
<code>
import sys
import logging
 
sys.path.insert(0, '/opt/path/to/your/app')
sys.path.insert(0, '/opt/path/to/your/app/venv/lib/python3.10/site-packages/')

#Set up logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
 
#Import and run the Flask app

from {name of the folder/file} import app as application
</code>

Then you need to set up two more configuration files. One is a general configuration of the app. The other is a configuration for a virtual host.
The first configuration file must be placed inside the folder **apache2/conf-enabled **. You can name it whatever you want as long as it hast the **.conf** extension.

#### Apache Config file
**app_name** = name of your application
**wsgi_file** = name of your wsgi file 
**url** = the URL that you want it to be at, a single slash if the application should live at the root directory

<code>
WSGIDaemonProcess app_name processes=1 threads=25 python-home=/opt/path/to/your/app/venv
WSGIScriptAlias /**url** /opt/path/to/your/app/**wsgi_file**

\<Directory /opt/organizer/>
    WSGIProcessGroup **app_name**
    WSGIApplicationGroup %{GLOBAL}
    Require all granted
\</Directory>

</code>

#### Virtual Host Config file
**server_name** = name of your server instance
**wsgi_file** = name of your wsgi file 
**url** = the URL that you want it to be at, a single slash if the application should live at the root directory

<code>

\<VirtualHost *>
    ServerName **server_name**
    WSGIScriptAlias /**url** /opt/path/to/your/app/**wsgi_file**
    \<Directory /opt/path/to/your/app>
        Order deny,allow
        Allow from all
    \</Directory>
\</VirtualHost>

</code>

