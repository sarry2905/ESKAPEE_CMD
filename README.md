# ESKAPEE CLassifer Command Line Tool

ESKAPEE_CMD is the command line based tool developed in python3.10. This command line has same functionality as the [Dynamic Web Server for ESKAPEE classification](http://115.241.23.53:8000/). This tool can be setup once (follow instructions below) and run on any (Windows and linux) machine locally without having to upload any gzip files on a third party server.

ESKAPEE_CMD is an AI based tool that can take raw clinical sequence(s) as input (SRA in form of gzipped fastq/fasta file(s)) and classifies them into either one of ESKAPE _(Enterococcus faecium, Staphylococcus aureus, Klebsiella pneumoniae, Acinetobacter baumannii, Pseudomonas aeruginosa, Enterobacter)_ or Escherichia Coli or none of them (Non-ESKAPE). 

The tool can be run through the command prompt or terminal using a set of instructions which are detailed below, with example. The input to the tool can be a single gzip file (path\to\file) or multiple gzip files, stored in the same directory (path\to\directory).
Upon execution, first the tool extracts the sequence from the input file(s), then generates the feature vector with a count of 4000 kmers from the extracted sequence. Lastly, an ensemble of 5 machine learning models, classifies this feature vector into one of the 8 categories using majority voting.

###### Please Note, the tool is designed in Python3.10 hence its recommended it should be run on the same. However, it can run on other Python versions as well depending on the version of packages.

 _The tool has been tested on Windows and linux environments with Python3.10._

## To run the ESKAPEE_CMD classifier tool on your local machine:


1. Clone this repository or download the zipped file and Unzip in a suitable location.

2. Setup a new virtual environment Make sure your python version is 3.10
   python -m venv venv

3. Once the virtual environment is created, activate it.
   path/to/directory/ESKAPEE_CMD>.\venv\Scripts\activate
	
    linux users: 
	path/to/directory/ESKAPEE_CMD> source venv/bin/activate

4. Now, Install the package dependencies using the given requirements.txt file.
    (venv) path/to/directory/ESKAPEE_CMD> pip install -r requirements.txt

5. Download the trained models from [here](https://drive.google.com/drive/folders/1TEz80deKo5-i2NoczavPoOD2x-ZgNq9g?role=writer). Extract the files, there are total 5 models with .sav extension and move them at the location ./Module/Models/

6. The classifier execution command takes one argument -i or -F.  
   A few sample fastq.gz files are provided with the tool at location ./Sample_Inputs/.
        -i for the path to the input gzipped file.
        -F for the path to the folder containing multiple gzipped files.

    1. For a single input gz file.
                
             (venv) path/to/directory/ESKAPEE_CMD>python main.py -i path\to\file\fname.gz
                                
              For example: (venv) path/to/directory/ESKAPEE_CMD>python main.py -i ./Input/SRR1635675.fastq.gz
          
    2. For multiple .gz files stored in a directory.
   
            (venv) path/to/directory/ESKAPEE_CMD>python main.py -F path\to\directory\containing\gzfiles
                  
            For Example: (venv) E:\ESKAPEE\ESKAPEE Classifier>python main.py -F .\Input

7. The output of the classifier will be displayed on the same terminal.

8. he same outputs can be found in .csv format at location .\Data\classification\