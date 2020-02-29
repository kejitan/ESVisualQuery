Query Based Image Search

The overall project consists of two independent but related
projects.

1. Given a text query (comma separated string), the system will
retrieve images from the given image database that contains 
each of the items in the list. While all candidates are retrieved,
only random 4 are presented to the user since it is possible
that some queries may retrieve a large number of images thus
clogging the system. For this part Visual Genome dataset from
Stanford with 108077 images is chosen. 

2. The other project uses a pre-trained pspnet model trained
on MIT CSAIL ADE20K data set consisting of approx 20000 images
is used. The pre-trained model is used to segment and then 
programmatically annotate the images. The annotations describe 
all the objects that are present in the images. When a query is
presented, it is segmented and annotated using the pre-trained
model and used to search the annotations of the ADE20K datset to
retrieve required images. As a further step, the Visual Geneome
data est is also annotated and thus augments the data set from
which to search for the items in the query. 

This submission reports the first project. 

The image annotations are quite big files and to expedite the
search, Elastic Search is used. 

The Github repository consists of self-contained system. 
a. image_data20.json contains image ids and image file names
(urls) of 20 sample images. 
b. objects_data20.json contains annotations of these 20 images. 
They consists of names of the objects in the images, and other
auxiliary information that can support more complex queries
c. ESMap20.py, creates two sets of indexes, one for image ids
and another for object annotations. 
d. In case it is desired to recreate the index files for 
Elastic Search, the existing indexes are deleted by
 DelESIndexes.py script
e. TestVG20.py file is a python application using Dash
and provides user interface

Testing procedure. 
1. Create a virtual environment with required dependencies 
(Dash, Elastic Search, ..) and clone the repository.
2. Install Electric Search (7.4.2 or later), Kibana
3. Start Electric Search daemon with 'sudo systemctl start elasticsearch.service'
4. in bash terminal in the repository home directory, run: 
'python ESMap20.py'. There is a 10 second programmed delay 
between creation of two indexes to prevent unintended errors.
5. On a web-browser check that Electric Search daemon is running
by visiting url localhost:9200. 
6. In another tab type in url localhost:8053 
- This is where the images will be displayed.
7. In the terminal dun 'python TestVG20.py'. 
There is some debug printing in the terminal to show 
what is retrieved from the system. It asks to refresh the browser. 
Please do so, and the images will be displayed. Still working 
on the part where the display will be automatically refreshed and 
when desired the user can clear the images from the screen.
Currently Clear Images button is not working.

A new file (in lieu of TestVG20.py has been added, This allows
clearing of images after they are viewed so that the images
for the fresh queries are displayed in the prime area. 
After installing Elastic Search, starting it with 
'sudo systemctl start elasticsearch.service', 
verify thatis is running by opening localhost:0200
Rub python ESMAP20.py
Run python VGdash20.py

For any comments please contact kejitan@gmail.com

Second project is on the way, where a sample image is presnted, 
the system segments it and annotated=s it and finds similar images
based on annotations. This part could be used to annotate and then
search the videos very fast.

The system has been tested on 108077 images and the response
is very fast. 

