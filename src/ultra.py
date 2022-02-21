from pickle import TRUE
import pandas as pd
import numpy as np
import argparse
import copy
import glob
import os
import sys
from ast import literal_eval
pd.set_option('mode.chained_assignment', None)


def initialising(outputdirectory):
    #To-Do: haben die geladenen MasterCodebook/UltraData den richtigen inhalt?
    """This function creates an empty MasterCodebook and an empty UltraData
    or starts loading an already existing MasterCodebook and UltraData"""
    print("STARTING ULTRADATA!  ＼(〇_ｏ)／")

    if os.path.exists(f"{outputdirectory}/MasterCodebook.csv") & os.path.exists(f"{outputdirectory}/UltraData.csv"):
        MasterCodebook = pd.read_csv(f"{outputdirectory}/MasterCodebook.csv")
        # convert string representations of lists back to lists
        MasterCodebook["Alternative Labels"] = MasterCodebook["Alternative Labels"].apply(lambda x: literal_eval(str(x)))
        UltraData = pd.read_csv(f"{outputdirectory}/UltraData.csv")   
    else:
        MasterCodebook = pd.DataFrame({
            "Variable Name": ["VAR1", "VAR2", "VAR3", "VAR4", "VAR5", "VAR6", "VAR7", "VAR8", "VAR9"],
            "Label": ["DbID", "Studiengang", "Fakultät", "Geschlecht", "Jahr", "Semester", "Dozent", "Fachbereich", "Modulinfo"],
            "Alternative Labels": [["DbID"], ["Studiengang"], ["Fakultät"], ["Geschlecht"], ["Jahr"], ["Semester"], ["Dozent"], ["Fachbereich"], ["Modulinfo"]],
            "Type": ["Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo"],
            "Data Type": ["Numeric", "String", "String", "Numeric", "Numeric", "String", "String", "String", "String"],
            "Value Codes": ["none", "none", "1 = phil I\n 2 = phil II", "1 = männlich\n2 = weiblich", "none", "none", "none", "none", "none"],
            "Missing Code": [999, 999, 999, 999, 999, 999, 999, 999, 999]
            })
        print("initialised empty MasterCodebook: The Beginning Part I")

        UltraData = pd.DataFrame({
            "VAR1": [],
            "VAR2": [],
            "VAR3": [],
            "VAR4": [],
            "VAR5": [],
            "VAR6": [],
            "VAR7": [],
            "VAR8": [],
            "VAR9": []
            })
    
    print("initialised empty UltraData: The Beginning Part II")
    return MasterCodebook, UltraData


def deletewhitespaces(exportdata):
    """WhiteSpace lösche in "Variable View" und "Data" (die beiden Datenblätter aus dem Excelexport)"""
    for datasheet in exportdata.keys():
        for column in exportdata[datasheet]:
            if exportdata[datasheet][column].dtype == "object":
                exportdata[datasheet][column] = exportdata[datasheet][column].str.strip()
            exportdata[datasheet] = exportdata[datasheet].rename(columns={column: column.strip()})
    print("all white spaces stripped")
    return exportdata


def expandMasterCodebook(exportfile, exportdata, matchingtable, MasterCodebook):
    #To-Do: innehaue, dasses frogt, ob meh das als alternatives lable will
    """Finds and matches Labels of the exported data with the labels in the MasterCodebook.
    New lables are added to the MasterCodebook and to the alternative labes of the new label."""
    print("find & match labels of exportdata and MasterCodebook")
    for _,row in exportdata["VariableView"].iterrows():
        exportlabel = row["Label"]
        print(row["Variable Name"])
        found = False

        #Schaut, ob das Label schon irgendwo in den alternativen Labels vorkommt.
        #Wenn ja, wird ein Eintrag im "matchingtabel" erstellt und der Loop bricht ab.
        for ii,xx in enumerate(MasterCodebook["Alternative Labels"]):
            if exportlabel in xx:
                matchingtable[row["Variable Name"]] = MasterCodebook["Variable Name"].iloc[ii]
                found = True
                break

        #Wenn Eintrag nicht gefunden wurde, wird das Label zu den alternativen Labels hinzugefügt.
        #Das Label wird danach neu benannt & das alte und neue Label kommen in's "matchingtable"
        #Das ganze kommt dann als neue Zeile ins "MasterCodebook"
        if not found:
            VIOLET = '\033[95m'
            YELLOW = '\033[93m'
            BOLD = '\033[1m'
            ENDC = '\033[0m'
            while True:
                text = input(f"\n{VIOLET}New label found:{ENDC} \'{row['Label']}\'"
                            f"\n{VIOLET}in:{ENDC} {exportfile}"
                            f"\n{VIOLET}Type in an {BOLD}existing variable number{ENDC}{VIOLET} (i.e. {BOLD}'1'{ENDC}{VIOLET} for VAR1)"
                            f" to add the label as alternative label or type {BOLD}'n'{ENDC}{VIOLET} to create a new variable: {ENDC}")
                
                if text == "n":
                    z = copy.deepcopy(row)
                    z["Alternative Labels"] = [row["Label"]]
                    varnameneu = "VAR" + str((MasterCodebook.shape[0]+1))
                    matchingtable[z["Variable Name"]] = varnameneu
                    z["Variable Name"] = varnameneu
                    MasterCodebook = MasterCodebook.append(z, ignore_index=True)
                    break
                elif isnumber(text):
                    if int(text) > MasterCodebook.shape[0]:
                        print(f"{YELLOW}Invalid variable name. Try again.{ENDC}")
                        continue
                    if ("VAR"+text in list(matchingtable.values())):
                        print(f"{YELLOW}Double entry detected! It is not possible to add two new variables to the same existing one.{ENDC}")
                        print(f"{YELLOW}Invalid input. Try again.{ENDC}")
                        continue
                    position = np.array(MasterCodebook["Variable Name"] == "VAR"+text)
                    temp = MasterCodebook.loc[position]["Alternative Labels"][np.where(position)[0][0]]
                    temp.append(row["Label"])
                    MasterCodebook["Alternative Labels"].loc[np.where(position)[0][0]] = temp
                    z = copy.deepcopy(row)
                    matchingtable[z["Variable Name"]] = "VAR"+text
                    break
                else:
                    print(f"{YELLOW}Invalid input. Try again.{ENDC}")
    return matchingtable, MasterCodebook


