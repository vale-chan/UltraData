
import argparse
import os
import shutil
import yaml


def main():
    scriptdirectory = os.path.dirname(os.path.abspath(__file__))

    description = "XXX"
    cli_args = argparse.ArgumentParser(description=description, add_help=True)
    cli_args.add_argument('--pathtotopfolder', type=str, action='store', required=True,
                          help='Path to the topfolder, where the config.yml, template.tex and Ultradata and Mastercodebook are stored.')
    cli_args.add_argument('--reportfoldername', type=str, action='store', required=True,
                          help='Choose a name for the generated report folder (will become name of the report).')
    ARGS = cli_args.parse_args()

    # readin in config
    with open('fancyconfig.yaml', 'r') as f:
        config = yaml.load(f, yaml.FullLoader)

    # read in template
    with open(f"{scriptdirectory}/../Data/template.tex", "r") as f:
        template = f.readlines()
    
    # replace placeholders in template
    for (key, value) in config.items():
        for ii, line in enumerate(template):
            if f"__{key}__" in line:
                template[ii] = line.replace(f"__{key}__", value)
    
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