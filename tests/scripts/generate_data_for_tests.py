"""script run by Makefile test-data-generate command

makes all the 'generated' test data, i.e. files created by vak,
It's called 'generated' test data to distinguish it from the
'source' test data, i.e., files **not** created by vak, that is,
the input data used when vak does create files (csv files, logs,
neural network checkpoints, etc.)

This script generates:
* temporary config.toml files used when generating results
* `prep`d (prepared) datasets, and results created with those datasets,
  both of which were generated using the temporary config.toml files

all the setup configs send output to one of two places:
for any prep command, the output goes to some child directory of ./tests/data_for_tests/generated/prep
for any command run with a `prep`d dataset, the output goes to some child dir of ./tests/data_for_tests/generated/results

examples:
    when we run `vak prep tests/data_for_tests/generated/configs/test_train_audio_wav_annot_koumura.toml`
    the `prep`d dataset will be in a new directory created in
    `./tests/data_for_tests/generated/prep/train/audio_wav_annot_koumura`

    when we run `vak train tests/data_for_tests/genereated/configs/test_train_audio_wav_annot_koumura.toml`
    it will use the `prep`d dataset csv that's now in
    `./tests/data_for_tests/generated/prep/train/audio_wav_annot_koumura`, that the temporary config.toml points to,
    and the results will go to a new directory created in
    `./tests/data_for_tests/generated/results/train/audio_wav_annot_koumura`

To set up this directory structure, we iterate through the constants defined below.

The constants are:
- TOP_LEVEL_DIRS
    name of sub-directories in .tests/data_for_tests/generated that correspond to
    either tempory config files, 'prep'd datasets, or `results` generated from those `prep`d datasets
- COMMAND_DIRS
    names of sub-sub-directories in ./tests/data_for_tests/generated/prep &
    ./tests/data_for_tests/generated/results that correspond to cli commands;
    e.g., dataset from running `vak prep $A_TRAIN_CONFIG.TOML` will be in
    ./tests/data_for_tests/generated/prep/train/audio_{}_annot_{}
- DATA_DIRS
    names of "subsub"directories in ./tests/data_for_tests/$COMMAND that correspond to toy test data sets;
    those sub-directories contain test data generated by $COMMAND using the specified toy test data set

In other words, the parent directory for all the generated directories we need to remove
will have a path of the form: `./tests/data_for_tests/$TOP_LEVEL_DIRS/COMMAND_DIRS/DATA_DIRS`.
For example:
The prep`d dataset from running `vak prep $AUDIO_CBIN_ANNOT_NOTMAT_CONFIG.TOML` will be in
`./tests/data_for_tests/prep/train/audio_cbin_annot_notmat`
and corresponding results will be in
`./tests/data_for_tests/results/train/audio_cbin_annot_notmat`
The directories will have names with timestamps like `prep_20201015_1115`.
Those are the generated directories we want to remove.
"""
from pathlib import Path
import shutil

import toml
import vak

HERE = Path(__file__).parent
TEST_DATA_ROOT = HERE / ".." / "data_for_tests"
GENERATED_TEST_DATA = TEST_DATA_ROOT / "generated"
GENERATED_TEST_CONFIGS_ROOT = GENERATED_TEST_DATA / "configs"

# convention is that all the config.toml files in tests/data_for_tests/configs
# that should be run when generating test data
# have filenames of the form `{MODEL}_{COMMAND}_audio_{FORMAT}_annot_{FORMAT}.toml'
# **or** `{MODEL}_{COMMAND}_spect_{FORMAT}_annot_{FORMAT}_config.ini'
# e.g., 'tweetynet_learncurve_audio_cbin_annot_notmat.toml'.
# Below, we iterate over model names
# so glob doesn't pick up static configs that are just used for testing,
# like 'invalid_option_config.toml`
TEST_CONFIGS_ROOT = TEST_DATA_ROOT.joinpath("configs")
CONFIGS_TO_RUN = []
MODELS = ("teenytweetynet", "tweetynet")
for model in MODELS:
    CONFIGS_TO_RUN.extend(sorted(TEST_CONFIGS_ROOT.glob(f"{model}*.toml")))

