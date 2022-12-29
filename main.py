#!/usr/bin/python3

import os
import random
import click

from helpers import (
    find_all_target_files,
    get_sample_processor,
    compare_file_to_target_sample,
    update_target_values,
)


@click.command()
@click.option(
    "--sample-type",
    "-s",
    type=click.Choice(["octa", "tracker", "rample"]),
    help="Target Sample type to use",
)
@click.option(
    "--bit-depth",
    "-bit",
    type=click.Choice(["8", "16", "24", "32"]),
    default=None,
    help="Force bit depth to a specific value",
)
@click.option(
    "--sample_rate",
    "-srate",
    type=click.Choice([
        "44.1", "48", "88.2", "96", "176.4", "192",
        "44100", "48000", "88200", "96000", "176400", "192000"
    ]),
    default=None,
    help="Force sample rate to specific value, \
        44.1 and 44100 are similarly mapped"
)
@click.option(
    "--force_mono",
    "-mono",
    is_flag=True,
    default=False,
    help="Ensure all files are set to mono"
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False, resolve_path=True),
    default=None,
    help="Destination target for output"
)
@click.option(
    "--input-dir",
    "-i",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    default=os.getcwd(),
    help="Input target"
)
@click.option(
    "--append-filename",
    "-a",
    default=None,
    help="Modify string pattern appended to filenames, default is shortname",
)
@click.option(
    "--replace-files",
    "-rf",
    is_flag=True,
    default=False,
    help="Ignore output_dir and extension, replace all found files",
)
@click.option(
    "--resample-all",
    "-ra",
    is_flag=True,
    default=False,
    help="Resample all files found, regardless if a difference is observed",
)
@click.option(
    "--test",
    is_flag=True,
    default=False,
    help="Resample all files found, regardless if a difference is observed",
)
def convert_files(  # pylint: disable=too-many-arguments,too-many-locals
    sample_type,
    input_dir,
    output_dir,
    bit_depth,
    sample_rate,
    force_mono,
    resample_all,
    test,
    append_filename,
    replace_files,
):
    """
    Find all the files in a given location and convert to new sample types
    """
    sample_proc = get_sample_processor(sample_type)
    file_extensions = sample_proc.get_base_extensions()
    bit_depth = int(bit_depth) if bit_depth else None
    sample_rate = int(sample_rate) if sample_rate else None
    click.echo(
        f"Collecting all {file_extensions=} "
        f"for {sample_proc.__name__} conversion under {input_dir}"
    )
    target_files = find_all_target_files(input_dir, file_extensions)
    if test:
        target_files = random.sample(target_files, 5)
    # initialize counts
    total_files = len(target_files)
    converts = 0
    heretics = 0
    exceptions = []
    click.echo(
        f"Ready to convert {total_files} "
        f"{'file' if total_files == 1 else 'files'} "
        f"to {sample_proc.__name__} conversion in "
        f"{output_dir if output_dir else input_dir}"
    )
    click.pause()
    with click.progressbar(
        target_files, label="Attempting conversion"
    ) as progressbar_files:
        for _f in progressbar_files:
            existing, target = compare_file_to_target_sample(_f, sample_proc)
            target_metadata = update_target_values(
                target,
                sample_rate,
                bit_depth,
                force_mono
            )
            target.insert_instance_metadata(target_metadata)
            if existing != target or resample_all:
                try:
                    existing.resample_audio_file(target)
                    converts += 1
                except Exception as ex:  # pylint: disable=broad-except
                    heretics += 1
                    exceptions += [ex]
            if len(exceptions) > 4:
                click.echo(
                    f"Large number of exceptions occuring, printing exceptions"
                    f"{exceptions=}"
                )
                break
    click.echo(f"Completed with {total_files=} {converts=} {heretics=}")
    if exceptions:
        click.echo(f"Exceptions occurred {len(exceptions)}")
        if test:
            click.echo(f"Exceptions: \n {exceptions}")


if __name__ == "__main__":
    convert_files()  # pylint: disable=no-value-for-parameter