def isnumber(string):
    number = False
    try:
        int(string)
        number = True
    except ValueError:
        pass
    return number


def addmetadata(ARGS, exportfile, data, UltraData):
    """Exstracts the metadata out of the file's name (makes it nicer looking) and adds it to the data"""
    print("seraching for meta-information")
    RED = '\033[31m'
    VIOLET = '\033[95m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

    exportname = os.path.basename(exportfile)

    if ARGS.evaluationtype == "LE":
        metainfo = {
            "Studiengang": "",
            "Jahr": "20" + exportname.split("_")[0][-2:],
            "Semester": exportname.split("_")[0][:-2],
            "Dozent": exportname.split("_")[2],
            "Fachbereich": "",       
            "Modulinfo": " ".join(exportname.split("_")[3:])[:-5]
            }

        print("beautifying meta-information")
        if (metainfo["Semester"] == "HeS") | (metainfo["Semester"] == "FrS"):
            metainfo["Semester"] = metainfo["Semester"][:1] + metainfo["Semester"][-1:]


        studiengang_fachbereich = exportname.split("_")[1]

        if studiengang_fachbereich[:3] == "Sek":
            metainfo["Studiengang"] = " ".join(studiengang_fachbereich.split(" ")[:2])
            metainfo["Fachbereich"] = " ".join(studiengang_fachbereich.split(" ")[2:])
        elif studiengang_fachbereich[:3] == "KGP":
            metainfo["Studiengang"] = studiengang_fachbereich.split(" ")[0]
            metainfo["Fachbereich"] = " ".join(studiengang_fachbereich.split(" ")[1:])
        elif studiengang_fachbereich[:3] == "Mas":
            metainfo["Studiengang"] = studiengang_fachbereich.split(" ")[0]
            metainfo["Fachbereich"] = " ".join(studiengang_fachbereich.split(" ")[1:])
        else:
            raise ValueError(f"Studiengang nicht definiert:\nDatei: {exportname}\nStudiengang_Fachbereich: {studiengang_fachbereich}")
    
    elif ARGS.evaluationtype == "WB":
        metainfo = {
            "Studiengang": exportname.split("-")[0].strip(),
            "Jahr": "20" + exportname.split("-")[1].strip(),
            "Semester": 999,
            "Dozent": exportname.split("-")[2].strip(),
            "Fachbereich": 999,
            "Modulinfo": " ".join(exportname.split("-")[3:])[:-5].replace("  ", " ")
            }

    else:
        raise ValueError(f"\{RED}Ungültiger Evaluationstypus!{ENDC}\n"
                         f"Bitte '\{YELLOW}LE'\{ENDC} für Lehrevaluation eingeben\n"
                         f"Bitte '\{YELLOW}WB'\{ENDC} für interne Weiterbildung eingeben\n")


    check = (UltraData["VAR2"] == metainfo["Studiengang"]) &\
            (UltraData["VAR5"] == int(metainfo["Jahr"])) &\
            (UltraData["VAR6"] == metainfo["Semester"]) &\
            (UltraData["VAR7"] == metainfo["Dozent"]) &\
            (UltraData["VAR8"] == metainfo["Fachbereich"]) &\
            (UltraData["VAR9"] == metainfo["Modulinfo"])
    
    skip = False
    

    if check.any():
        skip = True
    else:
        data["Studiengang"] = metainfo["Studiengang"]
        data["Jahr"] = metainfo["Jahr"]
        data["Semester"] = metainfo["Semester"]
        data["Dozent"] = metainfo["Dozent"]
        data["Fachbereich"] = metainfo["Fachbereich"]
        data["Modulinfo"] = metainfo["Modulinfo"]
        print("meta-information added to data")

    return data, skip


def recodevalues(data):
    """The string values for 'Geschlecht' and 'Fakultät' are recoded to numeric values,
    according to the values in the above defined MasterCodebook"""
    data = data.replace(to_replace={"phil. I":1, "phil. II":2, "Herr":1, "Frau":2})
    return data