# the sub-directories that will get made inside `./tests/data_for_tests/generated`
TOP_LEVEL_DIRS = [
    "configs",
    "prep",
    "results",
]

# these sub-dirs get made in each of the TOP_LEVEL_DIRS (except for 'configs')
COMMAND_DIRS = [
    "eval",
    "learncurve",
    "predict",
    "train",
]

# these sub-dirs get made in each of the COMMAND_DIRS (except for 'configs')
DATA_DIRS = [
    "audio_cbin_annot_notmat",
    "audio_wav_annot_koumura",
    "spect_mat_annot_yarden",
]


def make_subdirs_in_generated():
    """make sub-directories inside ./tests/data_for_tests/generated

    first thing that has to get done before copying configs and
    then using those configs to generate results

    makes three directories in data_for_tests/generated:
    configs, prep, and results.
    prep has one sub-directory for every data "type".
    results does also, but in addition will have sub-directories
    within those for models.
    """
    for top_level_dir in TOP_LEVEL_DIRS:
        if top_level_dir == "configs":
            subdir_to_make = GENERATED_TEST_DATA / top_level_dir
            subdir_to_make.mkdir(parents=True)
        else:
            for command_dir in COMMAND_DIRS:
                for data_dir in DATA_DIRS:
                    if top_level_dir == "prep":
                        subdir_to_make = (
                            GENERATED_TEST_DATA / top_level_dir / command_dir / data_dir
                        )
                        subdir_to_make.mkdir(parents=True)
                    else:
                        for model in MODELS:
                            subdir_to_make = (
                                GENERATED_TEST_DATA
                                / top_level_dir
                                / command_dir
                                / data_dir
                                / model
                            )
                            subdir_to_make.mkdir(parents=True)


def copy_config_files():
    """copy config files from setup to data_for_tests/configs

    the copied files are the ones that get modified when this setup script runs,
    while the originals in this directory remain unchanged.
    """
    copied_configs = []

    for toml_path in CONFIGS_TO_RUN:
        if not toml_path.exists():
            raise FileNotFoundError(f"{toml_path} not found")

        dst = GENERATED_TEST_CONFIGS_ROOT.joinpath(toml_path.name)
        print(f"\tcopying to {dst}")
        shutil.copy(src=toml_path, dst=dst)
        copied_configs.append(dst)

    return copied_configs


def run_prep(config_paths):
    """run ``vak prep`` to generate data for testing"""
    for config_path in config_paths:
        if not config_path.exists():
            raise FileNotFoundError(f"{config_path} not found")
        print(
            f"running vak prep to generate data for tests test, using config: {config_path.name}"
        )
        vak.cli.prep.prep(toml_path=config_path)


def fix_options_in_configs(config_paths, command):
    """fix values assigned to options in predict and eval configs

    Need to do this because both predict and eval configs have options
    that can only be assigned *after* running the corresponding `train` config
    """
    # split configs into train and predict or eval configs
    configs_to_fix = [config for config in config_paths if command in config.name]
    train_configs = [config for config in config_paths if "train" in config.name]

    for config_to_fix in configs_to_fix:
        # figure out which 'train' config corresponds to this 'predict' or 'eval' config
        # by using 'suffix' of config file names. `train` suffix will match `predict`/'eval' suffix
        prefix, suffix = config_to_fix.name.split(command)
        train_config_to_use = []
        for train_config in train_configs:
            train_prefix, train_suffix = train_config.name.split("train")
            if train_suffix == suffix:
                train_config_to_use.append(train_config)
        if len(train_config_to_use) != 1:
            raise ValueError(
                f"did not find just a single train config that matches with predict config:\n"
                f"{config_to_fix}"
                f"Matches were: {train_config_to_use}"
            )
        train_config_to_use = train_config_to_use[0]

        # now use the config to find the results dir and get the values for the options we need to set
        # which are checkpoint_path, spect_scaler_path, and labelmap_path
        with train_config_to_use.open("r") as fp:
            train_config_toml = toml.load(fp)
        root_results_dir = Path(train_config_toml["TRAIN"]["root_results_dir"])
        results_dir = sorted(root_results_dir.glob("results_*"))
        if len(results_dir) != 1:
            raise ValueError(
                f"did not find just a single results directory in root_results_dir from train_config:\n"
                f"{train_config_to_use}"
                f"root_results_dir was: {root_results_dir}"
                f'Matches for "results_*" were: {results_dir}'
            )
        results_dir = results_dir[0]
        # these are the only options whose values we need to change
        # and they are the same for both predict and eval
        checkpoint_path = sorted(results_dir.glob("**/checkpoints/checkpoint.pt"))[0]
        spect_scaler_path = sorted(results_dir.glob("StandardizeSpect"))[0]
        labelmap_path = sorted(results_dir.glob("labelmap.json"))[0]

        # now add these values to corresponding options in predict / eval config
        with config_to_fix.open("r") as fp:
            config_toml = toml.load(fp)
        config_toml[command.upper()]["checkpoint_path"] = str(checkpoint_path)
        config_toml[command.upper()]["spect_scaler_path"] = str(spect_scaler_path)
        config_toml[command.upper()]["labelmap_path"] = str(labelmap_path)
        with config_to_fix.open("w") as fp:
            toml.dump(config_toml, fp)


