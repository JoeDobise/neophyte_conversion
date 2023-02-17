# neophyte_conversion
Recursive sample conversion for all your needing sample conversion conversions


Intent is to build an easy to use command line tool capable of converting all audio files in a given directory to a target audio file type 

v0 milestones(done): 
- handle wave files (done)
- add commandline options (done)
  - input_directory: where the files should be scanned (done)
  - sample_type: which type are we converting to (done)

v1 milestones(done)
- initial set of Octatrack, Rample, Polyend Tracker file targets (done)
- modularize code (done)
- add commandline options (done)
- replaced native wave module with SoundFile and librosa modules (done)

v2 milestones(projected):
- handle additional audio files: aiff & mp3
- create easy to use template for adding custom targets
- create documentation 

testing needed:
- validate mono conversion (rample and tracker targets are both mono), not sure how this sounds
- validate w/HW 

This is currently a work in progress
