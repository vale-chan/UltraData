
import argparse
import os
import shutil
import yaml
import pandas as pd


def main():
    scriptdirectory = os.path.dirname(os.path.abspath(__file__))

    description = "XXX"
    cli_args = argparse.ArgumentParser(description=description, add_help=True)
    cli_args.add_argument('--pathtotopfolder', type=str, action='store', required=True,
                          help='
                          Path to the topfolder, where the config.yml, template.tex and Ultradata and Mastercodebook are stored.')
    cli_args.add_argument('--reportfoldername', type=str, action='store', required=True,
                          help='Choose a name for the generated report folder (will become name of the report).')
    cli_args.add_argument('--pathtodata', type=str, action='store', required=True,
                          help='Path to the UltraData.cvs-files that should be used by niceplots')
    cli_args.add_argument('--pathtocodebook', type=str, action='store', required=True,
                          help="Path to the MasterCodebook to be used by niceplots.")
    cli_args.add_argument('--reporttype', type=str, action='store', required=False, default="LE",
                          help='Type "WB" to create a report for "interne Weiterbildung", default report type is set to "LE" ("Lehrevaluation")')
    ARGS = cli_args.parse_args()

    #Codebook &  Ultradata einlesen
    codebook = pd.read_csv(ARGS.pathtocodebook)
    data = pd.read_csv(ARGS.pathtodata)

    # readin in config
    with open('fancyconfig.yaml', 'r') as f:
        config = yaml.load(f, yaml.FullLoader)

    # read in template
    with open(f"{scriptdirectory}/../Data/template{ARGS.reporttype}.tex", "r") as f:
        template = f.readlines()
    
    # replace placeholders in template
    for (key, value) in config.items():
        for ii, line in enumerate(template):
            if f"__{key}__" in line:
                template[ii] = line.replace(f"__{key}__", value)

    # Zahlenwerte irgendwie in Bericht rein bekommen, sind einzelne Werte die berechnet werden
    value = data[config["wert"][0]][4] + data[config["wert"][1]][8]
    for ii, line in enumerate(template):
        if "__value__" in line:
            template[ii] = line.replace("__value__", str(value))
    
    # table template
    table = "\\begin{table}[h!]\n" \
            "\\onehalfspacing\n" \
            "\\small\n" \
            "\\begin{tabular}{L{0.02\\textwidth}L{0.58\\textwidth}R{0.15\\textwidth}R{0.15\\textwidth}}" \
            "\\toprule" \
            "\\multicolumn{2}{l}{Studiengang/Studienbereich} & Anzahl Evaluationen & $\\emptyset$ Anzahl Items\\\\\n" \
            "\\midrule\n" \
            "__content__" \
            "\\bottomrule\n" \
            "\\end{tabular}\n" \
            "\\end{table}"
    
    content = "\\multicolumn{2}{l}{\\textbf{Sekundarstufe II} (Sek II)} & \\textbf{" + str(data[config["wert"][0]][4]) + "} & \\textbf{XX}\\\\\n" \
              "& Allgemeinbildender Unterricht (ABU) Diplomstudiengang & XX & XX\\\\"
    
    #content in table einsetzten
    table = table.replace("__content__", content)

    for ii, line in enumerate(template):
        if "__tabelle__" in line:
            template[ii] = line.replace("__tabelle__", table)
    
    #TODO: calculate stuff

    # save finished tex base to subfolder
    os.chdir(ARGS.pathtotopfolder)
    os.makedirs(ARGS.reportfoldername, exist_ok=True)
    with open(f"{ARGS.reportfoldername}/{ARGS.reportfoldername}.tex", 'w+') as f:
        f.writelines(template)
    print(__file__)
    shutil.copyfile(f"{scriptdirectory}/../Data/kreis.png", f"{ARGS.reportfoldername}/kreis.png")
    shutil.copyfile(f"{scriptdirectory}/../Data/PHSGlogo.png", f"{ARGS.reportfoldername}/PHSGlogo.png")
    shutil.copyfile(f"{scriptdirectory}/../Data/PHSGlogow.png", f"{ARGS.reportfoldername}/PHSGlogow.png")

    # compile
    os.chdir(ARGS.reportfoldername)
    os.system(f"xelatex -synctex=1 -interaction=nonstopmode {ARGS.reportfoldername}.tex")
    os.system(f"xelatex -synctex=1 -interaction=nonstopmode {ARGS.reportfoldername}.tex")


if __name__ == '__main__':
    main()