The Dreams - Anleitung


INTRODUCTION
UltraData was developed to produce reports based on multiple datasets with the help of nice-plots. UltraData works in three steps:
1. Aggregation of the datasets to one dataset
2. Plotting the data using nice-plots
3. Insert the plots in a prefixed report template
Each of the three steps needs a seperate command.

Installation - UltraData
1. Open a terminal and clone the UltraData repository „git clone https://github.com/vale-chan/UltraData.git“

Installation - nice-plots
1. Open a terminal and clone the nice-plots repository „git clone https://github.com/DZuercher/nice-plots.git“
2. Enter the nice-plots directory „cd nice-plots“
3. Install nice-plots „pip3 install . --user“

USAGE
ultradata - aggregation of datasets
Run „python3 ultra.py --help“ to get a list of arguments that UltraData accepts:

--pathtodatafolder: Path to where all the .cvs-files are stored which should be aggregated by UltraData.
--pathtosavingfolder: Argument to save the newly created dataset in a specified directory.
--evaluationtype: optional; choose if the data derives from a "Lehrevaluation" (=LE) or "interne Weiterbildung" (=WB), the standard is set for „Lehrevaluation“.

**
example:
python3 ultra.py --evaluationtype=WB --pathtodatafolder=/Users/Vale-chan/Documents/ArtologikExports/TestDokumentation --pathtosavingfolder=/Users/Vale-chan/Documents/ArtologikExports/TestDokumentation
**

The first time UltraData is runned it creats two files: „UltraData.csv“ and „MasterCodebook.csv“. UltraData.csv“ contains all the aggregated data, while „MasterCodebook.csv“ contains the metainformation about the dataset (such as question-lable, data-type, etc.). If more data should be added to an existing „UltraData.csv“ the --pathtodatafolder can be directed to the existing „UltraData.csv“ and „MasterCodebook.csv“, UltraData will use those files and add the new data.

——————————————

ultra2nice - plotting of data
Run „python3 ultra2nice.py --help“ to get a list of arguments that UltraData accepts:

--pathtodata: Path to the „UltraData.cvs“ which niceplots should be using.
--pathtocodebook: Path to the „MasterCodebook.cvs“ which niceplots should be using. niceplots needs the metainformation from the „MasterCodebook.cvs“ to create labels, etc. for the plots. It will creat a new codebook with additional metainformation. For more detailled informations go to https://github.com/DZuercher/nice-plots
--pathtoconfigfile: The config-file contains all the variables that need to be plotted togehter wiht informations like the colour scheme, as well as filters, etc.. This file is not the „niceconfig“-file, which contains the style-informations for the plots.
--saveto: Argument to specify the directory for saving the plots.
--plottype: Choose the desired plot type; one can choose between „bars“, „lines“, „histograms“, and „timeline“.
--outputname: Choose the name for your plots, every plot created will have the same name + a number, starting with 0.
--saveas: Choose the desired saving format; one can choos beween „pdf“, „png“ and „svg“.
--timelabels: TIMELABELS [TIMELABELS ...] Optional: Enter the timelabels, e.g.: 2018 2019 2020
--verbosity: Optional; Choose the verbosity level (1 = low, 4 = high)
--clearchache: Optinal: Choose "True" or "False" to clear the cache. Necessary when plot sizing is changend.

**
example:
python3 ultra2nice.py --pathtodata=/Users/Vale-chan/Documents/ArtologikExports/TestDokumentation/UltraData.csv --pathtocodebook=/Users/Vale-chan/Documents/ArtologikExports/TestDokumentation/MasterCodebook.csv --pathtoconfigfile=/Users/Vale-chan/Documents/ArtologikExports/TestDokumentation/config.yml  --saveto=/Users/Vale-chan/Documents/ArtologikExports/TestDokumentation --outputname=bars --plottype=bars --saveas=pdf
**

ultra2nice will create a new folder with a new „UltraData.csv“ and „MasterCodebook.csv“ and config-file for each new --outputname. If the plots styling needs to be adjusted, either use the newly created config-file or delet the folder to use the previous config-file.

——————————————

nice2fancy - creation of report
Run „python3 nice2fancy.py --help“ to get a list of arguments that UltraData accepts:

--pathtotopfolder: PATHTOTOPFOLDER
                        Path to the topfolder, where the config.yml,
                        template.tex and Ultradata and Mastercodebook are
                        stored.
  --reportfoldername REPORTFOLDERNAME
                        Choose a name for the generated report folder (will
                        become name of the report).
  --pathtodata PATHTODATA
                        Path to the UltraData.cvs-files that should be used by
                        niceplots
  --pathtocodebook PATHTOCODEBOOK
                        Path to the MasterCodebook to be used by niceplots.
  --reporttype REPORTTYPE
                        Type "WB" to create a report for "interne
                        Weiterbildung", default report type is set to "LE"
                        ("Lehrevaluation")



--pathtodata: Path to the „UltraData.cvs“ which niceplots should be using.
--pathtocodebook: Path to the „MasterCodebook.cvs“ which niceplots should be using. niceplots needs the metainformation from the „MasterCodebook.cvs“ to create labels, etc. for the plots. It will creat a new codebook with additional metainformation. For more detailled informations go to https://github.com/DZuercher/nice-plots
--pathtoconfigfile: Path to the config-file that overrides the defaults of the nice-plot config-file. This confic-file is used to determine the styling specifics of the plots.
--saveto: Argument to specify the directory for saving the plots.
--plottype: Choose the desired plot type; one can choose between „bars“, „lines“, „histograms“, and „timeline“.
--outputname: Choose the name for your plots, every plot created will have the same name + a number, starting with 0.
--saveas: Choose the desired saving format; one can choos beween „pdf“, „png“ and „svg“.
--timelabels: TIMELABELS [TIMELABELS ...] Optional: Enter the timelabels, e.g.: 2018 2019 2020
--verbosity: Optional; Choose the verbosity level (1 = low, 4 = high)
--clearchache: Optinal: Choose "True" or "False" to clear the cache. Necessary when plot sizing is changend.

ultra2nice will create a new folder with a new „UltraData.csv“ and „MasterCodebook.csv“ and config-file for each new --outputname. If the plots styling needs to be adjusted, either use the newly created config-file or delet the folder to use the previous config-file.

