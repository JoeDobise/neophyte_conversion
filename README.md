# neophyte_conversion
Recursive sample conversion for all your needing sample conversion conversions


Intent is to build an easy to use command line tool capable of converting all audio files in a given directory to a target audio file type 

v0 milestones(in progrees): 
- handle wave files (complete)
- initial set of Octatrack, Rample, Polyend Tracker file targets (complete)
- modularize code (complete)
- add commandline options (in progress)
  - source_directory: where the files should be scanned
  - target_directory: where the new files should go)
  - target_type: which type are we converting to
  - (target_sample_rate, target_bit_depth, target_mono): unsure if these would have value 

v1 milestones(projected):
- handle additional audio files: aiff & mp3
- create easy to use template for adding custom targets
- create documentation 

testing needed:
- validate mono conversion (rample and tracker targets are both mono), not sure how this sounds
- validate w/HW 

This is currently a work in progress