def fitdatatoUltraData(data, UltraData):
    """Finds columns, which are only occuring in data or UltraData.
    Those additional columns from UltraData are added to data and vice versa."""
    print("drawing ven-diagramm to find overlaps")
    ###Block hier macht "data" und "UltraData" gleich gross###
    columnsdata = np.asarray(data.columns)
    columnsultradata = np.asarray(UltraData.columns)

    #Schmeisst Kolonnen aus "data" und "UltraDAta" zusammen
    union = np.union1d(columnsdata, columnsultradata)

    #Kolonnen, welche nicht in "data" sind (sind in "UltraData") und daher zu "data" hinzugefügt werden müssen
    notindata = np.setdiff1d(union, columnsdata)
    #Kolonnen, welche nicht in "UltraData" sind (sind in "data") und daher zu "UltraData" hinzugefügt werden müssen
    notinultradata = np.setdiff1d(union, columnsultradata)

    for column in notindata:
        data[column] = 999

    for column in notinultradata:
        UltraData[column] = 999

    columnsdata = np.asarray(data.columns)
    columnsultradata = np.asarray(UltraData.columns)

    #Kontrolliert, ob die Kolonnen "data" und "UltraData" gleich sind
    assert np.array_equal(np.sort(columnsdata), np.sort(columnsultradata))
    print("overlaps found")

    return(data, UltraData)


def setcolumntype(UltraData):
    """Sets the right datatype for each columne."""
    for column in UltraData.columns:
        try:
            UltraData[column] = pd.to_numeric(UltraData[column], downcast="float")
        except ValueError:
            pass
        try:
            UltraData[column] = pd.to_numeric(UltraData[column], downcast="integer")
        except ValueError:
            pass
    return(UltraData)
    

def main():
    description = "Fuses different data-tables to one big one and expands a codebook accordingly"
    cli_args = argparse.ArgumentParser(description=description, add_help=True)
    cli_args.add_argument('--evaluationtype', type=str, action='store', required=False, default="LE",
                          help='Choose if the data is from a "Lehrevaluation" (=LE) or "interne Weiterbildung" (=WB)')
    cli_args.add_argument('--pathtodatafolder', type=str, action='store', required=True,
                          help='Path to the folders of the data.cvs-files that should be added to the UltraData.')
    cli_args.add_argument('--pathtosavingfolder', type=str, action='store', required=True,
                          help="Path to where the UltraData and MasterCodebook should be saved to.")
    ARGS = cli_args.parse_args()

    MasterCodebook, UltraData = initialising(ARGS.pathtosavingfolder)

    print("starting Mega-Process")
    for exportfile in glob.glob(f"{ARGS.pathtodatafolder}/*.xlsx"):
        print(f"working on {exportfile}")
        
        exportdata = pd.read_excel(io=exportfile, sheet_name=None, engine="openpyxl")
        print(f"sheets scanned")

        exportdata = deletewhitespaces(exportdata)
        
        print("generating matchingtable")
        matchingtable = {"DbID": "VAR1",
                         "Studiengang": "VAR2",
                         "SEK": "VAR3",
                         "Anrede": "VAR4",
                         "Jahr": "VAR5",
                         "Semester": "VAR6",
                         "Dozent": "VAR7",
                         "Fachbereich": "VAR8",
                         "Modulinfo": "VAR9"}

        matchingtable, MasterCodebook = expandMasterCodebook(exportfile, exportdata, matchingtable, MasterCodebook)

        data = exportdata["Data"]

        data = data.drop(errors="ignore", columns=[
                                "Befragten ID",
                                "Angezeigter Name",
                                "Vorname",
                                "Nachname",
                                "Organisation",
                                "E-Mail",
                                "Adresse",
                                "Postleitzahl",
                                "Stadt",
                                "Land",
                                "Telefon",
                                "Handy",
                                "Sprache",
                                "Halbgruppe A",
                                "Halbgruppe B",
                                "Alter",
                                "Unternehmen",
                                "Beruf",
                                "Wohnsituation",
                                "Studienjahrgang",
                                "Familienstand",
                                "Studiengang",
                                "Lerngruppe",
                                "Lerngruppe klein",
                                "Funktion",
                                "Diplomtyp",
                                "Ort",
                                "Studienbereich",
                                "Organisation.1",
                                "ID"
                                ])
        

        data, skip = addmetadata(ARGS, exportfile, data, UltraData)
        
        if skip:
            continue

        data = recodevalues(data)

        print("applying matchingtable")
        data = data.rename(columns=matchingtable)
        print("matchingtable application completed")

        data, UltraData = fitdatatoUltraData(data, UltraData)

        UltraData = UltraData.append(data)
        print("data added to UltraData")
        
        
    UltraData = setcolumntype(UltraData)
    UltraData.to_csv(f"{ARGS.pathtosavingfolder}/UltraData.csv", index=False)
    MasterCodebook.to_csv(f"{ARGS.pathtosavingfolder}/MasterCodebook.csv", index=False)


if __name__ == "__main__":
    main()