from unittest import skip
import pandas as pd
import numpy as np
import argparse
import os
import yaml


def main():
    description = "Prepares the MasterCodebook to be used in 'niceplots' and generates the plots."

    cli_args = argparse.ArgumentParser(description=description, add_help=True)
    cli_args.add_argument('--pathtodata', type=str, action='store', required=True,
                          help='Path to the UltraData.cvs-files that should be used by niceplots')
    cli_args.add_argument('--pathtocodebook', type=str, action='store', required=True,
                          help="Path to the MasterCodebook to be used by niceplots.")
    cli_args.add_argument('--pathtoconfigfile', type=str, action='store', required=True,
                          help="Path to the config file that overrides the defaults of the nice-plot config file")
    cli_args.add_argument('--saveto', type=str, action='store', required=False, default="",
                          help='Path to where the plots shoulde be saved')
    cli_args.add_argument('--plottype', type=str, action='store', required=True,
                          help="Choose the desired plot type (bars, lines, histograms")
    cli_args.add_argument('--outputname', type=str, action='store', required=True,
                          help='Choose the name for your plots')
    cli_args.add_argument('--saveas', type=str, action='store', required=True,
                          help="Choose the desired saving format (pdf, png, svg")
    cli_args.add_argument('--timelabels', type=str, action='store', required=False, default=[""], nargs='+',
                          help="Optional: Enter the timelabels, e.g.: 2018 2019 2020")
    cli_args.add_argument('--verbosity', type=int, action='store', required=False, default=3,
                          help='Optional: Choose the verbosity level (1 = low, 4 = high') 
    cli_args.add_argument('--clearchache', action='store_true', default=False,
                         help='Optinal: Choose "True" or "False" to clear the cache. Necessary when plot sizing is changend.')               
    ARGS = cli_args.parse_args()

    #Codebook einlsen
    codebook = pd.read_csv(ARGS.pathtocodebook)
    data = pd.read_csv(ARGS.pathtodata)

    #configfile einlesen
    with open(ARGS.pathtoconfigfile, "r") as f:
        config = yaml.full_load(f)

    with open(f"{os.path.dirname(__file__)}/niceconfig.yml", "r") as f:
        niceconfig = yaml.full_load(f)
    
    #Filter in niceconfig überschreiben mit den in XXX'example'XXX definierten fildern
    niceconfig["filtser"] = config["filters"]
    
    #add columns to the codebook for niceplots to plot nice plots
    codebook[niceconfig["block_id_label"]] = -1
    codebook["color_scheme" + " - nice-plots"] = niceconfig["color_scheme"]
    codebook["invert" + " - nice-plots"] = niceconfig["invert"]
    codebook["nbins" + " - nice-plots"] = niceconfig["nbins"]
    codebook["unit" + " - nice-plots"] = niceconfig["unit"]
    codebook["bar_text_color" + " - nice-plots"] = niceconfig["bar_text_color"]

    #overrides the config-defaults of 'niceplots' ('niceconfig') with the settings in XXX'example'XXX
    for key, value in config.items():
        if key == "filters":
            continue
        position = np.where(codebook[niceconfig["name_label"]] == key)[0][0]
        for innerkey, innervalue in value.items():
            if innerkey != "Group":
                codebook.at[position, innerkey + " - nice-plots"] = innervalue
            else:
                codebook.at[position, innerkey] = innervalue
 
    
    #last main here is the function "main()"
    from niceplots.main import main

    main(ARGS.plottype, [ARGS.pathtodata], niceconfig, codebook, ARGS.outputname, ARGS.clearchache, ARGS.saveas, ARGS.timelabels, ARGS.verbosity, ARGS.saveto)

if __name__ == "__main__":
    main()