# need to run 'train' config before we run 'predict'
# so we can add checkpoints, etc., from training to predict
COMMANDS = (
    "train",
    "learncurve",
    "eval",
    "predict",
)


def main():
    print(
        "making sub-directories in ./tests/data_for_tests/generated/ where files generated by `vak` will go"
    )
    make_subdirs_in_generated()

    print(
        "copying config files run to generate test data from ./tests/data_for_tests/configs to "
        "./tests/data_for_tests/generated/configs"
    )
    config_paths = copy_config_files()

    print(f"will generate test data from these config files: {config_paths}")

    # ---- only need to run prep once, since prep'd data is the same regardless of model ----
    prep_config_paths = [
        config_path
        for config_path in config_paths
        if config_path.name.startswith(MODELS[0])
    ]
    run_prep(config_paths=prep_config_paths)
    # now add the prep csv from those configs to the corresponding config
    # from all the other models
    for model in MODELS[1:]:
        model_config_paths = [
            config_path
            for config_path in config_paths
            if config_path.name.startswith(model)
        ]
        for model_config_path in model_config_paths:
            # we want the same prep config for MODEL[0] which will have the
            # exact same name, but with a different model name as the "prefix"
            stem_minus_model = model_config_path.stem.replace(model, "")
            prep_config_path = [
                prep_config_path
                for prep_config_path in prep_config_paths
                if prep_config_path.stem.endswith(stem_minus_model)
            ]
            assert len(prep_config_path) == 1
            prep_config_path = prep_config_path[0]
            with prep_config_path.open("r") as fp:
                prep_config_toml = toml.load(fp)
            with model_config_path.open("r") as fp:
                model_config_toml = toml.load(fp)
            # find the section that `vak prep` added the `csv_path` to,
            # and set `csv_path` for model config to the same value in
            # the same section for this model config
            for section_name, options_dict in prep_config_toml.items():
                if "csv_path" in options_dict:
                    model_config_toml[section_name]["csv_path"] = options_dict[
                        "csv_path"
                    ]
            with model_config_path.open("w") as fp:
                toml.dump(model_config_toml, fp)

    for model in MODELS:
        for command in COMMANDS:
            if command == "prep":
                continue  # already ran 'prep'
            print(f"running configs for command: {command}")
            command_config_paths = [
                config_path
                for config_path in config_paths
                if config_path.name.startswith(model) and command in config_path.name
            ]
            print(f"using the following configs:\n{command_config_paths}")
            if command == "predict" or command == "eval":
                # fix values for required options in predict / eval configs
                # using results from running the corresponding train configs.
                # this only works if we ran the train configs already,
                # which we should have because of ordering of COMMANDS constant above
                copied_config_paths_this_model = [
                    config_path
                    for config_path in config_paths
                    if config_path.name.startswith(model)
                ]
                fix_options_in_configs(copied_config_paths_this_model, command)

            for config_path in command_config_paths:
                vak.cli.cli.cli(command, config_path)


if __name__ == "__main__":
    main()
