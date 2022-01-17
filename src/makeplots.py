import pandas as pd
import numpy as np
import argparse
import yaml


def main():
    description = "Prepares the MasterCodebook to be used in 'niceplots' and generates the plots."

    cli_args = argparse.ArgumentParser(description=description, add_help=True)
    cli_args.add_argument('--pathtodata', type=str, action='store', required=True,
                          help='Path to the UltraData.cvs-files that should be used by niceplots')
    cli_args.add_argument('--pathtocodebook', type=str, action='store', required=True,
                          help="Path to the MasterCodebook to be used by niceplots.")
    ARGS = cli_args.parse_args()

    #Codebook einlsen
    codebook = pd.read_csv(ARGS.pathtocodebook)
    data = pd.read_csv(ARGS.pathtodata)





    #configfile einlesen
    with open("example.yml", "r") as f:
        config = yaml.full_load(f)

    with open("niceconfig.yml", "r") as f:
        niceconfig = yaml.full_load(f)
    
    #Filter in niceconfig überschreiben mit den in XXX'example'XXX definierten fildern
    niceconfig["filtser"] = config["filters"]
    











    codebook[niceconfig["block_id_label"]] = -1
    codebook["color_scheme" + " - nice-plots"] = niceconfig["color_scheme"]
    codebook["invert" + " - nice-plots"] = niceconfig["invert"]
    codebook["nbins" + " - nice-plots"] = niceconfig["nbins"]
    codebook["unit" + " - nice-plots"] = niceconfig["unit"]
    codebook["bar_text_color" + " - nice-plots"] = niceconfig["bar_text_color"]


    for key, value in config.items():
        position = np.where(codebook["Variable Name"] == key)[0][0]
    for innerkey, innervalue in value.items():
        if innerkey != "Group":
            codebook.at[position, innerkey + " - nice-plots"] = innervalue
        else:
            codebook.at[position, innerkey] = innervalue
    

    #last main here is the function "main()"
    from niceplots.main import main

    main("bars", ["/Users/Vale-chan/Documents/ArtologikExports/UltraData.csv"], "niceconfig.yml", codebook, "output1", False, "pdf", [""], 3)



if __name__ == "__main__":
    main()