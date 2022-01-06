import pandas as pd
import numpy as np
import copy
import glob
import os


def main():
    #To-Do: input throught terminal
    inputdirectory = "/Users/Vale-chan/Documents/ArtologikExports/EinzelExport"
    outputdirectory = "/Users/Vale-chan/Documents/ArtologikExports"

    print("STARTING ULTRADATA!  ＼(〇_ｏ)／")

    MasterCodebook = pd.DataFrame({
        "Variable Name": ["VAR1", "VAR2", "VAR3", "VAR4", "VAR5", "VAR6", "VAR7", "VAR8", "VAR9"],
        "Label": ["DbID", "Studiengang", "Fakultät", "Geschlecht", "Jahr", "Semester", "Dozent", "Fachbereich", "Modulinfo"],
        "Alternative Labels": [["DbID"], ["Studiengang"], ["Fakultät"], ["Geschlecht"], ["Jahr"], ["Semester"], ["Dozent"], ["Fachbereich"], ["Modulinfo"]],
        "Type": ["Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo", "Metainfo"],
        "Data Type": ["Numeric", "String", "String", "Numeric", "Numeric", "String", "String", "String", "String"],
        "Value Codes": ["none", "none", "1 = phil I\n 2 = phil II", "1 = männlich\n2 = weiblich", "none", "none", "none", "none", "none"],
        "Missing Code": [999, 999, 999, 999, 999, 999, 999, 999, 999]
        }
    )
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
        }
    )
    print("initialised empty UltraData: The Beginning Part II")

    #To-Do: nicht jedesmal neues MasterCodebuch genereieren & UltraData

    print("starting Mega-Process")
    for exportfile in glob.glob(f"{inputdirectory}/*.xlsx"):
        print(f"working on {exportfile}")
        
        exportdata = pd.read_excel(io=exportfile, sheet_name=None, engine="openpyxl")
        print(f"sheets scanned")
        
        #WhiteSpace lösche in "Variable View" und "Data" (die beiden Datenblätter aus dem Excelexport)
        for datasheet in exportdata.keys():
            for column in exportdata[datasheet]:
                exportdata[datasheet][column].dtype
                if exportdata[datasheet][column].dtype == "object":
                    exportdata[datasheet][column] = exportdata[datasheet][column].str.strip()
        print("all white spaces stripped")
        
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

        print("find & match labels of exportdata and MasterCodebook")
        for _,row in exportdata["VariableView"].iterrows():
            exportlabel = row["Label"]
            found = False

            #Schaut, ob das Label schon irgendwo in den alternativen Labels vorkommt.
            #Wenn ja, wird ein Eintrag im "matchingtabel" erstellt und der Loop bricht ab.
            for ii,xx in enumerate(MasterCodebook["Alternative Labels"]):
                if exportlabel in xx:
                    matchingtable[row["Variable Name"]] = MasterCodebook["Variable Name"].iloc[ii]
                    found = True
                    break

            #Wenn Eintrag nicht gefunden wurde, wird das Label zu den alternativen Labels hinzugefügt.
            #Das Label wird danach neu benannt &  das alte und neue Label kommen in's "matchingtable"
            #Das ganze kommt dann als neue Zeile ins "MasterCodebook"
            if not found:
                # TODO
                # innehaue, dasses frogt, ob meh das als alternatives lable will
                z = copy.deepcopy(row)
                z["Alternative Labels"] = [row["Label"]]
                varnameneu = "VAR" + str((MasterCodebook.shape[0]+1))
                matchingtable[z["Variable Name"]] = varnameneu
                z["Variable Name"] = varnameneu
                MasterCodebook = MasterCodebook.append(z)
        
        print("seraching for meta-information")
        exportname = os.path.basename(exportfile)

        exportname.split("_")

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
        
        data = exportdata["Data"]

        data = data.drop(columns=[
                                "Befragten ID",
                                "Angezeigter Name ",
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
        
        data["Studiengang"] = metainfo["Studiengang"]
        data["Jahr"] = metainfo["Jahr"]
        data["Semester"] = metainfo["Semester"]
        data["Dozent"] = metainfo["Dozent"]
        data["Fachbereich"] = metainfo["Fachbereich"]
        data["Modulinfo"] = metainfo["Modulinfo"]
        print("meta-information added to data")

        print("applying matchingtable")
        data = data.rename(columns=matchingtable)
        print("matchingtable application completed")

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
            data[column] = np.NaN

        for column in notinultradata:
            UltraData[column] = np.NaN

        columnsdata = np.asarray(data.columns)
        columnsultradata = np.asarray(UltraData.columns)

        #Kontrolliert, ob die Kolonnen "data" und "UltraData" gleich sind
        assert np.array_equal(np.sort(columnsdata), np.sort(columnsultradata))
        print("overlaps found")

        UltraData = UltraData.append(data)
        print("data added to UltraData")

    UltraData.to_csv(f"{outputdirectory}/UltraData.csv", index=False)
    MasterCodebook.to_csv(f"{outputdirectory}/MasterCodebook.csv", index=False)


















if __name__ == "__main__":
    main()