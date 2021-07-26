import json
from pathlib import Path
import re

import pandas as pd

def read_json(experiment_data_path):
    # find and read json files
    experiment_data_path = Path(experiment_data_path)
    data = []
    for experiment_type_folder in experiment_data_path.glob("*"):
        experiment_name = experiment_type_folder.stem
        for folder in experiment_type_folder.glob("*"):
            json_files = Path(folder).glob("evolution_data.json")
            for filepath in json_files:
                json_file = Path(filepath).open("r")
                data_unit = json.load(json_file)
                data_unit["reference culture"] = experiment_name
                data.append(data_unit)

    # transform data to a list of dictionaries
    data_list_dict = []
    for element in data:
        for i_gen in element["generations"]:
            for i, key in enumerate(element["generations"][i_gen]):
                r = re.search("[0-3][0-9].spk.txt", element["REFERENCE_PHENOTYPE"])
                div = int(r.group()[:-8])
                data_unit = {
                    "model type" : element["MODEL_TYPE"][0],
                    "dimensions" : element["DIMENSION"],
                    "population size" : element["POPULATION_SIZE"],
                    "n generations" : element["NUM_GENERATIONS"],
                    "sim duration" : element["SIMULATION_DURATION"],
                    "time step resolution" : element["TIME_STEP_RESOLUTION"],
                    "mutation p" : element["MUTATION_P"],
                    "parents p" : element["PARENTS_P"],
                    "retained adults p" : element["RETAINED_ADULTS_P"],
                    "reference phenotype" : element["REFERENCE_PHENOTYPE"],
                    "reference culture" : element["reference culture"],
                    "DIV" : div,
                    "generation" : i_gen,
                    "rank" : i+1,
                    "genotype" : element["generations"][i_gen][key]["genotype"],
                    "fitness" : element["generations"][i_gen][key]["fitness"],
                }
                data_list_dict.append(data_unit)
    
    return data_list_dict

if __name__ == "__main__":

    # path to folder with experiments
    experiment_path = Path("/home/wehak/code/ACIT4610_Semesteroppgave/RESULTS")

    # name of pickle file
    pickle_name = Path("plots/results.pkl")

    # save data as pickle file
    data = read_json(experiment_path)
    df = pd.DataFrame(data)
    df.to_pickle(pickle_name)

    print(f"Data saved to \"{pickle_name}\"")